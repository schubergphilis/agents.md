"""Tests for configuration and TOML parsing."""
from conftest import cli


def test_parse_detection_toml(repo_root):
    detection = cli.parse_detection_toml(repo_root / "detection.toml")
    assert "python" in detection
    assert detection["python"]["files"] == ["pyproject.toml", "setup.py", "requirements.txt"]
    assert detection["python"]["pack"] == "python"


def test_parse_defaults_toml(repo_root):
    defaults = cli.parse_defaults_toml(repo_root / "defaults.toml")
    assert "architecture-review" in defaults["skills"]
    assert "review" in defaults["commands"]


def test_parse_pack_manifest(repo_root):
    manifest = cli.parse_pack_manifest(repo_root / "packs" / "python" / "manifest.toml")
    assert manifest["name"] == "python"
    assert manifest["version"] == "1.0.0"
    assert "pyproject.toml" in manifest["detect_files"]
    assert manifest["targets"]["agents_md"] is True
