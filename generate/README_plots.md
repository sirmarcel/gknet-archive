## outputs

This folder collects the scripts to generate all figures in the manuscript, as well as PNG previews.

The `tbx` subfolder collects common routines for plotting. It is expected to be in the `PYTHONPATH` for the scripts to run. If you intend to run anything in this folder, you additionally must update `tbx/__init__.py` such that `results` points to the `results/` folder in this repository, and redefine `img` to point to some folder where you would like the PDF version of figures to render to.

Dependencies of the scripts are: `numpy scipy matplotlib seaborn xarray netCDF4`. Used versions:

```
Package         Version
--------------- --------
cftime          1.6.2
contourpy       1.0.7
cycler          0.11.0
fonttools       4.39.2
kiwisolver      1.4.4
matplotlib      3.7.1
netCDF4         1.6.3
numpy           1.24.2
packaging       23.0
pandas          1.5.3
Pillow          9.4.0
pip             22.0.4
pyparsing       3.0.9
python-dateutil 2.8.2
pytz            2023.2
scipy           1.10.1
seaborn         0.12.2
setuptools      58.1.0
six             1.16.0
xarray          2023.3.0
```

with `python 3.10.4`.
