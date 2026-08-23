# yads-common

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Language](https://img.shields.io/badge/language-Python-informational.svg) ![AI generated](https://img.shields.io/badge/AI-generated-8A2BE2.svg)

Shared GUI and utility library used across [YADS](https://github.com/MrMarco74/yads) tooling — dark-mode detection, ANSI-to-HTML log formatting, and other small PySide6 helpers.

## Installation

```bash
pip install git+https://github.com/MrMarco74/yads-common.git
```

## Usage

```python
from yads_common.gui import detect_system_dark_mode

if detect_system_dark_mode():
    ...
```

## License

MIT — see [LICENSE](LICENSE).
