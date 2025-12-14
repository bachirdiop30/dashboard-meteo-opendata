"""
Nettoyage des données climatologiques horaires Météo-France.

- Lecture des fichiers CSV compressés (.csv.gz)
- Fusion des départements et périodes
- Sélection des variables pertinentes
- Conversion des dates
- Sauvegarde dans data/cleaned
"""

from pathlib import Path
import pandas as pd


RAW_DIR = Path("data/raw")
CLEAN_DIR = Path("data/cleaned")
OUTPUT_FILE = CLEAN_DIR / "meteo_cleaned.csv"


def load_raw_data() -> pd.DataFrame:
    dfs = []

    for file in RAW_DIR.glob("*.csv.gz"):
        print(f"Lecture : {file.name}")

        # extraction du département depuis le nom du fichier
        departement = file.name.split("_")[2]

        df = pd.read_csv(file, sep=";", compression="gzip")
        df["departement"] = departement

        dfs.append(df)

    if not dfs:
        raise FileNotFoundError("Aucun fichier .csv.gz trouvé dans data/raw")

    return pd.concat(dfs, ignore_index=True)



def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    columns_to_keep = [
        "NUM_POSTE",
        "NOM_USUEL",
        "LAT",
        "LON",
        "ALTI",
        "AAAAMMJJHH",
        "FF",
        "DD",
        "T",
        "TD",
        "U",
        "PMER",
        "PSTAT",
        "departement"
    ]

    df = df[columns_to_keep]

    df = df.rename(columns={
        "NUM_POSTE": "station_id",
        "NOM_USUEL": "station_name",
        "LAT": "lat",
        "LON": "lon",
        "ALTI": "altitude",
        "AAAAMMJJHH": "datetime",
        "FF": "wind_speed",
        "DD": "wind_dir",
        "T": "temperature",
        "TD": "dew_point",
        "U": "humidity",
        "PMER": "pressure_sea",
        "PSTAT": "pressure_station"
    })

    df["datetime"] = pd.to_datetime(df["datetime"], format="%Y%m%d%H", errors="coerce")

    # nettoyage MINIMAL
    df = df.dropna(subset=["datetime"])

    # conversions
    df["temperature"] = df["temperature"] / 10
    df["dew_point"] = df["dew_point"] / 10

    df["hour"] = df["datetime"].dt.hour
    df["year"] = df["datetime"].dt.year
    df["month"] = df["datetime"].dt.month

    return df


def main() -> None:
    df_raw = load_raw_data()
    df_clean = clean_data(df_raw)

    df_clean.to_csv(OUTPUT_FILE, index=False)
    print(f"✔ Données nettoyées sauvegardées dans : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
