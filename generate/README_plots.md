## outputs

This folder collects the scripts to generate all figures in the manuscript, as well as PNG previews.

The `tbx` subfolder collects common routines for plotting. It is expected to be in the `PYTHONPATH` for the scripts to run. If you intend to run anything in this folder, you additionally must update `tbx/__init__.py` such that `results` points to the `results/` folder in this repository, and redefine `img` to point to some folder where you would like the PDF version of figures to render to.

Dependencies of the scripts are: `numpy scipy matplotlib seaborn xarray`. Used versions:

```
Package              Version    
-------------------- -----------
matplotlib           3.5.
numpy                1.20.2
scipy                1.7.3
seaborn              0.11.2
xarray               0.20.2
```

with `python 3.7.13`.
