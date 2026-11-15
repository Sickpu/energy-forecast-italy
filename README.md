# Previsione day-ahead di carico e prezzo elettrico in Italia

Progetto di data science end-to-end: dati ENTSO-E e Open-Meteo, modelli (baseline, regressione lineare, LightGBM), validazione walk-forward e app Streamlit.

> Lavori in corso. Specifica: `.scratch/previsione-carico-prezzo/spec.md`.

## Setup

```bash
python -m uv sync --group dev
cp .env.example .env   # inserisci il token ENTSO-E
python -m uv run pytest
```
