import numpy as np

from ase.calculators.calculator import Calculator as aseCalculator

from .calculator import gknetCalculator


class gknetEnsembleCalculator(aseCalculator):

    implemented_properties = [
        "energy",
        "forces",
        "stress",
        "stresses",
        "energies",
    ]

    def __init__(
        self,
        models,
        device=None,
        stress=False,
        energies=False,
        virials=False,
        virials_reference=None,
        **kwargs,
    ):
        aseCalculator.__init__(self, **kwargs)

        self.calcs = [
            gknetCalculator(
                model,
                device=device,
                stress=stress,
                energies=energies,
                virials=virials,
                virials_reference=virials_reference,
            )
            for model in models
        ]

        self.energies = energies
        self.stress = stress
        self.virials = virials

    @property
    def stress(self):
        return self.calc[0].stress

    @stress.setter
    def stress(self, compute_stress):
        for calc in self.calcs:
            calc.stress = compute_stress

    @property
    def virials(self):
        return self.calcs[0].virials

    @virials.setter
    def virials(self, compute_virials):
        for calc in self.calcs:
            calc.virials = compute_virials

    def calculate(self, atoms=None, properties=None, system_changes=None):
        aseCalculator.calculate(self, atoms)

        raw_results = [calc.calculate(atoms=self.atoms) for calc in self.calcs]

        full_results = {}
        for key in raw_results[0].keys():
            full_results[key] = np.array([r[key] for r in raw_results])

        results = {}
        for prop, values in full_results.items():
            results[prop] = values.mean(axis=0)
            results[f"{prop}_std"] = values.std(axis=0)
            results[f"{prop}_all"] = values

        self.results = results

        return results
