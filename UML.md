# UML class diagrams

## 1. Factory – Payment system

```mermaid
classDiagram
    class PaymentProcessor {
        <<abstract>>
        +method: str
        +validate(details) bool*
        +compute_fee(amount) float*
        +process(amount, details) dict
    }
    class CreditCardProcessor {
        +validate(details) bool
        +compute_fee(amount) float
    }
    class BankTransferProcessor {
        +validate(details) bool
        +compute_fee(amount) float
    }
    class PayPalProcessor {
        +validate(details) bool
        +compute_fee(amount) float
    }
    class PaymentFactory {
        -_processors: dict
        +get_processor(payment_type) PaymentProcessor
        +register(payment_type, processor_class)$
    }
    PaymentProcessor <|-- CreditCardProcessor
    PaymentProcessor <|-- BankTransferProcessor
    PaymentProcessor <|-- PayPalProcessor
    PaymentFactory ..> PaymentProcessor : creates
```

## 2. Builder – HR Employee onboarding

```mermaid
classDiagram
    class Employee {
        <<dataclass>>
        +first_name: str
        +last_name: str
        +email: str
        +department: str
        +position: str
        +salary: float
        +has_laptop: bool
        +has_vpn_access: bool
        +has_admin_rights: bool
        +contract_type: str
    }
    class EmployeeBuilder {
        -_data: dict
        +with_name(first, last) EmployeeBuilder
        +with_email(email) EmployeeBuilder
        +with_job(department, position, salary) EmployeeBuilder
        +with_equipment(laptop, parking) EmployeeBuilder
        +with_access(vpn, admin) EmployeeBuilder
        +with_contract(contract_type) EmployeeBuilder
        +build() Employee
    }
    class DeveloperBuilder {
        +__init__(first, last, email)
    }
    class InternBuilder {
        +__init__(first, last, email, department)
    }
    EmployeeBuilder <|-- DeveloperBuilder
    EmployeeBuilder <|-- InternBuilder
    EmployeeBuilder ..> Employee : builds
```

## 3. Singleton – Configuration manager

```mermaid
classDiagram
    class ConfigManager {
        -_instance: ConfigManager$
        -_config: dict
        +get_instance()$ ConfigManager
        +get(key) any
        +set(key, value)
    }
    note for ConfigManager "Only one instance: the file is read once"
    class DatabaseService
    class EmailService
    class PaymentService
    DatabaseService ..> ConfigManager : get_instance()
    EmailService ..> ConfigManager : get_instance()
    PaymentService ..> ConfigManager : get_instance()
```

## 4. Adapter – Reporting system

```mermaid
classDiagram
    class ReportGeneratorInterface {
        <<interface>>
        +generate(data) str
    }
    class LegacyReportAdapter {
        -_legacy: LegacyReportGenerator
        +generate(data) str
        -_xml_to_json(xml) str
    }
    class LegacyReportGenerator {
        +generate_report(data) str
    }
    class AnalyticsDashboard {
        +display(json_data)
    }
    ReportGeneratorInterface <|.. LegacyReportAdapter
    LegacyReportAdapter o-- LegacyReportGenerator : wraps
    AnalyticsDashboard ..> ReportGeneratorInterface : uses JSON
```

## 5. Decorator – Order pricing

```mermaid
classDiagram
    class OrderComponent {
        <<interface>>
        +get_cost() float
        +get_description() str
    }
    class BaseOrder {
        +base_price: float
        +get_cost() float
        +get_description() str
    }
    class OrderDecorator {
        <<abstract>>
        -_order: OrderComponent
        +get_cost() float
        +get_description() str
    }
    class ExpressShippingDecorator
    class InsuranceDecorator
    class GiftWrapDecorator
    class DiscountDecorator {
        +percent: float
    }
    class PremiumMemberDecorator
    OrderComponent <|.. BaseOrder
    OrderComponent <|.. OrderDecorator
    OrderDecorator o-- OrderComponent : wraps
    OrderDecorator <|-- ExpressShippingDecorator
    OrderDecorator <|-- InsuranceDecorator
    OrderDecorator <|-- GiftWrapDecorator
    OrderDecorator <|-- DiscountDecorator
    OrderDecorator <|-- PremiumMemberDecorator
```

## 6. Strategy – Report formats

```mermaid
classDiagram
    class ReportGenerator {
        +data: list
        -_strategy: ReportFormatStrategy
        +set_strategy(strategy)
        +generate_report() str
        +save_report(filename) str
    }
    class ReportFormatStrategy {
        <<interface>>
        +extension: str
        +format(data) str
    }
    class PDFFormatStrategy
    class ExcelFormatStrategy
    class CSVFormatStrategy
    class JSONFormatStrategy
    class HTMLFormatStrategy
    ReportGenerator o-- ReportFormatStrategy : uses
    ReportFormatStrategy <|.. PDFFormatStrategy
    ReportFormatStrategy <|.. ExcelFormatStrategy
    ReportFormatStrategy <|.. CSVFormatStrategy
    ReportFormatStrategy <|.. JSONFormatStrategy
    ReportFormatStrategy <|.. HTMLFormatStrategy
```

## 7. Template Method – ETL pipeline

```mermaid
classDiagram
    class DataPipeline {
        <<abstract>>
        +source: str
        +required_fields: tuple
        +run() str
        +connect()
        +extract()
        +transform()
        +validate()
        +load()
        +cleanup()
        +before_run()
        +after_run()
        +read_records() list*
        +transform_record(record)*
    }
    class CSVPipeline
    class APIPipeline {
        +before_run()
    }
    class DatabasePipeline {
        +after_run()
    }
    class XMLPipeline
    DataPipeline <|-- CSVPipeline
    DataPipeline <|-- APIPipeline
    DataPipeline <|-- DatabasePipeline
    DataPipeline <|-- XMLPipeline
```
