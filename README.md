## gknet archive

This repository contains data, code, and related artefacts supporting the following publication:

```
"Heat flux for semi-local machine-learning potentials"
Marcel F. Langer, Florian Knoop, Christian Carbogno, Matthias Scheffler, and Matthias Rupp
arXiv: TBD
doi: TBD
```

The repository is organised as follows:

- `infrastructure/`: project-specific software
- `results/`: raw data used to produce figures and tables
- `plots/`: figures, tables, and the scripts used to generate them
- `dft/`: input files and trajectories for training data and other first-principles calculations
- `train/`: model training input files, losses, logs
- `run/`: input files and related data for production runs with the MLP, including phonons, VDOS, GK, ...
- `generate/`: scripts used to generate this repository.

Subfolders contain additional `README.md` files detailing dependencies and other relevant information.

The primary objective of this repository is to clarify the workflows and methods used to obtain the results in the publication. Not all code is intended to be used in unrelated settings, or can be expected to execute directly.

If your goal is to build on the methods developed in the paper, we recommended to instead take a look at [`glp`](https://github.com/sirmarcel/glp), which presents a generic implementation of the heat flux in `jax`. Full `jax`-based workflows to run Green-Kubo simulations are also in development.

The training trajectories are also available on the NOMAD repository under DOI [10.17172/NOMAD/2023.03.24-2](https://doi.org/10.17172/NOMAD/2023.03.24-2).

For any further questions, feel free to contact `mail@marcel.science`, `@marceldotsci` on twitter, or `@marcel@sigmoid.social`.

### versions

- `v1.0`: version for the initial arXiv upload (archived at [doi:10.5281/zenodo.7767432](https://doi.org/10.5281/zenodo.7767432))
