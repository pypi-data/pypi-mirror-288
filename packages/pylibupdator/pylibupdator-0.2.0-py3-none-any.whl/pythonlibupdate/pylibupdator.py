import os
import pkg_resources
import requests
from pathlib import Path

def get_installed_packages(site_packages_dir):
    packages = [d for d in pkg_resources.working_set]
    return [p for p in packages if site_packages_dir in str(p.location)]

def get_latest_version(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["info"]["version"]
    return None

def check_for_updates(site_packages_dir, output_file):
    packages = get_installed_packages(site_packages_dir)
    count = 1
    with open(output_file, 'w') as file:
        for package in packages:
            package_name = package.project_name
            installed_version = package.version
            latest_version = get_latest_version(package_name)
            if latest_version and latest_version != installed_version:
                update_message = (f"{count}. Package '{package_name}' has a new version available: "
                                  f"{installed_version} -> {latest_version}\n"
                                  f"To upgrade, run: pip install --upgrade {package_name}\n\n")
                print(update_message)
                file.write(update_message)
                count += 1

def main():
    site_packages_dir = next(p for p in pkg_resources.working_set if "site-packages" in str(p.location)).location
    desktop_path = Path.home() / "Desktop"
    output_file = desktop_path / "Libraries To Upgrade.txt"

    check_for_updates(site_packages_dir, output_file)
    print(f"A text file is saved to: {output_file}")
