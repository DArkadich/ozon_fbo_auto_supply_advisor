from src import utils


def test_load_config_handles_missing_file(tmp_path):
    missing_file = tmp_path / "nope.json"
    config = utils.load_config(missing_file)
    assert isinstance(config, dict)
    assert config == {}


def test_setup_logging_creates_logger():
    logger = utils.setup_logging()
    assert logger is not None
