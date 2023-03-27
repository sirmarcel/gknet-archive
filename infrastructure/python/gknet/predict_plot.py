import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def fig_and_ax(figsize=None):
    if figsize:
        fig = plt.figure(figsize=figsize, dpi=200)
    else:
        fig = plt.figure(figsize=(8, 8), dpi=200)
    ax = plt.axes()
    return fig, ax


def rmse(true, pred):
    return np.sqrt(np.mean((true - pred) ** 2))


def mae(true, pred):
    return np.mean(np.fabs(true - pred))


def maxae(true, pred):
    return np.max(np.fabs(true - pred))


def r2(true, pred):

    mean = np.mean(true)
    sum_of_squares = np.sum((true - mean) ** 2)
    sum_of_residuals = np.sum((true - pred) ** 2)

    return 1.0 - (sum_of_residuals / sum_of_squares)


def simple_scatterplot(
    true,
    pred,
    ax=None,
    labeltrue='Ground truth (1000 * energy unit)',
    labelpred='Prediction (1000 * energy unit)',
    plotrange=None,
    precision=4,
):
    # drop NaNs if they exist in true values
    pred = pred[~np.isnan(true)]
    true = true[~np.isnan(true)]

    if ax is None:
        fig, ax = fig_and_ax()

    if plotrange is not None:
        rangemin = plotrange[0]
        rangemax = plotrange[1]
    else:
        rangemin = np.min(true)
        rangemax = np.max(true)
        spread = rangemax - rangemin
        rangemin, rangemax = rangemin - spread * 0.05, rangemax + spread * 0.05

    # plot diagonal
    ax.plot(
        [rangemin, rangemax],
        [rangemin, rangemax],
        marker='',
        color='darkgray',
        linestyle='dashed',
        linewidth=1,
    )

    # set range
    ax.set_xlim(rangemin, rangemax)
    ax.set_ylim(rangemin, rangemax)

    # scatterplot!
    ax.scatter(true, pred, marker='o', alpha=0.8)

    # catch everything out of the range and display as arrows
    # plot markers for predictions outside of plot range
    indfailneg = [i for (i, p) in zip(range(len(pred)), pred) if p < rangemin]
    indfailpos = [i for (i, p) in zip(range(len(pred)), pred) if p > rangemax]
    indfail = indfailneg + indfailpos

    if len(indfail) > 0:
        print(
            'Indices of predictions above scatter plot range: {}\n'.format(
                indfailpos if len(indfailpos) > 0 else 'None'
            )
        )
        print(
            'Indices of predictions below scatter plot range: {}\n'.format(
                indfailneg if len(indfailneg) > 0 else 'None'
            )
        )

        if len(indfailneg) > 0:
            ax.plot(
                true[indfailneg],
                [rangemin + spread * 0.01 for i in indfailneg],
                color='red',
                marker='v',
                linestyle='none',
                markersize=4,
                markeredgecolor='black',
                markeredgewidth=0.4,
            )
        if len(indfailpos) > 0:
            ax.plot(
                true[indfailpos],
                [rangemax - spread * 0.01 for i in indfailpos],
                color='red',
                marker='^',
                linestyle='none',
                markersize=4,
                markeredgecolor='black',
                markeredgewidth=0.4,
            )

    # axes and labels
    ax.set_xlabel(labeltrue)
    ax.set_ylabel(labelpred)

    l = [
        rmse(true, pred),
        mae(true, pred),
        r2(true, pred),
        np.mean(true),
        np.std(true),
    ]
    formatted_loss = f"RMSE: {l[0]:.{precision}f} / MAE: {l[1]:.{precision}f} / R$^2$: {l[2]:.4f} ( {l[3]:.{precision}f} ,  {l[4]:.{precision}f})"
    print(formatted_loss)
    ax.text(
        0.05,
        0.95,
        formatted_loss,
        horizontalalignment='left',
        verticalalignment='top',
        transform=ax.transAxes,
    )

    return ax, l


def save_loss(outfolder, loss, name=""):
    with open(outfolder / "loss.txt", "a") as f:
        f.write(" ".join((f"{name}:", *[str(l) for l in loss])) + "\n")


