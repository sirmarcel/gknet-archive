## infrastructure

This folder contains the infrastructure required for the `train/` and `run/` subfolders.

While this is not intended to serve as infrastructure for unrelated projects, we nevertheless provide installation instructions and an outline of functionality.

This package implements additional functionality on top of `schnetpack` (version 1) and `FHI-vibes`, in particular:

- de/serialisation infrastructure based on `cmlkit` (the functionality used from `cmlkit` has been extracted into [`specable`](https://github.com/sirmarcel/specable))
- training wrapper for `schnetpack` with pre-processing of training data (significant speedups as neighborlist recomputation is avoided)
- `slurm` support, including resumable training, via `FHI-vibes`
- `fastCalculator`, a `vibes`-compatible calculator with neighborlist caching and support for different formulations of the heat flux
- `UnfoldedHeatFluxCalculator`, which implements the "unfolded" heat flux introduced in the publication
- `Recompute` task for the `FHI-vibes` `slurm` system, which allows the recomputation of existing trajectories
- `gknet` CLI that integrates `stepson`, can run and submit tasks mentioned above, performs various GK-related post-processing tasks

Some of this functionality has been extracted into [`schnetkit`](https://github.com/sirmarcel/schnetkit/).

As most of this infrastructure is built for an obsolete version of `schnetpack`, which was recently rewritten, it must be considered deprecated. Work is underway to develop a more modular and generic Green-Kubo infrastructure for `jax`, which no longer depends on a particular machine learning potential.

Please see [`glp`](https://github.com/sirmarcel/glp) or get in touch via twitter (`@marceldotsci`) or e-mail (`mail@marcel.science`) for questions on this -- the best is yet to come!


### installation

For historical reasons, main dependencies are not declared and must instead be installed manually.
The expected dependencies are: `fhi-vibes cmlkit stepson ase schnetpack`. Exact versions can be found in the `run/` readme.

Once these dependencies are available:

```
cd python
pip install .
```

This will make the `gknet` package importable and add the `gknet` command to `PATH`.

### usage

Main usage of this code is via input files and the `gknet` CLI.

Examples of such input files are found in the `train/` and `run/` folders.

### good to know

Note that `transpose_derivatives=True` is required to yield the correct local heat flux in the `M=1` case. The reason for this is rather subtle: in order to be efficient in the implementation, we require the `j` index (i.e. the neighbouring atom) to be the first index. In the standard neighborlist format of `schnetpack`, the central atom `i` is first. This flag makes sure that this is "transposed" correctly.
