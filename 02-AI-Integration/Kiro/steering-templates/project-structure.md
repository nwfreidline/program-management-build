# Project Folder Standards

All projects follow a consistent structure optimized for portability and team sharing.

## Folder Layout

```
<Project Name>/
├── <App Name>.pyw           # Main launcher (if it's a runnable app)
├── README.md                # Setup & usage instructions
├── _app/                    # Application internals (source code, requirements.txt)
│   ├── requirements.txt     # Python dependencies
│   ├── <source files>
│   └── <modules>/
├── _dev/                    # Dev/test tools (excluded from shared packages)
├── _data/                   # Personal/transient data (excluded from shared packages)
└── config/                  # User-facing configuration (if applicable)
    └── settings.json
```

## Rules

1. **Top-level should be clean.** User sees: the launcher (.pyw), the README, and config/.
2. **Apps use .pyw format.** No console window on Windows.
3. **README.md is always present.** Every project explains setup and usage.
4. **requirements.txt lives in `_app/`.** README references `pip install -r _app\requirements.txt`.
5. **`_dev/` for development artifacts.** Excluded from distribution.
6. **`_data/` for personal/transient data.** Excluded from distribution.
7. **No hardcoded personal paths in source code.** Use `Path(__file__).parent` patterns.
