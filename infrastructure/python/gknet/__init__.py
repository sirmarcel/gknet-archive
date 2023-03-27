from cmlkit.engine import _from_config
from .engine import load

from .model import Model
from .data import Data
from .loss import MSE, SMSE
from .train import components as train_components
from .calculator import gknetCalculator
from .ensemble_calculator import gknetEnsembleCalculator

components = [Model, Data, MSE, SMSE, *train_components]


def from_config(config):
    return _from_config(
        config,
        classes={component.kind: component for component in components}
    )
