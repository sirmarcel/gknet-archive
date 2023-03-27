cd ..
mkdir infrastructure

cp generate/README_infrastructure.md infrastructure/README.md

cd infrastructure/
rm -rf bin
rm -rf python
cp -r ../../../gknet/infrastructure/* .
cd python
rm -r poetry.lock gknet.egg-info/
cd gknet/experimental/
rm -r fixed_skin_calculator/
rm -r fast_calculator_2/
rm -r fast_calculator_1.py
cd ..
cd ../tests/
rm -r __pycache__/
