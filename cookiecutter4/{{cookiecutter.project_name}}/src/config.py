from services.utils import get_project_dir

PROJECT_ROOT = get_project_dir()

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_PATH = DATA_DIR /

OUTPUTS_DIR = PROJECT_ROOT / "outputs"

CONFIGS_DIR = PROJECT_ROOT / "configs"
SETTINGS_FILE = CONFIGS_DIR / "settings.yaml"

APP_TITLE = "<app_title"
LAYOUT = "wide"