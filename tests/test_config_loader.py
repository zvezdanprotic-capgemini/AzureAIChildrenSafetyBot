from config_loader import load_config, get_age_band

def test_load_config_age_bands():
    cfg = load_config()
    assert 'age_bands' in cfg
    assert get_age_band(5) == 'child'
    assert get_age_band(16) == 'teen'
    assert get_age_band(35) == 'adult'
