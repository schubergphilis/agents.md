"""Tests for the init command — integration tests using local repo as source."""
from pathlib import Path
from conftest import cli


def test_render_agents_md(tmp_project, repo_root):
    """Test that init renders AGENTS.md with baseline + detected pack fragments."""
    (tmp_project / "pyproject.toml").write_text("[project]\nname='test'\n")

    cli.render_agents_md(
        project_dir=tmp_project,
        repo_root=repo_root,
        detected_packs={"python"},
    )

    agents_md = (tmp_project / "AGENTS.md").read_text()
    assert "<!-- BEGIN baseline -->" in agents_md
    assert "<!-- END baseline -->" in agents_md
    assert "<!-- BEGIN pack: python -->" in agents_md
    assert "Mission-Critical Engineering" in agents_md


def test_render_claude_md(tmp_project, repo_root):
    """Test that init renders CLAUDE.md with baseline + pack fragments."""
    cli.render_claude_md(
        project_dir=tmp_project,
        repo_root=repo_root,
        detected_packs={"python"},
    )

    claude_md = (tmp_project / "CLAUDE.md").read_text()
    assert "<!-- BEGIN baseline -->" in claude_md
    assert "<!-- BEGIN pack: python -->" in claude_md


def test_render_claude_md_skips_packs_without_claude_md(tmp_project, repo_root):
    """Supply-chain pack has no CLAUDE.md — should not appear."""
    cli.render_claude_md(
        project_dir=tmp_project,
        repo_root=repo_root,
        detected_packs={"supply-chain"},
    )

    claude_md = (tmp_project / "CLAUDE.md").read_text()
    assert "<!-- BEGIN baseline -->" in claude_md
    assert "supply-chain" not in claude_md


def test_copy_commands(tmp_project, repo_root):
    """Test that default commands are copied to .claude/commands/."""
    cli.copy_commands(
        project_dir=tmp_project,
        repo_root=repo_root,
        defaults=["review", "challenge", "risk-check"],
        detected_packs=set(),
    )

    commands_dir = tmp_project / ".claude" / "commands"
    assert (commands_dir / "review.md").exists()
    assert (commands_dir / "challenge.md").exists()
    assert (commands_dir / "risk-check.md").exists()


def test_link_skills(tmp_home, repo_root):
    """Test that default skills are symlinked to ~/.claude/skills/."""
    (tmp_home / ".claude" / "skills").mkdir(parents=True)

    cli.link_skills(
        home=tmp_home,
        repo_root=repo_root,
        skills=["architecture-review", "deploy-checklist"],
        tool="claude-code",
    )

    skills_dir = tmp_home / ".claude" / "skills"
    assert (skills_dir / "architecture-review").is_symlink()
    assert (skills_dir / "deploy-checklist").is_symlink()
    assert (skills_dir / "architecture-review" / "SKILL.md").exists()


def test_init_preserves_local_section(tmp_project, repo_root):
    """Test that re-running render preserves LOCAL sections."""
    cli.render_agents_md(tmp_project, repo_root, {"python"})

    agents_md = (tmp_project / "AGENTS.md").read_text()
    agents_md += "\n<!-- LOCAL -->\nOur team-specific rules.\n<!-- /LOCAL -->\n"
    (tmp_project / "AGENTS.md").write_text(agents_md)

    cli.render_agents_md(tmp_project, repo_root, {"python"})

    updated = (tmp_project / "AGENTS.md").read_text()
    assert "Our team-specific rules." in updated
    assert "<!-- LOCAL -->" in updated
