import torch
from torch.autograd import grad
import numpy as np


def compute_barycenter(reference, energies, positions, forces, velocities, volume):

    potential_barycenter = torch.sum(reference.unsqueeze(0) * energies, axis=1)
    dot_potential_barycenter = torch.zeros(3)
    for alpha in range(3):
        tmp = (
            grad(potential_barycenter[:, alpha], positions, retain_graph=True)[0]
            .detach()
            .squeeze()
        )
        dot_potential_barycenter[alpha] = torch.sum(tmp * velocities)

    dot_kinetic_barycenter = torch.sum(
        reference * torch.sum(forces * velocities, axis=1).unsqueeze(-1), axis=0
    )

    dot_potential_barycenter = dot_potential_barycenter.cpu().numpy() / volume
    dot_kinetic_barycenter = dot_kinetic_barycenter.cpu().numpy() / volume

    return (
        dot_potential_barycenter + dot_kinetic_barycenter,
        dot_potential_barycenter,
        dot_kinetic_barycenter,
    )
