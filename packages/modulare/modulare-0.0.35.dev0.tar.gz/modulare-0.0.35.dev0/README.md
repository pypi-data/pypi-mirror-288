# install pip requirements
    pip install -e .

python3 -m build

twine upload --repository modulare dist/*

pip uninstall modulare

pip install modulare