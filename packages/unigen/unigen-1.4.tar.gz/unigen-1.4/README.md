# Unigen

Wrapper around python's mutagen package which provides a single interface to interact with audio metadata of various formats

## Dependencies installation
For installing dependencies:
`pip install -r requirements.txt`

To add a new dependency, add it to `setup.py` and `requirements.in`. Then:

```
pip install pip-tools
pip-compile --upgrade
pip-sync
```
This will update `requirements.txt`
