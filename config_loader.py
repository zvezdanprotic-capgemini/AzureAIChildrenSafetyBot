import yaml
from functools import lru_cache
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / 'safety_config.yaml'

@lru_cache(maxsize=1)
def load_config():
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_age_band(age: int) -> str:
    cfg = load_config()
    for band_name, band in cfg['age_bands'].items():
        if age <= band['max_age']:
            return band_name
    return 'adult'


def is_allowed_by_severity(age_band: str, categories: dict) -> bool:
    cfg = load_config()
    thresholds = cfg['age_bands'][age_band]['severity_thresholds']
    for cat_key, sev in categories.items():
        limit = thresholds.get(cat_key.lower())
        if limit is not None and sev > limit:
            return False
    return True
