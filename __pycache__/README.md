# 📁 `__pycache__/` — Python Bytecode Cache

This folder contains auto-generated `.pyc` files compiled by Python to speed up module loading and execution. These files are created automatically when Python scripts are run and are specific to the interpreter version.

---

## 📦 Contents

| File                              | Description                                                       |
|-----------------------------------|-------------------------------------------------------------------|
| `fetcher.cpython-313.pyc`         | Compiled bytecode from `fetcher.py` for faster execution          |
| `timeseries_scaler.cpython-313.pyc` | Compiled bytecode from `timeseries_scaler.py` used in scaling pipeline |

---

## ⚠️ Notes

- These files are **not meant to be edited manually**.
- They are **safe to delete** — Python will regenerate them as needed.
- It is recommended to **exclude this folder from version control** using `.gitignore`:

```bash
__pycache__/
*.pyc

---

## ⚖️ License

This project is proprietary. All rights reserved © 2025 Gerrald Andersen.  
No part of this repository may be copied, modified, reused, or redistributed without explicit written permission.

![License: Proprietary](https://img.shields.io/badge/license-Proprietary-red.svg)
