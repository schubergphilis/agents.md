"""Tests for pack and skill validation."""
from pathlib import Path
from conftest import cli


def test_validate_valid_pack(repo_root):
    errors = cli.validate_pack(repo_root / "packs" / "python")
    assert errors == [], f"Unexpected errors: {errors}"


def test_validate_pack_missing_manifest(tmp_path):
    pack_dir = tmp_path / "bad-pack"
    pack_dir.mkdir()
    (pack_dir / "AGENTS.md").write_text("## Bad Pack\n\nStuff\n")
    errors = cli.validate_pack(pack_dir)
    assert any("manifest.toml" in e for e in errors)


def test_validate_pack_missing_agents_md(tmp_path):
    pack_dir = tmp_path / "no-agents"
    pack_dir.mkdir()
    (pack_dir / "manifest.toml").write_text('[pack]\nname = "no-agents"\ndescription = "Test pack with enough description for validation"\nversion = "1.0.0"\n')
    errors = cli.validate_pack(pack_dir)
    assert any("AGENTS.md" in e for e in errors)


def test_validate_valid_skill(repo_root):
    errors = cli.validate_skill(repo_root / "skills" / "architecture-review")
    assert errors == [], f"Unexpected errors: {errors}"


def test_validate_skill_short_description(tmp_path):
    skill_dir = tmp_path / "bad-skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: bad-skill\ndescription: Too short\n---\nBody\n")
    errors = cli.validate_skill(skill_dir)
    assert any("description" in e.lower() for e in errors)


def test_validate_skill_name_mismatch(tmp_path):
    skill_dir = tmp_path / "actual-name"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("---\nname: wrong-name\ndescription: This description is long enough to pass the minimum character validation requirement.\n---\nBody\n")
    errors = cli.validate_skill(skill_dir)
    assert any("name" in e.lower() and "match" in e.lower() for e in errors)
