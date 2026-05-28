# Installation

This guide covers all the ways to install Pali.

## Requirements

- Python 2.7+ or Python 3.4+
- pip (optional, but recommended)

## Install from PyPI (Recommended)

The easiest way to install Pali is using pip:

```bash
pip install pali
```

## Install from Source

If you prefer to install from source or want the latest development version:

### Using git

```bash
git clone https://github.com/gitvipin/pali.git
cd pali
python setup.py install
```

### Using setup.py directly

```bash
wget https://github.com/gitvipin/pali/archive/master.zip
unzip master.zip
cd pali-master
python setup.py install
```

## Verify Installation

To verify that Pali was installed correctly, open a Python shell and import it:

```python
>>> import pali
>>> print(pali.__version__)
0.0.6
```

If you see the version number without errors, Pali is installed correctly!

## Next Steps

Once installed, check out:
- [Quick Start](quick-start.md) - Get running with your first example
- [Thread Pool](../guide/thread-pool.md) - Learn the core concepts

## Troubleshooting

### ImportError: No module named pali

Make sure Pali is installed by running `pip install pali` or `python setup.py install` from the source directory.

### Python version issues

Pali supports Python 2.7+ and 3.4+. If you're using an older version, please upgrade Python first.

```bash
python --version
```

### Can't install from source

Make sure you have the required build tools:

**On Ubuntu/Debian:**
```bash
sudo apt-get install python-dev python-setuptools
```

**On macOS:**
```bash
brew install python
```

**On Windows:**
Download Python from [python.org](https://www.python.org/downloads/) and run the installer.

## Getting Help

If you encounter any issues during installation, please:
1. Check the [FAQ](../guide/faq.md) (coming soon)
2. Open an issue on [GitHub](https://github.com/gitvipin/pali/issues)
