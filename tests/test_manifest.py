"""Tests for .sbp/manifest.json read/write."""
from conftest import cli


def test_create_manifest():
    manifest = cli.create_manifest(
        central_repo="git@github.com:schuberg/sbp-skills.git",
        tools=["claude-code"],
        baseline_version="1.0.0",
        packs={"python": {"version": "1.0.0", "source": "auto-detected", "detected_by": "pyproject.toml"}},
        skills={"architecture-review": {"source": "default"}},
    )
    assert manifest["version"] == "1"
    assert manifest["baseline"]["version"] == "1.0.0"
    assert "python" in manifest["packs"]
    assert manifest["packs"]["python"]["source"] == "auto-detected"


def test_save_and_load_manifest(tmp_project):
    manifest = cli.create_manifest(
        central_repo="git@github.com:schuberg/sbp-skills.git",
        tools=["claude-code"],
        baseline_version="1.0.0",
        packs={},
        skills={},
    )
    cli.save_manifest(tmp_project, manifest)
    assert (tmp_project / ".sbp" / "manifest.json").exists()

    loaded = cli.load_manifest(tmp_project)
    assert loaded["baseline"]["version"] == "1.0.0"


def test_load_manifest_missing(tmp_project):
    loaded = cli.load_manifest(tmp_project)
    assert loaded is None


def test_manifest_removed_list(tmp_project):
    manifest = cli.create_manifest(
        central_repo="test",
        tools=[],
        baseline_version="1.0.0",
        packs={},
        skills={},
    )
    manifest["removed"] = ["terraform"]
    cli.save_manifest(tmp_project, manifest)

    loaded = cli.load_manifest(tmp_project)
    assert "terraform" in loaded["removed"]
