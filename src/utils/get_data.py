# src/utils/get_data.py

import os
import requests
from tqdm import tqdm  # pour barre de progression

# --------------------------------------------------
# 1️⃣ Départements et fichiers à télécharger
# --------------------------------------------------

fichiers = {
    "01": {
        "1890-1899": "https://www.data.gouv.fr/api/1/datasets/r/c66dc0d5-b4ac-4801-9115-5f7f95785d79",
        "1900-1909": "https://www.data.gouv.fr/api/1/datasets/r/16bd3e0e-33dd-4389-83a9-dd26114f84f7", 
    },
    "13": {
        "1890-1899": "https://www.data.gouv.fr/api/1/datasets/r/fc252327-35f9-4d6e-aaf3-9617d414ad28",
        "1900-1909": "https://www.data.gouv.fr/api/1/datasets/r/c7a0f9c8-a2ed-49fb-b6a1-8153338c629d",
    },
    "75": {
        "1890-1899": "https://www.data.gouv.fr/api/1/datasets/r/b1d5a728-70f9-4fbb-8302-2e753c1025d0",
        "1900-1909": "https://www.data.gouv.fr/api/1/datasets/r/f4274981-d774-4c3d-9a45-153282ecb50b",
    }
}
# --------------------------------------------------
# 2️⃣ Fonction pour télécharger un fichier
# --------------------------------------------------
def download_file(url, output_path):
    """Télécharge un fichier avec barre de progression"""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(output_path, 'wb') as f, tqdm(
        desc=output_path,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)

# --------------------------------------------------
# 3️⃣ Fonction principale
# --------------------------------------------------
def get_data():
    os.makedirs("data/raw", exist_ok=True)  # créer le dossier si nécessaire

    for dept, periodes in fichiers.items():
        for periode, url in periodes.items():
            filename = f"HOR_departement_{dept}_periode_{periode}.csv.gz"
            output_path = os.path.join("data/raw", filename)

            if not os.path.exists(output_path):
                print(f"Téléchargement : {filename}")
                try:
                    download_file(url, output_path)
                    print(f"✔ Téléchargement terminé : {filename}")
                except Exception as e:
                    print(f"❌ Erreur téléchargement {filename} : {e}")
            else:
                print(f"⚠ Fichier déjà présent : {filename}")

# --------------------------------------------------
# 4️⃣ Lancer le script
# --------------------------------------------------
if __name__ == "__main__":
    get_data()
