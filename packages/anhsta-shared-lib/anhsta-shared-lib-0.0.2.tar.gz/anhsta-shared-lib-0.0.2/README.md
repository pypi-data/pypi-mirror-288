# anhsta-shared-lib
 
python setup.py build_ext --inplace

python setup.py sdist bdist_wheel

python -m twine upload dist/*
