#!/usr/bin/env python3
import requests
import re
import sys
import yaml
from bs4 import BeautifulSoup

def list_version_dirs(base_url):
    resp = requests.get(base_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return [
        a['href'].strip('/')
        for a in soup.find_all('a')
        if a['href'].endswith('/') and not a['href'].startswith('?') and '.v' in a['href']
    ]

def fetch_versions(base_url, directory, files, libs):
    results = {}
    for file in files:
        try:
            url = f"{base_url}{directory}/{file}"
            print("Getting URL:", url, file=sys.stderr)
            text = requests.get(url).text
            for lib in libs:
                match = re.search(rf'{lib}_ver\s*=\s*([\w\.]+)', text.lower())
                if match:
                    results[lib] = match.group(1)
        except Exception as e:
            print(f"Warning: Failed to fetch {url} ({e})", file=sys.stderr)
            continue
    return results

def main(config_path):
    with open(config_path) as f:
        cfg = yaml.safe_load(f)

    base_url = cfg['nwprod_base_url']
    files = ['build.ver']
    libs = cfg['libraries']

    if 'nwprod_subdirs' in cfg:
        dirs = cfg['nwprod_subdirs']
    else:
        dirs = [d + "/versions/" for d in list_version_dirs(base_url)]

    print("## Library Usage in NCO `nwprod` Version Files\n")

    # Header row
    header = "| nwprod code | " + " | ".join(f"`{lib}`" for lib in libs) + " |"
    separator = "|-------------|" + "|".join(["---"] * len(libs)) + "|"
    print(header)
    print(separator)

    lib_counts = {lib: 0 for lib in libs}
    total_rows = 0

    for dir in sorted(dirs):
        print(f"Processing: {dir}", file=sys.stderr)
        usage = fetch_versions(base_url, dir, files, libs)

        # Skip completely empty rows
        if not usage:
            row = [f"`{dir.rstrip('/versions/')}`"] + ["❌"] * len(libs)
        else:
            row = [f"`{dir.rstrip('/versions/')}`"]
            for lib in libs:
                if lib in usage:
                    row.append(usage[lib])
                    lib_counts[lib] += 1
                else:
                    row.append("❌")
        print("| " + " | ".join(row) + " |")
        total_rows += 1

    # TOTAL row
    total_row = ["**TOTAL**"]
    for lib in libs:
        total_row.append(str(lib_counts[lib]))
    print("| " + " | ".join(total_row) + " |")

if __name__ == '__main__':
    main(sys.argv[1])
