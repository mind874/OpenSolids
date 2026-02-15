# Releasing OpenSolids To PyPI

## Prerequisites

- PyPI account with 2FA enabled.
- Maintainer access to this GitHub repository.
- A PyPI API token scoped to your project (recommended), or account-wide token.

## 1. Create/Register the PyPI Project

The package name is `opensolids`.

Before first release, check if the name is available:

```bash
python -m pip index versions opensolids
```

If this returns "No matching distribution found", the name is likely still available.

## 2. Create a PyPI API Token

In PyPI:

1. Go to `Account settings` -> `API tokens`.
2. Create a token for project `opensolids` (or account-wide if needed).
3. Copy the token once.

## 3. Add GitHub Secret

In GitHub repo settings:

1. Go to `Settings` -> `Secrets and variables` -> `Actions`.
2. Add secret named `PYPI_API_TOKEN`.
3. Paste the token value.

## 4. Publish via GitHub Actions

Workflow file: `.github/workflows/publish-pypi.yml`

Publish options:

- Create a GitHub Release (workflow triggers automatically).
- Or run `Publish To PyPI` manually from the Actions tab.

The workflow builds from repo root and publishes:

- `opensolids` (wheel + sdist)

## 5. Verify Install

After publish:

```bash
pip install opensolids
python -c "import opensolids as osl; print(osl.list_providers())"
```

Expected providers include `nist-cryo`, `ntrs`, and `mil-hdbk-5`.

## Manual Publish (Optional)

From repository root:

```bash
python -m pip install --upgrade build twine
python -m build --sdist --wheel --outdir dist .
python -m twine check dist/*
python -m twine upload dist/*
```

When prompted, use:

- Username: `__token__`
- Password: your `pypi-...` token
