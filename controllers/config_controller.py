from models.config_model import ConfigModel


class ConfigController:
    def __init__(self, config_file: str = None):
        self.config = ConfigModel(config_file)

    def get_language_file(self, key: str = "language_file") -> str:
        return self.config.get(key)

    def get_total_questions(self) -> int:
        return self.config.get("total_questions")

    def get_complete_config(self) -> dict:
        return self.config.get_all()

    def get_config_value(self, key: str) -> any:
        """
        Retrieve a specific configuration value by key.

        Args:
            key (str): The configuration key to retrieve.

        Returns:
            any: The value associated with the key.
        """
        return self.config.get(key)
