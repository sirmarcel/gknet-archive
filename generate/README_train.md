## train

This folder contains the input files and losses for the models used in the paper.

Subfolders correspond to cutoff, and then the number of message-passing steps. Inside each such subfolder, there are `.yml` files specifying model architecture and training procedure, and `.in` files with information needed for submission with slurm; the `predict*.in` files contain instructions about datasets to use for evaluation. Losses for different datasets can be found in the `predict/` sufolder. Final trained model and the end of the training log files in the `train/` subfolder.

Python scripts at the cutoff level document how datasets were generated. They are not expected to be executable, as they refer to system-specific paths. Names of datasets correspond to the ones in the `dft` folder.

The "production" model used in most cases can be found in `cu_5.0/m2/`. (The internal name for this model was `ccl_zro_t96/cu_5.0_e_inpt_4387/train_n2_s1`, used in various input files and scripts.)

Additionally, `heat_flux_timings/` contains the script used to compute timings for the heat flux.
