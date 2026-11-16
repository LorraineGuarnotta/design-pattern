import time
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class DataPipeline(ABC):
    source_type = "source"
    required_fields = ()

    def __init__(self, source: str):
        self.source = source
        self.data = None

    def run(self) -> str:
        self.before_run()
        self.connect()
        self.extract()
        self.transform()
        self.validate()
        self.load()
        self.cleanup()
        self.after_run()
        return f"{self.source_type} Pipeline finished"

    def connect(self):
        print(f"Connecting to {self.source_type}: {self.source}")
        time.sleep(0.5)
        print(f"{self.source_type} connection established")

    def extract(self):
        print(f"Extracting data from {self.source_type}...")
        self.data = self.read_records()
        print(f"Extracted {len(self.data)} records")

    def transform(self):
        print(f"Transforming {self.source_type} data...")
        for record in self.data:
            self.transform_record(record)
        print("Transformation complete")

    def validate(self):
        print("Validating data...")
        for record in self.data:
            if any(field not in record for field in self.required_fields):
                raise ValueError("Invalid record structure")
        print("Validation passed")

    def load(self):
        print("Loading data to destination...")
        time.sleep(0.5)
        print(f"Loaded {len(self.data)} records successfully")

    def cleanup(self):
        print("Cleaning up resources...")
        self.data = None
        print("Cleanup complete")

    def before_run(self):
        pass

    def after_run(self):
        pass

    @abstractmethod
    def read_records(self) -> list:
        pass

    @abstractmethod
    def transform_record(self, record: dict) -> None:
        pass


class CSVPipeline(DataPipeline):
    source_type = "CSV"
    required_fields = ("id", "name")

    def read_records(self) -> list:
        return [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
        ]

    def transform_record(self, record: dict) -> None:
        record["age"] = int(record["age"])
        record["name"] = record["name"].upper()


class APIPipeline(DataPipeline):
    source_type = "API"
    required_fields = ("user_id", "username")

    def read_records(self) -> list:
        return [
            {"user_id": 101, "username": "charlie", "score": 85},
            {"user_id": 102, "username": "diana", "score": 92},
        ]

    def transform_record(self, record: dict) -> None:
        record["score"] = int(record["score"])
        record["username"] = record["username"].lower()
        record["grade"] = "A" if record["score"] >= 90 else "B"

    def before_run(self):
        print("[hook] Checking API rate limit...")


class DatabasePipeline(DataPipeline):
    source_type = "Database"
    required_fields = ("product_id", "price")

    def read_records(self) -> list:
        return [
            {"product_id": 501, "product_name": "Laptop", "price": 1200},
            {"product_id": 502, "product_name": "Mouse", "price": 25},
        ]

    def transform_record(self, record: dict) -> None:
        record["price"] = float(record["price"])
        record["product_name"] = record["product_name"].title()
        record["tax"] = record["price"] * 0.2

    def after_run(self):
        print("[hook] Closing database connection pool")


class XMLPipeline(DataPipeline):
    source_type = "XML"
    required_fields = ("order_id", "amount")

    def read_records(self) -> list:
        xml = """
        <orders>
            <order><order_id>9001</order_id><customer>emma</customer><amount>59.90</amount></order>
            <order><order_id>9002</order_id><customer>lucas</customer><amount>120</amount></order>
        </orders>
        """
        root = ET.fromstring(xml)
        return [{child.tag: child.text for child in order} for order in root]

    def transform_record(self, record: dict) -> None:
        record["order_id"] = int(record["order_id"])
        record["amount"] = float(record["amount"])
        record["customer"] = record["customer"].capitalize()


if __name__ == "__main__":
    print("RUNNING CSV PIPELINE")
    print("=" * 70)
    print(f"\n{CSVPipeline('data/users.csv').run()}\n")

    print("RUNNING API PIPELINE")
    print("=" * 70)
    print(f"\n{APIPipeline('https://api.example.com/users').run()}\n")

    print("RUNNING DATABASE PIPELINE")
    print("=" * 70)
    print(f"\n{DatabasePipeline('postgresql://localhost/mydb').run()}\n")

    print("RUNNING XML PIPELINE (NEW!)")
    print("=" * 70)
    print(f"\n{XMLPipeline('data/orders.xml').run()}\n")
