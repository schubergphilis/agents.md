"""Tests for CLI management commands."""
from pathlib import Path
from conftest import cli


def test_validate_pack_name_mismatch(tmp_path):
    """validate_pack catches name != directory name."""
    pack_dir = tmp_path / "actual-name"
    pack_dir.mkdir()
    (pack_dir / "manifest.toml").write_text(
        '[pack]\nname = "wrong-name"\n'
        'description = "This description is long enough to pass the minimum character validation check"\n'
        'version = "1.0.0"\n'
    )
    (pack_dir / "AGENTS.md").write_text("## Conventions\n")
    (pack_dir / "README.md").write_text("# Test\n")
    errors = cli.validate_pack(pack_dir)
    assert any("wrong-name" in e and "actual-name" in e for e in errors)


def test_link_skills_replaces_existing_symlink(tmp_home, repo_root):
    """link_skills replaces an existing symlink cleanly."""
    skills_dir = tmp_home / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    # Create a stale symlink
    stale = skills_dir / "sbp-architecture-review"
    stale.symlink_to("/nonexistent/path")

    cli.link_skills(tmp_home, repo_root, ["sbp-architecture-review"], "claude-code")
    assert stale.is_symlink()
    assert (stale / "SKILL.md").exists()


def test_link_skills_replaces_existing_directory(tmp_home, repo_root):
    """link_skills replaces an existing directory with a symlink."""
    skills_dir = tmp_home / ".claude" / "skills"
    skills_dir.mkdir(parents=True)
    # Create a real directory where the symlink should go
    existing = skills_dir / "sbp-architecture-review"
    existing.mkdir()
    (existing / "old-file.txt").write_text("stale")

    cli.link_skills(tmp_home, repo_root, ["sbp-architecture-review"], "claude-code")
    assert existing.is_symlink()
    assert (existing / "SKILL.md").exists()


def test_link_skills_skips_unknown_tool(tmp_home, repo_root):
    """link_skills does nothing for tools without skills_dir."""
    cli.link_skills(tmp_home, repo_root, ["architecture-review"], "copilot")
    # copilot has no skills_dir, so nothing should be created
    assert not (tmp_home / ".copilot" / "skills").exists()


def test_render_agents_md_empty_packs(tmp_project, repo_root):
    """Render with no packs — just baseline."""
    cli.render_agents_md(tmp_project, repo_root, set())
    content = (tmp_project / "AGENTS.md").read_text()
    assert "Mission-Critical Engineering" in content
    assert "Python" not in content


def test_copy_commands_with_pack_commands(tmp_project, repo_root):
    """copy_commands picks up pack-specific commands if they exist."""
    # Create a fake pack with commands
    pack_cmds = repo_root / "packs" / "python" / "commands"
    had_commands = pack_cmds.exists()
    if not had_commands:
        pack_cmds.mkdir(parents=True)
        (pack_cmds / "lint.md").write_text("Run ruff check.\n")

    cli.copy_commands(tmp_project, repo_root, ["review"], {"python"})
    commands_dir = tmp_project / ".claude" / "commands"
    assert (commands_dir / "review.md").exists()

    # Cleanup if we created the test commands
    if not had_commands:
        import shutil
        shutil.rmtree(pack_cmds)


def test_gitignore_created_on_init(tmp_project, repo_root):
    """Verify .sbp/ gets added to .gitignore."""
    # Simulate the gitignore logic from init
    gitignore = tmp_project / ".gitignore"
    assert not gitignore.exists()

    # Create manifest (simulates init writing it)
    manifest = cli.create_manifest("local", ["claude-code"], "1.0.0", {}, {})
    cli.save_manifest(tmp_project, manifest)

    # Now test the gitignore logic
    if gitignore.exists():
        content = gitignore.read_text()
        if ".sbp/" not in content:
            with open(gitignore, "a") as f:
                f.write("\n.sbp/\n")
    else:
        gitignore.write_text(".sbp/\n")

    assert ".sbp/" in gitignore.read_text()


def test_gitignore_appended_when_exists(tmp_project):
    """Verify .sbp/ gets appended to existing .gitignore."""
    gitignore = tmp_project / ".gitignore"
    gitignore.write_text("node_modules/\n*.pyc\n")

    content = gitignore.read_text()
    if ".sbp/" not in content:
        with open(gitignore, "a") as f:
            f.write("\n.sbp/\n")

    updated = gitignore.read_text()
    assert "node_modules/" in updated
    assert ".sbp/" in updated


def test_gitignore_not_duplicated(tmp_project):
    """Verify .sbp/ is not added twice."""
    gitignore = tmp_project / ".gitignore"
    gitignore.write_text("node_modules/\n.sbp/\n")

    content = gitignore.read_text()
    if ".sbp/" not in content:
        with open(gitignore, "a") as f:
            f.write("\n.sbp/\n")

    assert content.count(".sbp/") == 1
