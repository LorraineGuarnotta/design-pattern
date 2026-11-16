import json
from abc import ABC, abstractmethod


class ReportFormatStrategy(ABC):
    extension = ""

    @abstractmethod
    def format(self, data: list) -> str:
        pass


class PDFFormatStrategy(ReportFormatStrategy):
    extension = ".pdf"

    def format(self, data: list) -> str:
        report = "PDF REPORT\n" + "=" * 50 + "\n"
        for item in data:
            report += f"| {item['name']:20} | {item['value']:10} |\n"
        report += "=" * 50 + "\nEnd of PDF Report"
        return report


class ExcelFormatStrategy(ReportFormatStrategy):
    extension = ".xlsx"

    def format(self, data: list) -> str:
        report = "EXCEL REPORT\n" + "-" * 50 + "\nName\tValue\n"
        for item in data:
            report += f"{item['name']}\t{item['value']}\n"
        report += "-" * 50 + "\n"
        return report


class CSVFormatStrategy(ReportFormatStrategy):
    extension = ".csv"

    def format(self, data: list) -> str:
        report = "name,value\n"
        for item in data:
            report += f"{item['name']},{item['value']}\n"
        return report


class JSONFormatStrategy(ReportFormatStrategy):
    extension = ".json"

    def format(self, data: list) -> str:
        return json.dumps(data, indent=2)


class HTMLFormatStrategy(ReportFormatStrategy):
    extension = ".html"

    def format(self, data: list) -> str:
        rows = "".join(f"<tr><td>{item['name']}</td><td>{item['value']}</td></tr>" for item in data)
        return f"<table><tr><th>Name</th><th>Value</th></tr>{rows}</table>"


class ReportGenerator:
    def __init__(self, data: list, strategy: ReportFormatStrategy = None):
        self.data = data
        self._strategy = strategy

    def set_strategy(self, strategy: ReportFormatStrategy) -> None:
        self._strategy = strategy

    def generate_report(self) -> str:
        if self._strategy is None:
            raise ValueError("No format strategy set")
        return self._strategy.format(self.data)

    def save_report(self, filename: str) -> str:
        path = filename + self._strategy.extension
        with open(path, "w") as f:
            f.write(self.generate_report())
        return path


if __name__ == "__main__":
    data = [
        {"name": "Sales Q1", "value": 15000},
        {"name": "Sales Q2", "value": 18000},
        {"name": "Sales Q3", "value": 22000},
        {"name": "Sales Q4", "value": 25000},
    ]

    generator = ReportGenerator(data)

    print("=== PDF FORMAT ===")
    generator.set_strategy(PDFFormatStrategy())
    print(generator.generate_report())

    print("\n" + "=" * 60 + "\n")

    print("=== CSV FORMAT ===")
    generator.set_strategy(CSVFormatStrategy())
    print(generator.generate_report())

    print("\n" + "=" * 60 + "\n")

    print("=== JSON FORMAT ===")
    generator.set_strategy(JSONFormatStrategy())
    print(generator.generate_report())

    print("\n" + "=" * 60 + "\n")

    print("=== HTML FORMAT (NEW!) ===")
    generator.set_strategy(HTMLFormatStrategy())
    print(generator.generate_report())

    print("\n" + "=" * 60 + "\n")
    generator.set_strategy(CSVFormatStrategy())
    print("Saved to", generator.save_report("sales_report"))
