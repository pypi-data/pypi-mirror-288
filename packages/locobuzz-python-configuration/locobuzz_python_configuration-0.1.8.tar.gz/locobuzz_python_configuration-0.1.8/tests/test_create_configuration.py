# test_create_configuration.py
import pytest
from locobuzz_python_configuration import create_configuration, InvalidConfigurationError,
from extended_sql_config_builder import ExtendedSQLConfigurationBuilder

from locobuzz_python_configuration.sql_config_builder import InvalidSQLConfigurationError


def test_create_configuration_from_file():
    config = create_configuration(file_path='settings.json', required_components=["sql", "clickhouse", "aws", "elastic"])
    assert config is not None
    assert isinstance(config.__dict__, dict)

def test_create_configuration_from_dict():
    config_data = {
        "sql": {"sql_database_name": "test_db"},
        "clickhouse": {},
        "aws": {},
        "elastic": {}
    }
    config = create_configuration(config_data=config_data, required_components=["sql", "clickhouse", "aws", "elastic"])
    assert config is not None
    assert isinstance(config.__dict__, dict)

def test_create_configuration_missing_component():
    with pytest.raises(InvalidConfigurationError):
        create_configuration(file_path='settings.json', required_components=["sql", "clickhouse", "aws", "elastic", "missing_component"])

def test_extended_sql_configuration_builder_valid():
    config_data = {"sql_database_name": "test_db"}
    builder = ExtendedSQLConfigurationBuilder(config={})
    builder.build(config_data)
    assert builder._sql_database_name == "test_db"

def test_extended_sql_configuration_builder_missing_name():
    config_data = {}
    builder = ExtendedSQLConfigurationBuilder(config={})
    with pytest.raises(InvalidSQLConfigurationError):
        builder.build(config_data)