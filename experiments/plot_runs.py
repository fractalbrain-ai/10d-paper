import argparse
import json
import lzma
import subprocess
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import accumulate
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.text import Text
from matplotlib.ticker import MaxNLocator

EXPERIMENTS = Path(__file__).resolve().parent
DEFAULT_RUNS = {
    "GPT6_Luna_high": "GPT-6 Luna (high)",
    "Qwen38_27b_8FP_xhigh": "Qwen3.8 27B (xhigh, FP8)",
}
DPI = 600
PAPER_WIDTH = 43 / 6
PAPER_FONT_SIZE = 9.5
LABEL_FONT_SIZE = 7
HYDRATION_COLOR = "#0072B2"
SATIETY_COLOR = "#D55E00"
MODEL_STYLES = (
    ("#A72577", "-"),
    ("#303030", "--"),
    ("#19724A", "-."),
    ("#6A3D9A", ":"),
)


@dataclass
class Run:
    seed: int
    label: str
    steps: list[int]
    satiety: list[float]
    hydration: list[float]
    cumulative_reward: list[float]


def read_run(path: Path) -> Run:
    seed = int(path.stem.removesuffix(".jsonl").removeprefix("seed-"))
    label = path.parent.name
    initial = None
    steps, satiety, hydration, rewards = [], [], [], []

    open_log = lzma.open if path.suffix == ".xz" else open
    with open_log(path, "rt", encoding="utf-8") as log:
        for line in log:
            event = json.loads(line)
            kind = event["event"]

            if kind == "provenance":
                seed = event["seed"]
                initial = event["initial_observation"]
                label = event["model_id"]

                for model in event["protocol"].get("inference", []):
                    if model["id"] == event["model_id"]:
                        label = model["label"]
                        break

            elif kind == "start":
                seed = event["seed"]
                label = event["settings"].get("model", label)

            elif kind == "request" and event["step"] == 1 and initial is None:
                initial = json.loads(event["messages"][-1]["content"])["observation"]

            elif kind == "transition":
                step = event["step"]
                if step != len(steps) + 1:
                    raise ValueError(
                        f"{path}: expected step {len(steps) + 1}, got {step}"
                    )

                obs = event["observation"]
                steps.append(step)
                satiety.append(obs["satiety_level"])
                hydration.append(obs["hydration_level"])
                rewards.append(obs["reward"])

    if initial is None or not steps:
        raise ValueError(
            f"{path}: expected an initial observation and game transitions"
        )

    return Run(
        seed,
        label,
        [0, *steps],
        [initial["satiety_level"], *satiety],
        [initial["hydration_level"], *hydration],
        list(accumulate(rewards, initial=0.0)),
    )


def padded_limits(values: Iterable[float]) -> tuple[float, float]:
    low = high = 0.0
    for value in values:
        low = min(low, value)
        high = max(high, value)

    padding = max(1.0, 0.04 * (high - low))

    return low - padding, high + padding


def plot_companion(
    configurations: list[tuple[str, dict[int, Run]]], output: Path
) -> None:
    runs = [run for _, config in configurations for run in config.values()]
    seeds = sorted({run.seed for run in runs})
    resource_limits = padded_limits(
        value
        for run in runs
        for trace in (run.hydration, run.satiety)
        for value in trace
    )
    last_step = max(run.steps[-1] for run in runs)

    fig = plt.figure(
        figsize=(PAPER_WIDTH, 1.05 * len(seeds) + 1.2), layout="constrained"
    )
    grid = fig.add_gridspec(
        len(seeds) + 1,
        len(configurations),
        height_ratios=[1] * len(seeds) + [1.1],
    )
    legend_handles = None

    for i, seed in enumerate(seeds):
        for j, (label, config) in enumerate(configurations):
            ax = fig.add_subplot(grid[i, j])
            ax.set_xlim(0, last_step)
            ax.set_ylim(*resource_limits)
            ax.xaxis.set_major_locator(MaxNLocator(nbins=4, integer=True))
            ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
            ax.axhline(0, color="#8B9094", ls=":", lw=0.85)
            ax.grid(axis="y", color="#E1E4E6", linewidth=0.5)
            ax.set_axisbelow(True)
            ax.spines[["top", "right"]].set_visible(False)
            ax.tick_params(axis="both", labelsize=LABEL_FONT_SIZE)
            ax.tick_params(axis="x", labelbottom=i == len(seeds) - 1)
            ax.tick_params(axis="y", left=j == 0, labelleft=j == 0)

            if i == 0:
                ax.set_title(label, fontsize=PAPER_FONT_SIZE)

            if j == 0:
                ax.set_ylabel(f"Seed {seed}", fontsize=LABEL_FONT_SIZE)

            if run := config.get(seed):
                (hydration,) = ax.plot(
                    run.steps,
                    run.hydration,
                    color=HYDRATION_COLOR,
                    lw=0.9,
                    label="Hydration",
                )
                (satiety,) = ax.plot(
                    run.steps, run.satiety, color=SATIETY_COLOR, lw=0.9, label="Satiety"
                )
                legend_handles = (hydration, satiety)

            else:
                ax.text(
                    0.5,
                    0.5,
                    "Awaiting log",
                    transform=ax.transAxes,
                    ha="center",
                    va="center",
                    fontsize=LABEL_FONT_SIZE,
                    color="#616970",
                )

    fig.legend(
        handles=legend_handles,
        loc="outside upper center",
        ncols=2,
        frameon=False,
        fontsize=LABEL_FONT_SIZE,
    )
    plot_reward(fig.add_subplot(grid[-1, :]), configurations)

    paper_font = subprocess.check_output(["kpsewhich", "uplr8a.pfb"], text=True).strip()
    for label in fig.findobj(Text):
        font = label.get_fontproperties().copy()
        font.set_file(paper_font)
        label.set_fontproperties(font)

    fig.savefig(output, dpi=DPI, facecolor="white")
    plt.close(fig)


