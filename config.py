from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"

MORTALITY_FILE = DATA_DIR / "Anexo1.NoFetal2019_CE_15-03-23.xlsx"
CAUSES_FILE = DATA_DIR / "Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx"
DIVIPOLA_FILE = DATA_DIR / "Divipola_CE_.xlsx"
GEOJSON_FILE = DATA_DIR / "Colombia.geo.json"

MORTALITY_SHEET = "No_Fetales_2019"
CAUSES_SHEET = "Final"
DIVIPOLA_SHEET = "Hoja1"
