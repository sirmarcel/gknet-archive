cd ..
rm -r results infrastructure run train plots dft

cd generate
sh copy_infrastructure.sh
python copy_dft.py
python copy_plots.py
python copy_results.py
python copy_run.py
python copy_train.py
python cleanup.py