def separate_labels(endpoints: list[float], low: float, high: float) -> list[float]:
    gap = (high - low) * min(0.15, 0.9 / len(endpoints))
    positions = []
    for value in endpoints:
        minimum = positions[-1] + gap if positions else low + gap / 2
        positions.append(max(value, minimum))

    maximum = high - gap / 2
    for i in reversed(range(len(positions))):
        positions[i] = min(positions[i], maximum)
        maximum = positions[i] - gap

    return positions


def plot_reward(ax: Axes, configurations: list[tuple[str, dict[int, Run]]]) -> None:
    endpoints = []
    for i, (label, config) in enumerate(configurations):
        color, linestyle = MODEL_STYLES[i % len(MODEL_STYLES)]
        for j, run in enumerate(sorted(config.values(), key=lambda run: run.seed)):
            ax.plot(
                run.steps,
                run.cumulative_reward,
                color=color,
                linestyle=linestyle,
                lw=1.05,
                label=label if j == 0 else None,
            )
            endpoints.append((run, color))

    last_step = max(run.steps[-1] for run, _ in endpoints)
    low, high = padded_limits(
        value for run, _ in endpoints for value in run.cumulative_reward
    )
    ax.set_ylim(low, high)
    ax.set_xlim(0, last_step)
    ticks = MaxNLocator(nbins=4, integer=True).tick_values(0, last_step)
    ax.set_xticks([tick for tick in ticks if 0 <= tick <= last_step])
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.set_xlabel("Game step", fontsize=LABEL_FONT_SIZE)
    ax.set_ylabel("Cumulative\nreward", fontsize=LABEL_FONT_SIZE)
    ax.grid(axis="y", color="#E1E4E6", linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="both", labelsize=LABEL_FONT_SIZE)

    endpoints.sort(key=lambda item: item[0].cumulative_reward[-1])
    labels = separate_labels(
        [run.cumulative_reward[-1] for run, _ in endpoints], low, high
    )
    for (run, color), y in zip(endpoints, labels, strict=True):
        x_end, y_end = run.steps[-1], run.cumulative_reward[-1]
        ax.plot(x_end, y_end, marker="o", color=color, ms=2, clip_on=False)
        ax.annotate(
            f"Seed {run.seed}",
            xy=(x_end, y_end),
            xytext=(1.05, y),
            textcoords=ax.get_yaxis_transform(),
            ha="left",
            va="center",
            fontsize=LABEL_FONT_SIZE,
            color=color,
            arrowprops={
                "arrowstyle": "-|>",
                "color": "#505458",
                "lw": 0.65,
                "mutation_scale": 6,
                "shrinkB": 2,
            },
        )

    ax.legend(loc="lower left", frameon=False, fontsize=LABEL_FONT_SIZE)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot resources and cumulative reward from companion game logs."
    )
    parser.add_argument(
        "runs",
        type=Path,
        nargs="*",
        default=[EXPERIMENTS / name for name in DEFAULT_RUNS],
        help="one directory of seed-*.jsonl or seed-*.jsonl.xz logs per model configuration",
    )
    parser.add_argument("-o", "--output", type=Path, help="output PNG path")
    args = parser.parse_args()

    configurations = []
    for directory in args.runs:
        if not directory.is_dir():
            parser.error(f"run directory does not exist: {directory}")

        logs = {path.name: path for path in directory.glob("seed-*.jsonl")}
        for path in directory.glob("seed-*.jsonl.xz"):
            logs.setdefault(path.stem, path)

        runs = [read_run(logs[name]) for name in sorted(logs)]
        labels = {run.label for run in runs}
        if len(labels) > 1:
            parser.error(f"{directory}: the logs must use one model configuration")

        label = DEFAULT_RUNS.get(directory.name, next(iter(labels), directory.name))
        configurations.append((label, {run.seed: run for run in runs}))

    if not any(config for _, config in configurations):
        parser.error("no seed-*.jsonl or seed-*.jsonl.xz logs found")

    filename = "companion-traces.png"
    if len(args.runs) == 1:
        filename = f"{args.runs[0].name}-{filename}"

    output = args.output or EXPERIMENTS / filename
    plot_companion(configurations, output)
    print(f"Wrote {output} ({DPI} DPI)")


if __name__ == "__main__":
    main()
