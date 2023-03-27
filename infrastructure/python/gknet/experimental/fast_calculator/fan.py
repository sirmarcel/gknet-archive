import torch
from torch.autograd import grad
import numpy as np


from .comms import comms


def compute_fan_virials(
    ref, energies, r_ij, idx, hatr_ij, volume, reporter, transpose_idx, mask, full=False
):

    n = idx.shape[0]
    idx = idx.astype(int)
    ref = ref.cpu().numpy()

    reporter.tick("got transpose")

    jacobian = []
    jacobian_transpose = []
    for i in range(n):
        reporter.tick(f"jacobian atom {i}")
        dui_drjk = (
            grad(
                energies[:, i],
                r_ij,
                retain_graph=True,
            )[0]
            .detach()
            .squeeze()
        )
        dui_dvecrjk = dui_drjk.unsqueeze(-1) * hatr_ij
        dui_drkj = dui_drjk[transpose_idx[:, :, 0], transpose_idx[:, :, 1]] * mask
        dui_dvecrkj = -1.0 * dui_drkj.unsqueeze(-1) * hatr_ij

        jacobian.append(dui_dvecrjk.cpu().numpy())
        jacobian_transpose.append(dui_dvecrkj.cpu().numpy())

    jacobian = np.array(jacobian)

    fan_virials = np.zeros((n, 3, 3))
    fan_virials_transpose = np.zeros((n, 3, 3))
    fan_virials_symm = np.zeros((n, 3, 3))
    for j in range(n):  # j: virial for atom j
        reporter.tick(f"virial {j}")
        for ii, i in enumerate(idx[j]):  # the ii-th neighbor of j is i
            if i == -1:  # not an actual neighbor, just padding
                continue
            jj = transpose_idx[j, ii][1]  # the jj-th neighbor of i is j
            # recap: virial j, neighbor i are the "real" indices,
            # relative indeices are: ii in N(j) and jj in N(i)

            fan_virials[j] += ref[j, i, :, None] * jacobian[i, i, jj][None, :]
            fan_virials_transpose[j] += ref[j, i, :, None] * jacobian[i, j, ii][None, :]
            fan_virials_symm[j] += 0.5 * (
                ref[j, i, :, None] * jacobian[i, i, jj][None, :]
                + ref[j, i, :, None] * jacobian[i, j, ii][None, :]
            )

    fan_virials_mpnn = np.sum(
        ref[:, :, :, None] * np.sum(jacobian - jacobian_transpose, axis=2)[:, :, None, :],
        axis=0,
    )

    results = {
        "fan_virials": fan_virials / volume,
        "fan_virials_transpose": fan_virials_transpose / volume,
        "fan_virials_symm": fan_virials_symm / volume,
        "fan_virials_mpnn": fan_virials_mpnn / volume,
    }

    return results
