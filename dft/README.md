## dft

Everything related to first-principles calculations for the presented work.

### versions

We used FHI-aims version `200926` on the `raven` HPC system at the MPCDF. All calculations were submitted using `FHI-vibes`

Loaded libraries during compilation:
```
intel/19.1.2
impi/2019.8 
```

`initial_cache.cmake`:

```
set(CMAKE_Fortran_COMPILER "mpiifort" CACHE STRING "")
set(CMAKE_Fortran_FLAGS "-O3 -ip -fp-model precise" CACHE STRING "")

###############
# C,C++ Flags #
###############

set(CMAKE_C_COMPILER "mpiicc" CACHE STRING "")
set(CMAKE_C_FLAGS "-O3 -ip -fp-model precise -std=gnu99" CACHE STRING "")

set(CMAKE_CXX_COMPILER "mpiicpc" CACHE STRING "")
set(CMAKE_CXX_FLAGS "-O3 -ip -fp-model precise" CACHE STRING "")

set(INC_PATHS "$ENV{INTEL_HOME}/include $ENV{I_MPI_ROOT}/include64" CACHE STRING "")
set(LIB_PATHS "$ENV{I_MPI_ROOT}/lib64 $ENV{MKLROOT}/lib/intel64 $ENV{CUDA_HOME}/lib64" CACHE STRING "")

set(LIBS "mkl_intel_lp64 mkl_sequential mkl_core mkl_blacs_intelmpi_lp64 mkl_scalapack_lp64" CACHE STRING "")

###############
#   Extras    #
###############
set(USE_C_FILES   ON CACHE BOOL "")
set(USE_CXX_FILES ON CACHE BOOL "")

set(USE_MPI       ON CACHE BOOL "")
set(USE_SCALAPACK ON CACHE BOOL "")

set(USE_SPGLIB    ON CACHE BOOL "ON")
set(USE_iPI       ON CACHE BOOL "ON")
set(ELPA2_KERNEL "AVX512" CACHE BOOL "")
```

### overall settings

Overall settings were chosen to be as similar as feasible with the previous work by Carbogno et al. In particular, we choose a custom `cc_light` basis set, which includes an additional basis function for oxygen and is otherwise identical to `light`. Basis sets can be found in `train/relaxation_symmetric/relaxation/basissets`.

### training data

Training data can be found in `train/`. Naming indicates that the "inhomogeneous" Berendsen barostat/thermostat implemented in `ase` was used. The remainder of folder names are `inpt_N_0_T_Yps_Zps` where `N` is a shorthand index, `T` indicates the target temperature, `Y` the duration of the trajectory and `Z` the time-constant of the barostat/thermostat. Trajectories with `N=3,4,7,8` were used in this work, the remainder are published to aid others.

`relaxation` and `relaxation_symmetric` are not used for training, but are used to obtain starting geometries for the training runs.

### rerun

`rerun/300K` contains a re-run (i.e. simply running a new MD from the same initial configuration) of the trajectories obtained for 300K from the NOMAD repository (https://doi.org/10.17172/NOMAD/2017.04.13-1), since the uploaded trajectories did not contain virials required to compute the heat flux and contain drift that makes it inconvenient to evaluate the vibrational density of states. These trajectories are the basis for the VDOS plots in the manuscript.

### phonons

Phonon calculations were run as follows: First, relaxations were performed with different k-grids and basis sets in `relaxation`. Having checked that 12x12x12 is sufficient, the resulting geometries were used as primitive cells for phonopy calculations. Calculations are named as `sX_kY_BASISSET`, where `X` denotes the `X x X x X` (or equivalent) supercell (`s2` is 96 atoms, `s3` 324, and `s4` 768) and `Y` the k-grid.

For the tetragonal phase, some special care had to be taken to avoid numerical issues with phonopy: in place of the 12-atom convetional cell used in the remainder of this work, a 6-atom primitive cell with a different orientation is used. To avoid issues with FHI-aims, slightly different settings were also used; they are documented in the input files.
