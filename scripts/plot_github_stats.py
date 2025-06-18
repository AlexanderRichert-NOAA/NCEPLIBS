#!/usr/bin/env python3
import sys
import json
import matplotlib.pyplot as plt

def main(config_path, json_path, out_png):
    with open(json_path) as f:
        stats = json.load(f)

    libraries = list(stats.keys())
    commits = [stats[lib]["commits"] for lib in libraries]
    clones = [stats[lib]["clones_unique"] for lib in libraries]

    x = range(len(libraries))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([i - width/2 for i in x], commits, width, label='Commits', color='steelblue')
    ax.bar([i + width/2 for i in x], clones, width, label='Unique Clones', color='orange')

    ax.set_xlabel('Library')
    ax.set_ylabel('Count')
    ax.set_title('GitHub Activity (Current Month)')
    ax.set_xticks(x)
    ax.set_xticklabels(libraries)
    ax.legend()
    ax.grid(axis='y', linestyle='--', linewidth=0.5)

    plt.tight_layout()
    plt.savefig(out_png)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: plot_github_stats.py CONFIG_PATH INPUT_JSON OUTPUT_PNG")
        sys.exit(1)
    _, config_path, json_path, out_png = sys.argv
    main(config_path, json_path, out_png)
