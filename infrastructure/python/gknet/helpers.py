import torch
from vibes.helpers import talk as _talk


def talk(msg, **kwargs):
    """wrapper for `utils.talk` with prefix"""
    return _talk(msg, prefix="gknet", **kwargs)


def guess_device_settings(device=None, parallel=None):
    if device is None:
        if torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"

    if parallel is None:
        if torch.cuda.device_count() > 1 and device == "cuda":
            parallel = True
        else:
            parallel = False

    return device, parallel


def stress_to_voigt(stress):
    symmetrised = 0.5 * (stress + stress.transpose(1, 2))
    return symmetrised[:, [0, 1, 2, 1, 0, 0], [0, 1, 2, 2, 2, 1]]

def open_file(file):
    from pathlib import Path

    file = Path(file)
    if file.suffix in [".yml", ".yaml"]:
        from gknet import from_config
        return from_config(file)
    elif file.suffix == ".torch":
        from gknet import load
        return load(gknet)
    else:
        raise ValueError(f"do not know how to open extension {file.suffix}")