def plot(task):
    data = np.load(task, allow_pickle=True)

    outfolder = Path(task.parent / task.stem)
    if outfolder.is_dir():
        print(f"{outfolder} exists, not doing anything!")
        return None
    else:
        outfolder.mkdir(parents=True)

    with open(outfolder / "loss.txt", "w") as f:
        f.write("Property / RMSE / MAE / R2 / Mean / Std\n")

    print("energy:")
    fig, ax = fig_and_ax(figsize=(9, 9))
    _, loss = simple_scatterplot(
        data["true_energy"].flatten() * 1000, data["pred_energy"].flatten() * 1000, ax=ax
    )
    fig.savefig(outfolder / "energy.png")
    save_loss(outfolder, loss, name="energy")

    print("forces:")
    fig, ax = fig_and_ax(figsize=(9, 9))
    _, loss = simple_scatterplot(
        data["true_forces"].flatten() * 1000,
        data["pred_forces"].flatten() * 1000,
        ax=ax,
    )
    fig.savefig(outfolder / "forces.png")
    save_loss(outfolder, loss, name="forces")

    if "true_stress" in data:
        print("stress:")
        if not np.isnan(np.sum(data["true_stress"])):
            fig, ax = fig_and_ax(figsize=(9, 9))
            _, loss = simple_scatterplot(
                1000 * data["true_stress"].flatten(),
                1000 * data["pred_stress"].flatten(),
                ax=ax,
                precision=8,
            )
            fig.savefig(outfolder / "stress_all.png")
            save_loss(outfolder, loss, name="stress_all")

            fig, ax = fig_and_ax(figsize=(9, 9))
            _, loss = simple_scatterplot(
                1000 * data["true_stress"][:, 0, 0],
                1000 * data["pred_stress"][:, 0, 0],
                ax=ax,
                precision=8,
            )
            fig.savefig(outfolder / "stress_0.png")
            save_loss(outfolder, loss, name="stress_0")

            fig, ax = fig_and_ax(figsize=(9, 9))
            _, loss = simple_scatterplot(
                1000 * data["true_stress"][:, 1, 1],
                1000 * data["pred_stress"][:, 1, 1],
                ax=ax,
                precision=8,
            )
            fig.savefig(outfolder / "stress_1.png")
            save_loss(outfolder, loss, name="stress_1")

            fig, ax = fig_and_ax(figsize=(9, 9))
            _, loss = simple_scatterplot(
                1000 * data["true_stress"][:, 2, 2],
                1000 * data["pred_stress"][:, 2, 2],
                ax=ax,
                precision=8,
            )
            fig.savefig(outfolder / "stress_2.png")
            save_loss(outfolder, loss, name="stress_2")

            fig, ax = fig_and_ax(figsize=(9, 9))
            _, loss = simple_scatterplot(
                1000 * data["true_stress"][:, 1, 2],
                1000 * data["pred_stress"][:, 1, 2],
                ax=ax,
                precision=8,
            )
            fig.savefig(outfolder / "stress_3.png")
            save_loss(outfolder, loss, name="stress_3")

            fig, ax = fig_and_ax(figsize=(9, 9))
            _, loss = simple_scatterplot(
                1000 * data["true_stress"][:, 0, 2],
                1000 * data["pred_stress"][:, 0, 2],
                ax=ax,
                precision=8,
            )
            fig.savefig(outfolder / "stress_4.png")
            save_loss(outfolder, loss, name="stress_4")

            fig, ax = fig_and_ax(figsize=(9, 9))
            _, loss = simple_scatterplot(
                1000 * data["true_stress"][:, 0, 1],
                1000 * data["pred_stress"][:, 0, 1],
                ax=ax,
                precision=8,
            )
            fig.savefig(outfolder / "stress_5.png")
            save_loss(outfolder, loss, name="stress_5")


def plot_predictions(model_path):
    model_path = Path(model_path)

    tasks = model_path.glob("*.npz")

    for task in tasks:
        plot(task)
