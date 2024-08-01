# config_package/__init__.py

from locobuzz_python_configuration.config_builder import ConfigurationBuilder
from locobuzz_python_configuration.sql_config_builder import SQLConfigurationBuilder
from locobuzz_python_configuration.clickhouse_config_builder import ClickHouseConfigurationBuilder
from locobuzz_python_configuration.aws_config_builder import AWSConfigurationBuilder
from locobuzz_python_configuration.elastic_config_builder import ElasticSearchConfigurationBuilder
from locobuzz_python_configuration.kafka_config_builder import KafkaConfigurationBuilder


def create_configuration(file_path=None, config_data=None, required_components=[],
                         builder_classes=None):
    builder = ConfigurationBuilder()

    default_builders = {
        'sql': SQLConfigurationBuilder,
        'clickhouse': ClickHouseConfigurationBuilder,
        'aws': AWSConfigurationBuilder,
        'elastic': ElasticSearchConfigurationBuilder,
        'kafka': KafkaConfigurationBuilder,
    }

    # Merge default builders with provided builders, if any
    if builder_classes:
        default_builders.update(builder_classes)

    # Setting the specific builders
    if 'sql' in default_builders:
        builder.set_sql_builder(default_builders['sql'](builder.get_configuration()))
    if 'clickhouse' in default_builders:
        builder.set_clickhouse_builder(default_builders['clickhouse'](builder.get_configuration()))
    if 'aws' in default_builders:
        builder.set_aws_builder(default_builders['aws'](builder.get_configuration()))
    if 'elastic' in default_builders:
        builder.set_elastic_builder(default_builders['elastic'](builder.get_configuration()))
    if 'kafka' in default_builders:
        builder.set_kafka_builder(default_builders['kafka'](builder.get_configuration()))

    try:
        if file_path:
            builder.load_from_file(file_path, required_components)
        elif config_data:
            builder.load_from_dict(config_data, required_components)
        else:
            raise ValueError("Either file_path or config_data must be provided")

        return builder.get_configuration()
    except Exception as e:
        print(f"Error creating configuration: {e}")
        return None
# config_package/__init__.py

from locobuzz_python_configuration.config_builder import ConfigurationBuilder
from locobuzz_python_configuration.sql_config_builder import SQLConfigurationBuilder
from locobuzz_python_configuration.clickhouse_config_builder import ClickHouseConfigurationBuilder
from locobuzz_python_configuration.aws_config_builder import AWSConfigurationBuilder
from locobuzz_python_configuration.elastic_config_builder import ElasticSearchConfigurationBuilder
from locobuzz_python_configuration.kafka_config_builder import KafkaConfigurationBuilder


def create_configuration(file_path=None, config_data=None, required_components=[],
                         builder_classes=None):
    builder = ConfigurationBuilder()

    default_builders = {
        'sql': SQLConfigurationBuilder,
        'clickhouse': ClickHouseConfigurationBuilder,
        'aws': AWSConfigurationBuilder,
        'elastic': ElasticSearchConfigurationBuilder,
        'kafka': KafkaConfigurationBuilder,
    }

    # Merge default builders with provided builders, if any
    if builder_classes:
        default_builders.update(builder_classes)

    # Setting the specific builders
    if 'sql' in default_builders:
        builder.set_sql_builder(default_builders['sql'](builder.get_configuration()))
    if 'clickhouse' in default_builders:
        builder.set_clickhouse_builder(default_builders['clickhouse'](builder.get_configuration()))
    if 'aws' in default_builders:
        builder.set_aws_builder(default_builders['aws'](builder.get_configuration()))
    if 'elastic' in default_builders:
        builder.set_elastic_builder(default_builders['elastic'](builder.get_configuration()))
    if 'kafka' in default_builders:
        builder.set_kafka_builder(default_builders['kafka'](builder.get_configuration()))

    try:
        if file_path:
            builder.load_from_file(file_path, required_components)
        elif config_data:
            builder.load_from_dict(config_data, required_components)
        else:
            raise ValueError("Either file_path or config_data must be provided")

        return builder.get_configuration()
    except Exception as e:
        print(f"Error creating configuration: {e}")
        raise e

# if __name__ == "__main__":
#     CONFIG = create_configuration(file_path='appsettings.json', required_components=["sql", "kafka"])
#     print(CONFIG.__dict__)
#     SERVICE_NAME = "FACEBOOK_PAGE_INSIGHT_READER_SERVICE"
#     IS_ASYNC_LOGGER = CONFIG.__dict__.get('_is_async_logger', False)

