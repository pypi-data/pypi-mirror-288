from pathlib import Path

import pytest
import os
import json
from unittest.mock import Mock, patch

import tomlkit

from ai_commit.config import AppConfig, JsonConfigRepository, ConfigService, TomlConfigRepository


@pytest.fixture
def mock_config() -> AppConfig:
    return AppConfig(prompt="Test prompt", model="gpt-4-test")


@pytest.fixture
def mock_json_file(tmp_path):
    config_file = tmp_path / "config.json"
    config_data = {"prompt": "Test prompt", "model": "gpt-4-test"}
    config_file.write_text(json.dumps(config_data))
    return config_file


@pytest.fixture
def mock_toml_file(tmp_path):
    config_file = tmp_path / "config.toml"
    config_data = {"prompt": "Test prompt", "model": "gpt-4-test"}
    with open(config_file, "w") as f:
        tomlkit.dump(config_data, f)
    return config_file


def test_json_config_repository_save(tmp_path, mock_config):
    repo = JsonConfigRepository(tmp_path / "config.json")
    repo.save(mock_config)

    assert os.path.exists(repo.file_path)
    with open(repo.file_path, 'r') as f:
        saved_data = json.load(f)
    assert saved_data == mock_config.to_dict()


def test_json_config_repository_load(mock_json_file):
    repo = JsonConfigRepository(mock_json_file)
    loaded_config = repo.load()

    assert isinstance(loaded_config, AppConfig)
    assert loaded_config.prompt == "Test prompt"
    assert loaded_config.model == "gpt-4-test"


def test_json_config_repository_load_non_existent():
    repo = JsonConfigRepository(Path("non_existent.json"))
    loaded_config = repo.load()

    assert loaded_config is None


def test_toml_config_repository_load(mock_toml_file):
    repo = TomlConfigRepository(mock_toml_file)
    loaded_config = repo.load()

    assert isinstance(loaded_config, AppConfig)
    assert loaded_config.prompt == "Test prompt"
    assert loaded_config.model == "gpt-4-test"


def test_config_service_save_config(mock_config):
    mock_repo = Mock(spec=JsonConfigRepository)
    service = ConfigService(mock_repo)

    service.save_config(mock_config)

    mock_repo.save.assert_called_once_with(mock_config)


def test_config_service_get_config():
    mock_repo = Mock(spec=JsonConfigRepository)
    mock_repo.load.return_value = AppConfig(prompt="Test prompt", model="gpt-4-test")
    service = ConfigService(mock_repo)

    config = service.get_config()

    assert isinstance(config, AppConfig)
    assert config.prompt == "Test prompt"
    assert config.model == "gpt-4-test"
    mock_repo.load.assert_called_once()
