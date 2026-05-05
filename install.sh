#!/usr/bin/env bash
set -euo pipefail

# sbp-skills installer
# Usage: curl -sSL https://.../install.sh | bash
#
# Override the default repo with SBP_SKILLS_REPO:
#   SBP_SKILLS_REPO=https://gitlab.com/my-org/sbp-skills.git curl ... | bash

DEFAULT_REPO="https://github.com/schubergphilis/agents.md.git"
REPO_URL="${SBP_SKILLS_REPO:-$DEFAULT_REPO}"
INSTALL_DIR="${HOME}/.local/bin"
CACHE_DIR="${HOME}/.cache/sbp-skills"

echo "Installing sbp-skills..."

# Check Python 3.11+
if ! command -v python3 &>/dev/null; then
    echo "Error: python3 not found."
    echo ""
    echo "Install Python 3.11+:"
    echo "  macOS:   xcode-select --install"
    echo "  Ubuntu:  sudo apt install python3"
    echo "  Windows: https://python.org/downloads/"
    exit 1
fi

PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)

if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 11 ]; }; then
    echo "Error: Python 3.11+ required (found $PY_VERSION)"
    exit 1
fi

# Check git
if ! command -v git &>/dev/null; then
    echo "Error: git not found. Install git first."
    exit 1
fi

# Clone or pull the repo
if [ -d "$CACHE_DIR/repo" ]; then
    echo "Updating central repo..."
    git -C "$CACHE_DIR/repo" pull --quiet
else
    echo "Cloning central repo..."
    mkdir -p "$CACHE_DIR"
    git clone --quiet "$REPO_URL" "$CACHE_DIR/repo"
fi

# Install the CLI
mkdir -p "$INSTALL_DIR"
cp "$CACHE_DIR/repo/cli/sbp-skills" "$INSTALL_DIR/sbp-skills"
chmod +x "$INSTALL_DIR/sbp-skills"

# Check PATH
if ! echo "$PATH" | tr ':' '\n' | grep -q "$INSTALL_DIR"; then
    echo ""
    echo "Add to your PATH:"
    echo "  export PATH=\"$INSTALL_DIR:\$PATH\""
    echo ""
fi

echo "Installed sbp-skills to $INSTALL_DIR/sbp-skills"
echo "Run 'sbp-skills init' in your project to get started."
