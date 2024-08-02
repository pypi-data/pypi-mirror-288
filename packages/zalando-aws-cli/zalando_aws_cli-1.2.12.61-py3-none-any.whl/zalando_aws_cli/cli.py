import os
import platform
import shutil
import subprocess
import sys

import pkg_resources

# Constants for documentation URLs
DOCS_BASE_URL = "https://cloud.docs.zalando.net/reference/zaws/"
DOCS_USAGE_URL = f"{DOCS_BASE_URL}#usage"
DOCS_INSTALL_URL = f"{DOCS_BASE_URL}#installation"

# Supported Ubuntu versions
SUPPORTED_UBUNTU_VERSIONS = ["jammy", "focal", "bionic", "noble"]


def is_new_cli_installed():
    return shutil.which("zalando-aws-cli") is not None


def is_debian_based():
    return os.path.isfile("/etc/debian_version")


def get_ubuntu_codename():
    try:
        return subprocess.check_output(
            ["lsb_release", "-cs"], universal_newlines=True,
        ).strip()
    except subprocess.CalledProcessError:
        return None


def run_linux_installer(codename):
    commands = [
        f'echo "deb [trusted=yes arch=amd64,arm64] https://cloud-utils.s3.eu-central-1.amazonaws.com/apt/ {codename} main" | sudo tee -a /etc/apt/sources.list.d/zalando-aws-cli.list',  # noqa: E501
        "sudo apt update",
        "sudo apt install -y zalando-aws-cli",
    ]
    for cmd in commands:
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError:
            print(f"Error executing command: {cmd}")
            return False
    return True


def main():
    print("The Zalando AWS CLI (zaws) is deprecated.")
    print(f"Please use the new tool. Documentation available at: {DOCS_BASE_URL}")

    if is_new_cli_installed():
        print(
            "\nGood news! The new Zalando AWS CLI is already installed on your system.",
        )
        print(
            "You can start using it immediately. For usage instructions, please visit:",
        )
        print(DOCS_USAGE_URL)
        sys.exit(0)

    system = platform.system()
    if system == "Darwin":  # macOS
        print("\nThe new Zalando AWS CLI is not installed on your system.")
        print("Would you like to install the new macOS version? (y/n)")
        choice = input().strip().lower()
        if choice == "y":
            script_path = pkg_resources.resource_filename(
                "zalando_aws_cli", "../scripts/zalando-aws-cli_mac_installer.sh",
            )
            try:
                subprocess.run(["/bin/bash", script_path], check=True)
                print("Installation complete. You can now use the new Zalando AWS CLI.")
                print(f"For usage instructions, please visit: {DOCS_USAGE_URL}")
            except subprocess.CalledProcessError:
                print(
                    f"Installation failed. Please visit {DOCS_INSTALL_URL} for manual installation instructions.",
                )
        else:
            print("Installation skipped. You can manually install the new tool later.")
    elif system == "Linux" and is_debian_based():
        ubuntu_codename = get_ubuntu_codename()
        if ubuntu_codename in SUPPORTED_UBUNTU_VERSIONS:
            codename = ubuntu_codename
        else:
            codename = "jammy"  # fallback to jammy for unsupported versions or non-Ubuntu Debian-based systems

        print("\nThe new Zalando AWS CLI is not installed on your system.")
        print(
            f"Would you like to install the new version for {codename.capitalize()}? (y/n)",
        )
        choice = input().strip().lower()
        if choice == "y":
            if run_linux_installer(codename):
                print("Installation complete. You can now use the new Zalando AWS CLI.")
                print(f"For usage instructions, please visit: {DOCS_USAGE_URL}")
            else:
                print(
                    f"Installation failed. Please visit {DOCS_INSTALL_URL} for manual installation instructions.",
                )
        else:
            print("Installation skipped. You can manually install the new tool later.")
    else:
        print(
            f"\nPlease visit {DOCS_INSTALL_URL} for installation instructions for your platform.",
        )

    print("\nAfter installation, you may want to enable autocompletion.")
    print(
        "Check 'zalando-aws-cli completion --help' for information on how to configure autocompletion in your shell.",
    )

    sys.exit(1)


if __name__ == "__main__":
    main()
