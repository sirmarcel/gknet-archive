from gknet.experimental.fast_calculator import fastCalculator

from ase.calculators.socketio import SocketClient
from ase.io import read

atoms = read("geometry.in", 0, "aims")

calc = fastCalculator("../best_model.torch", stress=True, device="cuda:1")

atoms.set_calculator(calc)

# Create client

port = 10200
host = "localhost"
client = SocketClient(host=host, port=port)
print("running...")
client.run(atoms, use_stress=True)
