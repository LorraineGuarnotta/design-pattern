import json
from pathlib import Path


class ConfigManager:
    _instance = None
    load_count = 0

    def __init__(self, path: str):
        if ConfigManager._instance is not None:
            raise RuntimeError("Use ConfigManager.get_instance()")
        with open(path, "r") as f:
            self._config = json.load(f)
        ConfigManager.load_count += 1

    @classmethod
    def get_instance(cls, path: str = None):
        if cls._instance is None:
            path = path or Path(__file__).parent / "config.json"
            cls._instance = cls(path)
        return cls._instance

    def get(self, key: str, default=None):
        value = self._config
        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return default
            value = value[part]
        return value

    def set(self, key: str, new_value) -> None:
        parts = key.split(".")
        current = self._config
        for part in parts[:-1]:
            current = current.setdefault(part, {})
        current[parts[-1]] = new_value


def connect_database():
    config = ConfigManager.get_instance()
    print(f"Connecting to database at {config.get('database.host')}:{config.get('database.port')}")


def send_email(to: str, subject: str):
    config = ConfigManager.get_instance()
    print(f"Sending email from {config.get('email.sender')} via {config.get('email.smtp_host')}")


def process_payment(amount: float):
    config = ConfigManager.get_instance()
    print(f"Processing {amount}€ in {config.get('payment.environment')} mode")


def start_application():
    config = ConfigManager.get_instance()
    print(f"Starting {config.get('app.name')} (debug={config.get('app.debug')})")


if __name__ == "__main__":
    start_application()
    connect_database()
    send_email("user@test.com", "Welcome")
    process_payment(99.99)

    first = ConfigManager.get_instance()
    second = ConfigManager.get_instance()
    print("Same instance:", first is second)
    print("File loaded", ConfigManager.load_count, "time(s)")

    first.set("payment.environment", "production")
    process_payment(10.0)
