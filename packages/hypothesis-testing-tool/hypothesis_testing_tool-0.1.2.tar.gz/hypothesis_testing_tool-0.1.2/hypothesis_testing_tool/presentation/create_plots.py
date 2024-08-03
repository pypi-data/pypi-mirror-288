import matplotlib.pyplot as plt


def create_one_sample_hypothesis_plot(path_to_save_plot: str, ci_dict: dict, width=5, height=5):

    fig, ax = plt.subplots(1, 1, figsize=(width, height))

    ax.plot([ci_dict["lower_bound"], ci_dict["upper_bound"]], [0, 0], color="gray", linewidth=1)
    ax.plot(ci_dict["lower_bound"], 0, marker="o", color="orange", markersize=6, label="95% CI Lower Bound")
    ax.plot(ci_dict["point_estimate"], 0, marker="o", color="black", markersize=6, label="Observed Point Estimate")
    ax.plot(ci_dict["upper_bound"], 0, marker="o", color="#05c9de", markersize=6, label="95% CI Upper Bound")

    ax.set_yticks([])
    ax.set_xlabel("Values")
    ax.set_title("95% Confidence Interval (CI) for the Mean of One Sample")

    ax.axvline(x=ci_dict["null_population_mean"], color="red", linestyle="--", linewidth=2, label="Null Population Mean")

    ax.legend(loc="upper right", frameon=True)

    plt.savefig(f"{path_to_save_plot}")
    plt.close(fig)

    return fig, ax
