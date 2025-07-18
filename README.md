# PyDk Custom

A simple Python SDK for Applifting API communication

---
📁 Table of contents:

- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
    - [Package Usage](#-package-usage)
    - [Simple Facade Example](#-simple-facade-example)
- [Development](#-development)
- [Acknowledgments](#-acknowledgments)
- [Future Development](#-future-development)

---

## 🚀 Features

* Async-first Python SDK
* Pluggable architecture for:

    * Token caching (in-memory or SQLite)
    * HTTP client adapters
* Simple facade for API communication

## ⚙️ Installation

Clone or install as package:

```bash
    # Clone repository
    git clone https://github.com/suvreal/PyDk
    
    # Install package locally
    pip install ./dist/pydk_custom-0.1.0-py3-none-any.whl
    
    # Or install directly from GitHub
    pip install git+https://github.com/suvreal/PyDk
```

Import into your Python project:

```python
    from py_dk_custom import MyApiSDK
```

## 🐍 Usage

### Package Usage

Check `examples/py_dk_custom_script.py` for implementation:

```bash
    source venv/bin/activate
    python -m examples.py_dk_custom_script
```

Expected output:

```json
    Register response: {"status_code": 201, "data": {"id": "79687ca6-b018-4cc6-b369-5cf92fc511a5"}}
    Offer response: {"status_code": 200, "data": [{"id": "...", "price": ..., "items_in_stock": ...}]
}
```

### 🧩 Simple Facade Example

```python
sdk = MyApiSDK(
    bearer="YOUR_BEARER_TOKEN"  # Get token from https://python.exercise.applifting.cz/assignment/sdk/
)

product = Product(
    id=uuid4(),
    name="Example Product",
    description="Example Description"
)

register_response = await sdk.product.register_product(product)
print("Register response:", register_response)

offer_response = await sdk.offer.get_offer(product)
print("Offer response:", offer_response)

await sdk.aclose()
```

## 🌱 Development

Install dependencies and run development commands:

```bash
    make dev
    make lint
    make type-check
    make test
    make format
```

## ✅ Acknowledgments

* **Token Cache Options**:

    * In-memory cache (runtime only)
    * SQLite cache (persistent, no extra dependencies)
* **Pluggable Architecture**:

    * Token caching: `memory_cache_adapter.py`, `sqlite_cache_adapter.py` via `cache_interface.py`
    * HTTP client logic: `http_x_client_adapter.py` via `http_client_interface.py`
* **User-defined Implementations**:

    * Override URL endpoints, token caching, and HTTP logic via Dependency Injection interfaces.

## 🛠️ Future Development

* Define custom exceptions for SDK domain
* Configurable logging system
* Retry mechanism support
* Extended test coverage with integration tests

---

## 📄 License

MIT License © Bartolomej Elias

---

> 🎨 Contributions and suggestions welcome!