"""Shared test fixtures for sbp-skills."""

import importlib.machinery
import importlib.util
import sys
from pathlib import Path

import pytest

_CLI_PATH = Path(__file__).parent.parent / "cli" / "sbp-skills"


def _load_cli():
    loader = importlib.machinery.SourceFileLoader("sbp_skills", str(_CLI_PATH))
    spec = importlib.util.spec_from_file_location("sbp_skills", _CLI_PATH, loader=loader)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["sbp_skills"] = mod
    spec.loader.exec_module(mod)
    return mod


cli = _load_cli()


@pytest.fixture
def tmp_project(tmp_path):
    """Create a temporary project directory."""
    project = tmp_path / "my-project"
    project.mkdir()
    return project


@pytest.fixture
def tmp_home(tmp_path):
    """Create a temporary home directory."""
    home = tmp_path / "home"
    home.mkdir()
    return home


@pytest.fixture
def repo_root():
    """Return the sbp-skills repo root."""
    return Path(__file__).parent.parent
