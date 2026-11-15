"""Temperatura oraria da Open-Meteo, aggregata sull'Italia con media pesata."""

from datetime import timedelta
from pathlib import Path

import pandas as pd
import requests_cache

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

# Le risposte vengono salvate in data/raw (ignorata da git) e riusate per 30 giorni.
CACHE_PATH = Path(__file__).resolve().parents[2] / "data" / "raw" / "http_cache"
session = requests_cache.CachedSession(str(CACHE_PATH), expire_after=timedelta(days=30))

# nome: (latitudine, longitudine, popolazione del comune, ordine di grandezza ISTAT)
CITIES: dict[str, tuple[float, float, int]] = {
    "Roma": (41.9028, 12.4964, 2_750_000),
    "Milano": (45.4642, 9.1900, 1_370_000),
    "Napoli": (40.8518, 14.2681, 910_000),
    "Torino": (45.0703, 7.6869, 860_000),
    "Palermo": (38.1157, 13.3615, 630_000),
    "Genova": (44.4056, 8.9463, 560_000),
    "Bologna": (44.4949, 11.3426, 390_000),
    "Firenze": (43.7696, 11.2558, 360_000),
    "Bari": (41.1171, 16.8719, 310_000),
    "Venezia": (45.4408, 12.3155, 250_000),
}


def fetch_city_temperature(lat: float, lon: float, start: str, end: str) -> pd.Series:
    """Temperatura oraria a 2 m, indice DatetimeIndex in UTC."""
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start,
        "end_date": end,
        "hourly": "temperature_2m",
        "timezone": "UTC",
    }
    r = session.get(ARCHIVE_URL, params=params, timeout=30)
    r.raise_for_status()
    hourly = r.json()["hourly"]
    index = pd.to_datetime(hourly["time"], utc=True)
    return pd.Series(hourly["temperature_2m"], index=index, name="temperature_2m")


def weighted_temperature(start: str, end: str) -> pd.Series:
    """Temperatura media pesata per popolazione sulle citta' di CITIES."""
    temps = pd.DataFrame(
        {
            name: fetch_city_temperature(lat, lon, start, end)
            for name, (lat, lon, _) in CITIES.items()
        }
    )
    populations = pd.Series({name: pop for name, (_, _, pop) in CITIES.items()})
    weights = populations / populations.sum()
    return (temps * weights).sum(axis=1).rename("temperature_italy")
