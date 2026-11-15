# Spec: previsione day-ahead di carico e prezzo elettrico in Italia

Status: approved

## Obiettivo
Progetto di data science end-to-end per portfolio e CV (ruolo: Data Scientist): dati reali, modello, app interattiva, repo curato.

## Decisioni
| Area | Decisione |
|---|---|
| Stack | Python, scikit-learn, LightGBM, SQL |
| Dominio | Energia: carico e prezzo elettrico italiano |
| Dati | ENTSO-E Transparency, 2019-2025, orari. Carico: Italia totale. Prezzi day-ahead: zona IT-North (proxy del PUN, che e' pubblicato da GME; da dichiarare nel README). Meteo: Open-Meteo. |
| Target | Carico e prezzo, orizzonte day-ahead (24 ore) |
| Modelli | Baseline naive, regressione lineare, LightGBM |
| Validazione | Walk-forward; ultimo anno come test finale |
| Successo | Carico: MAE almeno 20% migliore della baseline naive. Prezzo: battere la baseline, riportando il risultato onestamente. |
| Deliverable | Repo GitHub curato (uv, ruff, pytest, GitHub Actions) + app Streamlit (solo locale per ora) |
| App | Previsione 24h con intervalli; confronto modelli/metriche; SHAP; esplorazione dati. Se il tempo stringe, tagliare per prime esplorazione e SHAP. |
| Lingua | Solo italiano |
| Tempo | 3-4 settimane, 5-8 ore/settimana; MVP entro la settimana 2 |

## Note operative
- Token ENTSO-E: registrazione gratuita, chiave in `.env` (mai committata).
- Rischio: il prezzo e' molto piu' volatile del carico (picco 2022); includerlo nella valutazione per regime.
