"""Tests for the update command."""
from conftest import cli


def test_update_preserves_local(tmp_project, repo_root):
    """Update re-renders fragments but preserves LOCAL sections."""
    cli.render_agents_md(tmp_project, repo_root, {"python"})

    content = (tmp_project / "AGENTS.md").read_text()
    content += "\n<!-- LOCAL -->\nTeam-specific rules here.\n<!-- /LOCAL -->\n"
    (tmp_project / "AGENTS.md").write_text(content)

    cli.render_agents_md(tmp_project, repo_root, {"python"})

    updated = (tmp_project / "AGENTS.md").read_text()
    assert "Team-specific rules here." in updated
    assert "<!-- BEGIN baseline -->" in updated
    assert "<!-- BEGIN pack: python -->" in updated


def test_update_removes_old_packs(tmp_project, repo_root):
    """If a pack is no longer detected, its fragment is removed."""
    cli.render_agents_md(tmp_project, repo_root, {"python"})
    assert "pack: python" in (tmp_project / "AGENTS.md").read_text()

    cli.render_agents_md(tmp_project, repo_root, set())
    updated = (tmp_project / "AGENTS.md").read_text()
    assert "pack: python" not in updated
    assert "<!-- BEGIN baseline -->" in updated


def test_update_adds_new_packs(tmp_project, repo_root):
    """If a new pack is detected, its fragment is added."""
    cli.render_agents_md(tmp_project, repo_root, set())
    assert "pack: python" not in (tmp_project / "AGENTS.md").read_text()

    cli.render_agents_md(tmp_project, repo_root, {"python"})
    updated = (tmp_project / "AGENTS.md").read_text()
    assert "<!-- BEGIN pack: python -->" in updated
