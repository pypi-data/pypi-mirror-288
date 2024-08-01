# for publish new version
python3 -m pip install twine

python3 -m pip install --upgrade twine

python3 -m pip install -e .

python3 -m build

twine upload --repository modulare dist/*
