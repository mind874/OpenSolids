from __future__ import annotations

import math
import re
from html import unescape
from urllib.parse import urljoin

PROPERTY_MAP = {
    "thermal conductivity": "k",
    "specific heat": "cp",
    "youngs modulus": "E",
    "young modulus": "E",
    "young modulus s": "E",
    "linear expansion": "eps_th",
}

DEFAULT_UNITS = {
    "k": "W/(m*K)",
    "cp": "J/(kg*K)",
    "E": "Pa",
    "eps_th": "1",
}

COEFF_INDEX = {ch: i for i, ch in enumerate("abcdefghi")}



def _strip_tags(html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", unescape(text)).strip()



def _normalize_label(text: str) -> str:
    text = _strip_tags(text).lower()
    text = text.replace("'", "")
    text = re.sub(r"\([^)]*\)", " ", text)
    text = text.replace("-", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text



def _parse_float(text: str) -> float | None:
    clean = _strip_tags(text)
    clean = clean.replace(",", "")
    if clean in {"", ".", "-", "--"}:
        return None
    match = re.search(r"[-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?", clean)
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None



def _parse_range(text: str) -> tuple[float, float] | None:
    clean = _strip_tags(text)
    m = re.search(
        r"([-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?)\s*(?:to|–|—|-)\s*([+]?\d*\.?\d+(?:[Ee][-+]?\d+)?)",
        clean,
        flags=re.IGNORECASE,
    )
    if m:
        lo = float(m.group(1))
        hi = float(m.group(2))
        return (min(lo, hi), max(lo, hi))

    nums = re.findall(r"[-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?", clean)
    if len(nums) < 2:
        return None
    lo = float(nums[0])
    hi = float(nums[1])
    return (min(lo, hi), max(lo, hi))



def _normalize_units(property_key: str, unit_text: str) -> tuple[str, float]:
    raw_text = _strip_tags(unit_text).lower()
    raw_text = raw_text.replace("−", "-").replace("–", "-").replace("×", "x")
    raw_text = raw_text.replace("units:", "").replace("unit:", "")
    text = re.sub(r"\s+", "", raw_text).strip(":;,.")

    if property_key in {"k"} and any(
        token in text for token in {"w/(m-k)", "w/(m*k)", "w/m-k", "w/m*k"}
    ):
        return "W/(m*K)", 1.0
    if property_key in {"cp"} and any(
        token in text for token in {"j/(kg-k)", "j/(kg*k)", "j/kg-k", "j/kg*k"}
    ):
        return "J/(kg*K)", 1.0
    if property_key == "E":
        if "gpa" in text:
            return "Pa", 1e9
        if "mpa" in text:
            return "Pa", 1e6
        if text == "pa":
            return "Pa", 1.0
    if property_key == "eps_th":
        exp_match = re.search(r"(?:x|\*)\s*10(?:\s*\^|\s+)\s*([+-]?\d+)", raw_text)
        if exp_match:
            exp = int(exp_match.group(1))
            if exp >= 0:
                return "1", 10.0 ** (-exp)
            return "1", 10.0**exp
        if "microstrain" in text:
            return "1", 1e-6
        return "1", 1.0

    if text in {"1/k", "k^-1", "1perk"}:
        return "1/K", 1.0
    if text in {"1", "unitless", "dimensionless"}:
        return "1", 1.0

    # Keep raw when unknown so we do not lose metadata, but normalize separators.
    return _strip_tags(unit_text).replace("-", "*") or DEFAULT_UNITS.get(property_key, "1"), 1.0



def _extract_table_blocks(page_html: str) -> list[dict[str, str]]:
    tables = []
    for m in re.finditer(r"(?is)<table\b([^>]*)>(.*?)</table>", page_html):
        attrs = m.group(1)
        body = m.group(2)
        class_match = re.search(r"class\s*=\s*['\"]([^'\"]+)['\"]", attrs, flags=re.IGNORECASE)
        klass = class_match.group(1).lower() if class_match else ""
        tables.append({"class": klass, "body": body})
    return tables



def _table_to_rows(table_body: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for row_html in re.findall(r"(?is)<tr\b[^>]*>(.*?)</tr>", table_body):
        cells = re.findall(r"(?is)<t[dh]\b[^>]*>(.*?)</t[dh]>", row_html)
        if not cells:
            continue
        rows.append([_strip_tags(cell) for cell in cells])
    return rows



def _property_key_from_header(header: str) -> str | None:
    normalized = _normalize_label(header)
    for alias, key in PROPERTY_MAP.items():
        if alias in normalized:
            return key
    return None



def _model_hint_from_equation_text(text: str) -> str:
    t = _normalize_label(text)
    if "log10" in t or "log 10" in t:
        return "log_polynomial"
    if "t low" in t or "t<tlow" in t or "y=f" in t or "y = f" in t:
        return "piecewise"
    if "a + bt" in t or "a+b t" in t or "ct" in t:
        return "polynomial"
    return "unknown"



def _scale_model(model: dict, scale: float) -> dict:
    if abs(scale - 1.0) < 1e-15:
        return model

    mtype = model.get("type")
    if mtype == "tabular":
        return {
            **model,
            "y": [float(v) * scale for v in model["y"]],
        }
    if mtype == "polynomial":
        return {
            **model,
            "coefficients": [float(v) * scale for v in model["coefficients"]],
        }
    if mtype == "log_polynomial":
        coeffs = [float(v) for v in model["coefficients"]]
        coeffs[0] = coeffs[0] + math.log10(scale)
        return {
            **model,
            "coefficients": coeffs,
        }
    if mtype == "piecewise":
        branches = []
        for branch in model["branches"]:
            branches.append(
                {
                    **branch,
                    "model": _scale_model(branch["model"], scale),
                }
            )
        return {
            **model,
            "branches": branches,
        }
    return model



def parse_material_links(index_html: str, base_url: str) -> list[str]:
    links = re.findall(r"href\s*=\s*['\"]([^'\"]+)['\"]", index_html, flags=re.IGNORECASE)
    out: list[str] = []
    for href in links:
        resolved = urljoin(base_url, href)
        low = resolved.lower()
        if "/cryogenics/materials/" not in low:
            continue
        if not (low.endswith(".htm") or low.endswith(".html")):
            continue
        if low.endswith("materialproperties.htm"):
            continue
        out.append(resolved)
    return sorted(set(out))



def _build_property_from_column(
    property_key: str,
    rows: list[list[str]],
    col_idx: int,
    model_hint: str,
) -> dict | None:
    units_text = ""
    coeffs_by_letter: dict[str, float] = {}
    t_low: float | None = None
    f_const: float | None = None
    equation_range: tuple[float, float] | None = None
    data_range: tuple[float, float] | None = None

    for row in rows[1:]:
        if len(row) <= col_idx:
            continue

        row_label = _normalize_label(row[0])
        value_cell = row[col_idx]

        if "unit" in row_label:
            units_text = value_cell
            continue

        range_candidate = _parse_range(value_cell)
        if "equation range" in row_label and range_candidate:
            equation_range = range_candidate
            continue
        if "data range" in row_label and range_candidate:
            data_range = range_candidate
            continue

        if "tlow" in row_label or "t low" in row_label:
            t_low = _parse_float(value_cell)
            continue

        if "f>" in row_label or "f >" in row_label:
            f_const = _parse_float(value_cell)
            continue

        label_char = row_label[:1]
        if label_char in COEFF_INDEX and (row_label == label_char or row_label.startswith(label_char + " ")):
            value = _parse_float(value_cell)
            if value is not None:
                coeffs_by_letter[label_char] = value

    if not coeffs_by_letter and t_low is None and f_const is None:
        return None

    units, scale = _normalize_units(property_key, units_text or DEFAULT_UNITS[property_key])
    valid_range = equation_range or data_range or (4.0, 300.0)

    highest_idx = max(COEFF_INDEX[ch] for ch in coeffs_by_letter) if coeffs_by_letter else 0
    coeffs = [0.0] * (highest_idx + 1)
    for ch, value in coeffs_by_letter.items():
        coeffs[COEFF_INDEX[ch]] = value

    effective_hint = model_hint
    if t_low is not None and f_const is not None:
        effective_hint = "piecewise"
    elif effective_hint == "piecewise":
        # Some tables share a piecewise equation block but only specific columns include T_low/f>.
        effective_hint = "polynomial"
    elif effective_hint == "unknown":
        if len(coeffs) >= 7:
            effective_hint = "log_polynomial"
        else:
            effective_hint = "polynomial"

    if effective_hint == "log_polynomial":
        model = {"type": "log_polynomial", "coefficients": coeffs}
    elif effective_hint == "piecewise":
        poly_coeffs = coeffs[: max(1, min(len(coeffs), 5))]
        t_low_value = t_low if t_low is not None else valid_range[0]
        f_value = f_const if f_const is not None else 0.0
        model = {
            "type": "piecewise",
            "branches": [
                {
                    "condition": {"kind": "lt", "upper": float(t_low_value)},
                    "model": {
                        "type": "tabular",
                        "interpolation": "linear",
                        "T": [float(valid_range[0]), float(valid_range[1])],
                        "y": [float(f_value), float(f_value)],
                    },
                },
                {
                    "condition": {"kind": "ge", "lower": float(t_low_value)},
                    "model": {
                        "type": "polynomial",
                        "coefficients": [float(v) for v in poly_coeffs],
                    },
                },
            ],
        }
    else:
        model = {"type": "polynomial", "coefficients": coeffs}

    model = _scale_model(model, scale)

    return {
        "units": units,
        "valid_T_min": float(valid_range[0]),
        "valid_T_max": float(valid_range[1]),
        "recommended_T_min": None,
        "recommended_T_max": None,
        "model": model,
    }



def _extract_properties_from_tables(page_html: str) -> dict[str, dict]:
    properties: dict[str, dict] = {}

    tables = _extract_table_blocks(page_html)
    for i, table in enumerate(tables):
        if "properties" not in table["class"]:
            continue

        rows = _table_to_rows(table["body"])
        if len(rows) < 2 or len(rows[0]) < 2:
            continue

        equation_hint = "unknown"
        for j in range(i + 1, min(i + 3, len(tables))):
            if "equation" in tables[j]["class"]:
                equation_hint = _model_hint_from_equation_text(tables[j]["body"])
                break

        headers = rows[0]
        for col_idx in range(1, len(headers)):
            prop_key = _property_key_from_header(headers[col_idx])
            if prop_key is None:
                continue

            prop = _build_property_from_column(prop_key, rows, col_idx, equation_hint)
            if prop is None:
                continue

            properties[prop_key] = prop

    return properties



def _extract_section(html: str, heading: str) -> str | None:
    pattern = rf"(?is)<h[1-6][^>]*>\s*{re.escape(heading)}\s*</h[1-6]>(.*?)(?=<h[1-6][^>]*>|</body>)"
    match = re.search(pattern, html)
    return match.group(1) if match else None



def _extract_properties_from_sections(page_html: str) -> dict[str, dict]:
    properties: dict[str, dict] = {}

    for heading, property_key in PROPERTY_MAP.items():
        block = _extract_section(page_html, heading.title())
        if block is None:
            block = _extract_section(page_html, heading)
        if block is None and "youngs" in heading:
            block = _extract_section(page_html, heading.replace("youngs", "young's"))
        if block is None:
            continue
        if property_key in properties:
            continue

        text = _normalize_label(block)

        found: dict[int, float] = {}
        for idx, value in re.findall(
            r"\ba\s*([0-8])\s*(?:=|:)\s*([-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?)",
            block,
            flags=re.IGNORECASE,
        ):
            found[int(idx)] = float(value)
        for letter, value in re.findall(
            r"\b([a-i])\s*(?:=|:)\s*([-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?)",
            block,
            flags=re.IGNORECASE,
        ):
            found[COEFF_INDEX[letter.lower()]] = float(value)
        coeffs = [found.get(i, 0.0) for i in range(max(found.keys()) + 1)] if found else [0.0]

        temp_range = _parse_range(_strip_tags(block)) or (4.0, 300.0)
        units, scale = _normalize_units(property_key, _strip_tags(block))

        if "log10" in text or "log poly" in text:
            model = {"type": "log_polynomial", "coefficients": coeffs}
        elif "piecewise" in text:
            model = {
                "type": "piecewise",
                "branches": [
                    {
                        "condition": {"kind": "lt", "upper": float(temp_range[0])},
                        "model": {
                            "type": "tabular",
                            "interpolation": "linear",
                            "T": [float(temp_range[0]), float(temp_range[1])],
                            "y": [0.0, 0.0],
                        },
                    },
                    {
                        "condition": {"kind": "ge", "lower": float(temp_range[0])},
                        "model": {
                            "type": "polynomial",
                            "coefficients": coeffs,
                        },
                    },
                ],
            }
        else:
            model = {"type": "polynomial", "coefficients": coeffs}

        properties[property_key] = {
            "units": units,
            "valid_T_min": float(temp_range[0]),
            "valid_T_max": float(temp_range[1]),
            "recommended_T_min": None,
            "recommended_T_max": None,
            "model": _scale_model(model, scale),
        }

    return properties



def parse_material_page(page_html: str, page_url: str) -> dict:
    title_match = re.search(r"(?is)<title[^>]*>(.*?)</title>", page_html)
    h1_match = re.search(r"(?is)<h1[^>]*>(.*?)</h1>", page_html)
    name = _strip_tags(h1_match.group(1) if h1_match else (title_match.group(1) if title_match else "Unknown"))
    name = re.sub(r"(?i)^material properties:\s*", "", name).strip()

    properties = _extract_properties_from_tables(page_html)
    if not properties:
        properties = _extract_properties_from_sections(page_html)

    return {
        "name": name,
        "url": page_url,
        "properties": properties,
    }
