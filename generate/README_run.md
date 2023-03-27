## run

This folder collects the workflows used to generate most results in the paper. All subfolders expect to be in a folder that contains a `best_model.torch` file, the files emitted by the training procedure, which can be found in the `train/` folder.

The workflows are:

- `*_production` contains input files for the "production" GK runs, i.e. 1ns and 1500 atoms.
- `*_variations` contains inputs for size, time, and settings convergence, as well as different heat flux formulations.
- `phonons`: compute phonon band structures
- `vdos`: running short MD trajectories on starting geometries that were also used for DFT to obtain the vibrational density of states
- `heat`: a long NPT run with `i-pi` to produce the "volume vs temperature" figure in the supplement

For the Green-Kubo workflows, the general order of operations is:

- Submit `nvt/` MD with `vibes submit md`
- Post-process result with `main_prep.sh` which will extract starting geometries from NVT
- Submit MD in the folders 00 ... 10
- Post-process MD with `main_post.sh`
- Submit re-computation (of heat flux) by copying `re_X.in` to each 00 ... 10 and running `gknet submit recompute re_X.in`
- Once that is done, run various post-processing scripts to obtain heat flux and GK results.

Post-processing of heat flux proceeds in two stages: First, the heat flux is extracted into `heat_flux_X.nc` datasets. Then, the HFACF (with various filtering approaches) is computed and put into `gk_X_modifiers.nc` datasets. These datasets are the basis for the results collected in `data/`.


### environment

All calculations were run on the `talos` HPC system at the MPCDF facility, using `python 3.7.10`.

Repositories and respective commits for core packets are listed below:

```
schnetpack: github.com:sirmarcel/schnetpack.git, master@5dd3d3f28506121cccc8da7d28b560840fd78ad1
stepson: gitlab.com:sirmarcel/stepson.git, main@8e565442b1e744df2f3bc682950273c9647704dd
fhi-vibes: gitlab.com:sirmarcel/vibes.git, master@6f39a407a5f4668eab326c9b422a5f168f6f66a1
i-pi: github.com/i-pi/i-pi.git master@b7cf899ff165a2eb844b929b0597074af28dadc8

```

Other packages were used as released, here is the output of `pip list`

```
Package               Version             Location
--------------------- ------------------- ----------------------------------------------------
apipkg                1.5
appdirs               1.4.4
ase                   3.21.1
atomicwrites          1.4.0
attrs                 19.3.0
backcall              0.2.0
black                 19.10b0
CacheControl          0.12.6
cached-property       1.5.2
cachy                 0.3.0
certifi               2020.12.5
cffi                  1.14.5
cftime                1.4.1
chardet               4.0.0
cleo                  0.8.1
click                 7.1.2
click-aliases         1.0.1
click-completion      0.5.2
clikit                0.6.2
cloudpickle           1.6.0
cmlkit                2.0.0a23
coverage              5.5
crashtest             0.3.1
cryptography          3.4.6
cycler                0.10.0
dask                  2021.4.1
decorator             4.4.2
dill                  0.2.9
distlib               0.3.1
execnet               1.8.0
fhi-vibes             1.1.0a0             /talos/u/mlang/gknet/software/gknet-2-vibes
filelock              3.0.12
flake8                3.9.1
flake8-bugbear        19.8.0
flake8-comprehensions 3.4.0
fsspec                2021.4.0
future                0.18.2
gknet                 0.1.0
graphviz              0.16
h5py                  3.1.0
html5lib              1.1
htmlmin               0.1.12
hyperopt              0.1.2
idna                  2.10
importlib-metadata    4.0.1
ipykernel             5.5.3
ipython               7.22.0
ipython-genutils      0.2.0
isort                 4.3.21
jconfigparser         0.1.3
jedi                  0.18.0
jeepney               0.6.0
Jinja2                2.11.3
joblib                1.0.1
jsmin                 2.2.2
jupyter-client        6.1.12
jupyter-core          4.7.1
keyring               21.8.0
kiwisolver            1.3.1
livereload            2.6.3
llvmlite              0.36.0
locket                0.2.1
lockfile              0.12.2
lunr                  0.5.8
lz                    0.11.0
Markdown              3.3.4
MarkupSafe            1.1.1
matplotlib            3.3.4
mccabe                0.6.1
memoir                0.0.3
mkdocs                1.1.2
mkdocs-material       4.6.3
mkdocs-minify-plugin  0.2.3
mkl-fft               1.3.0
mkl-random            1.1.1
mkl-service           2.3.0
more-itertools        8.7.0
msgpack               1.0.2
mypy                  0.812
mypy-extensions       0.4.3
netCDF4               1.5.6
networkx              2.5
nltk                  3.6.2
numba                 0.53.1
numexpr               2.7.3
numpy                 1.19.2
packaging             20.9
pandas                1.1.5
paradigm              0.6.2
parso                 0.8.2
partd                 1.2.0
pastel                0.2.1
pathspec              0.8.1
Pebble                4.3.10
pexpect               4.8.0
phonopy               2.8.1
pickleshare           0.7.5
Pillow                8.2.0
pip                   21.0.1
pkginfo               1.7.0
pluggy                0.13.1
poetry                1.1.5
poetry-core           1.0.2
prompt-toolkit        3.0.18
protobuf              3.15.6
ptyprocess            0.7.0
py                    1.10.0
pycodestyle           2.7.0
pycparser             2.20
pyflakes              2.3.1
Pygments              2.8.1
pylev                 1.3.0
pymdown-extensions    6.3
pymongo               3.11.3
pyparsing             2.4.7
pytest                4.6.11
pytest-cov            2.11.1
pytest-forked         1.3.0
pytest-xdist          1.34.0
python-dateutil       2.8.1
pytz                  2021.1
PyYAML                5.4.1
pyzmq                 22.0.3
regex                 2021.4.4
reprit                0.4.0
requests              2.25.1
requests-toolbelt     0.9.1
rope                  0.14.0
schnetpack            0.4.0rc0            /talos/u/mlang/gknet/software/gknet-2-schnetpack/src
scipy                 1.6.2
seaborn               0.11.1
SecretStorage         3.3.1
seekpath              1.9.7
setuptools            52.0.0.post20210125
shellingham           1.4.0
six                   1.15.0
son                   0.4.1
spglib                1.16.1
stepson               0.1.0
tables                3.6.1
tensorboardX          2.1
toml                  0.10.2
tomlkit               0.7.0
toolz                 0.11.1
torch                 1.8.0+cu111
torchvision           0.9.0+cu111
tornado               6.1
tqdm                  4.60.0
traitlets             5.0.5
typed-ast             1.4.3
typing-extensions     3.7.4.3
ujson                 4.0.2
urllib3               1.26.4
virtualenv            20.4.3
wcwidth               0.2.5
webencodings          0.5.1
wheel                 0.36.2
xarray                0.16.2
zipp                  3.4.1
```

Here is the output of `module list`

```
Currently Loaded Modulefiles:
 1) anaconda/3/2020.02   3) git-lfs/3.3   5) intel/19.1.3   7) mkl/2020.2   9) pytorch/gpu-cuda-11.0/1.8.0  
 2) git/2.39             4) gcc/10        6) impi/2019.9    8) cuda/11.0   
```
