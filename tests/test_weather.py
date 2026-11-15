import pandas as pd
import pytest

from energy_forecast import weather

HOURS = pd.date_range("2024-01-01", periods=3, freq="h", tz="UTC")


def fake_fetch(value_by_lat):
    """Costruisce una finta fetch_city_temperature: la temperatura dipende dalla latitudine."""

    def _fetch(lat, lon, start, end):
        return pd.Series(value_by_lat(lat), index=HOURS)

    return _fetch


def test_uniform_temperature_gives_same_value(monkeypatch):
    # Se ogni citta' ha 15 C, la media pesata deve essere 15 (i pesi sommano a 1).
    monkeypatch.setattr(weather, "fetch_city_temperature", fake_fetch(lambda lat: 15.0))
    result = weather.weighted_temperature("2024-01-01", "2024-01-01")
    assert result.tolist() == pytest.approx([15.0, 15.0, 15.0])


def test_big_city_weighs_more_than_simple_average(monkeypatch):
    # Roma a 0 C, tutte le altre a 20 C: il risultato deve essere sotto la media semplice (18 C)
    # perche' Roma e' la citta' piu' popolosa.
    rome_lat = weather.CITIES["Roma"][0]
    monkeypatch.setattr(
        weather,
        "fetch_city_temperature",
        fake_fetch(lambda lat: 0.0 if lat == rome_lat else 20.0),
    )
    result = weather.weighted_temperature("2024-01-01", "2024-01-01")
    simple_average = 18.0
    assert (result < simple_average).all()
