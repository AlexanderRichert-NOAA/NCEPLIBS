#!/usr/bin/env python3
import sys
import yaml
import json
from github import Github
from datetime import datetime

def main(config_path):
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    repos = cfg['repos']
    gh = Github()  # Unauthenticated, or use GITHUB_TOKEN

    stats = {}
    lines = ["## GitHub Repository Statistics\n"]

    for repo_name in repos:
        repo = gh.get_repo(repo_name)
        clones = repo.get_clones_traffic()
        commits = repo.get_commits(since=datetime.utcnow().replace(day=1, hour=0, minute=0, second=0))

        shortname = repo_name.split('/')[-1]
        stats[shortname] = {
            "commits": commits.totalCount,
            "clones_total": clones['count'],
            "clones_unique": clones['uniques']
        }

        lines.append(f"### `{repo_name}`")
        lines.append(f"- Monthly commits: {commits.totalCount}")
        lines.append(f"- Monthly clones: {clones['count']} total, {clones['uniques']} unique\n")

    # Write markdown report
    with open("output/github_stats.md", "w") as f:
        f.write("\n".join(lines))

    # Write JSON file
    with open("output/github_stats.json", "w") as f:
        json.dump(stats, f, indent=2)

if __name__ == "__main__":
    main(sys.argv[1])

