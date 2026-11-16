# Design Patterns – Refactoring exercises

Refactoring of "spaghetti" code with 7 design patterns. Each file runs on its own: `python3 <file>.py`.
The UML class diagrams of every solution are in [UML.md](UML.md).

| Category | Pattern | File | What it fixes |
|---|---|---|---|
| Creational | Factory | `factory.py` | if/elif chain for payment methods → one class per method + a dictionary in `PaymentFactory` |
| Creational | Builder | `builder.py` | function with 17 parameters → fluent `EmployeeBuilder` + `DeveloperBuilder` / `InternBuilder` presets |
| Creational | Singleton | `singleton.py` + `config.json` | config file read 4 times → `ConfigManager.get_instance()` loads it once |
| Structural | Adapter | `adapter.py` | legacy XML generator vs JSON dashboard → `LegacyReportAdapter` converts XML to JSON |
| Structural | Decorator | `decorator.py` | 5 boolean flags → decorators wrapped around a `BaseOrder` |
| Behavioral | Strategy | `strategy.py` | if/elif on report format → one strategy per format, switchable with `set_strategy()` |
| Behavioral | Template Method | `template_method.py` | 3 duplicated pipelines → `run()` defined once in `DataPipeline`, hooks `before_run` / `after_run` |

## Problems identified

### Strategy – report generator
1. Adding a format (XML, Markdown) means modifying `generate_report` **and** `save_report`: it violates the Open/Closed Principle.
2. One class does everything (all formats + saving): it violates the Single Responsibility Principle.
3. Formats cannot be tested separately, you always go through the big if/elif.
4. The format cannot be changed at runtime without passing strings everywhere; a typo returns "Unknown format".
5. The if/elif chain on `format_type` is duplicated in two methods.

**Extensibility test:** `HTMLFormatStrategy` was added without modifying any existing strategy class.

### Template Method – ETL pipelines
1. Validation logic is repeated 3 times (only the required fields change).
2. Cleanup, connect and load logic are repeated 3 times, identical.
3. Adding logging to all pipelines means modifying 3 classes.
4. If the workflow order changes, it must be changed in 3 places and they can get out of sync.
5. About 80% of the code is duplicated: only extraction and transformation are really different.

**Extensibility test:** `XMLPipeline` was added by implementing only `read_records()` and `transform_record()`.

## Notes
- **Factory**: a new method (e.g. Apple Pay) is added with `PaymentFactory.register(...)` without touching existing code.
- **Decorator**: the order of the decorators changes the total (a discount applied before or after shipping does not give the same price).
- **Singleton**: `ConfigManager.load_count` shows the file is read only once.
