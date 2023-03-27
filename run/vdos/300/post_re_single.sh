cd $2/recompute
gknet out hf --other_virials $1/ -o heat_flux_$1.nc --nofreq ../md/trajectory/
cd ../../