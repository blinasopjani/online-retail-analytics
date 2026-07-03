"""
Hapi 2.2 — Segmentimi RFM dhe motori i rekomandimeve (Dev B).
"""

import pandas as pd


def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """Llogarit Recency, Frequency, Monetary për çdo klient. TODO: implementim."""
    raise NotImplementedError


def generate_recommendations(df: pd.DataFrame) -> list[dict]:
    """
    Gjeneron rekomandime rule-based (cross-selling, retention, optimizim
    çmimi, etj.), secili me vlerësim numerik të ndikimit të mundshëm në fitim.

    Returns
    -------
    list[dict]
        p.sh. [{"tipi": "retention", "mesazhi": "...", "ndikimi_ne_fitim_pct": 4.2}, ...]
    """
    raise NotImplementedError
