"""
Hapi 1.2 — Pastrimi dhe standardizimi i të dhënave (Dev A).

Ky funksion do të përdoret dy herë:
1. Nga Dev B për EDA (notebook 02).
2. Nga Dev C brenda Streamlit-it, për çdo CSV të ri që klienti ngarkon.

Prandaj duhet të mbetet një funksion i pastër, pa side-effects (nuk printon,
nuk lexon skedarë vetë — merr DataFrame, kthen DataFrame).
"""

import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pastron datasetin "Online Retail II".

    Hapat (për t'u implementuar):
    - Trajtimi i CustomerID mungesë (p.sh. shënim si "Guest").
    - Klasifikimi i Quantity negative si kthime/refunds (jo fshirje verbër).
    - Filtrimi/analiza e UnitPrice <= 0.
    - Konvertimi i InvoiceDate në datetime.
    - Krijimi i kolonës Revenue = Quantity * UnitPrice.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset i papërpunuar (raw).

    Returns
    -------
    pd.DataFrame
        Dataset i pastruar.
    """
    df_clean = df.copy()

    # TODO: implemento hapat e pastrimit këtu

    return df_clean
