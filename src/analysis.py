"""
Hapi 2.1 — Funksionet e EDA-s (Dev B).

Çdo funksion duhet të kthejë DataFrame/dict (jo vetëm print/grafik), sepse
do të thirren nga Dev C brenda Streamlit-it.
"""

import pandas as pd


def get_monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Kthen të ardhurat e agreguara për muaj. TODO: implementim."""
    raise NotImplementedError


def get_top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Kthen top N produktet sipas sasisë/të ardhurave. TODO: implementim."""
    raise NotImplementedError


def get_country_performance(df: pd.DataFrame) -> pd.DataFrame:
    """Kthen performancën sipas vendit (Country). TODO: implementim."""
    raise NotImplementedError
