cd $2/recompute
gknet out gk --freq 3.0 -o gk_$1.nc heat_flux_$1.nc
cd ../../