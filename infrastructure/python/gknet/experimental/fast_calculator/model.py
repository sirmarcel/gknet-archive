import torch

import schnetpack as spk
from gknet.engine import Stateful

from gknet import keys

from .schnet import SchNet

defaults_representation = {
    "cutoff": 5.0,
    "n_interactions": 2,
    "n_atom_basis": 128,
    "n_filters": 128,
    "trainable_gaussians": False,
    "normalize_filter": False,
}

defaults_atomwise = {"mean": 0.0, "stddev": 1.0, "n_layers": 2, "n_neurons": None}


class Model(Stateful):
    # Model should always be assumed to be a) on CPU, b) not parallel, c) not have stress,
    # if this is needed, it needs to be done *to* the model

    kind = "model"

    def __init__(self, representation={}, atomwise={}):

        self.config_representation = {
            **defaults_representation,
            **representation,
        }
        representation = SchNet(**self.config_representation)

        # option is no longer supported since it appears to be pointless
        if "symmetrize_stress" in atomwise:
            del atomwise["symmetrize_stress"]

        self.config_atomwise = {
            **{"n_in": representation.n_atom_basis},
            **defaults_atomwise,
            **atomwise,
        }

        atomwise = get_atomwise(**self.config_atomwise)

        self.model = spk.atomistic.model.AtomisticModel(representation, [atomwise])

        self.disable_stress()

        self._training = False
        self._return_pairwise = False

    def _restore(self, state):
        self.model.load_state_dict(state)

    def _get_config(self):
        return {
            "representation": self.config_representation,
            "atomwise": self.config_atomwise,
        }

    def _get_state(self):
        if self.parallel:
            return self.model.module.state_dict()
        else:
            return self.model.state_dict()

    def enable_stress(self):
        enable_property(self.model, keys.stress)
        self.model.requires_stress = True
        if self.parallel:
            self.model.module.requires_stress = True
        self._stress = True

    def enable_stresses(self):
        self.enable_stress()
        enable_property(self.model, keys.stresses)

    def disable_stress(self):
        disable_property(self.model, keys.stress)
        self.model.requires_stress = False
        self.disable_stresses()
        self._stress = False

    def disable_stresses(self):
        disable_property(self.model, keys.stresses)

    @property
    def parallel(self):
        return True if isinstance(self.model, torch.nn.DataParallel) else False

    @parallel.setter
    def parallel(self, make_parallel):
        if make_parallel and not self.parallel:
            self.model = torch.nn.DataParallel(self.model)

    @property
    def stress(self):
        return self._stress

    @stress.setter
    def stress(self, predict_stress):
        if predict_stress and not self._stress:
            self.enable_stress()

    def to(self, device):
        self.model.to(device)

    @property
    def return_pairwise(self):
        return self._return_pairwise

    @return_pairwise.setter
    def return_pairwise(self, enable_pairwise):
        if self.parallel:
            self.model.module.representation.return_pairwise = enable_pairwise
        else:
            self.model.representation.return_pairwise = enable_pairwise

        self._return_pairwise = enable_pairwise

    @property
    def training(self):
        return self._training

    @training.setter
    def training(self, enable_training):
        if self.parallel:
            self.model.module.representation.training = enable_training
            output_modules = self.model.module.output_modules
        else:
            self.model.representation.training = enable_training
            output_modules = self.model.output_modules

        for module in output_modules:
            module.training = enable_training

        self._training = enable_training


def get_atomwise(n_in, mean, stddev, n_layers, n_neurons):

    return spk.atomistic.Atomwise(
        n_in=n_in,
        mean=torch.tensor(mean),
        stddev=torch.tensor(stddev),
        n_layers=n_layers,
        n_neurons=n_neurons,
        negative_dr=True,
        property=keys.energy,
        derivative=keys.forces,
        stress=None,
        # stresses=None,
        contributions=keys.energies,
    )


def enable_property(model, prop):

    # check for parallel model
    if hasattr(model, "module"):
        output_modules = model.module.output_modules
    else:
        output_modules = model.output_modules

    for module in output_modules:
        if hasattr(module, prop):
            setattr(module, prop, prop)

    return model


def disable_property(model, prop):

    # check for parallel model
    if hasattr(model, "module"):
        output_modules = model.module.output_modules
    else:
        output_modules = model.output_modules

    for module in output_modules:
        if hasattr(module, prop):
            setattr(module, prop, None)

    return model
