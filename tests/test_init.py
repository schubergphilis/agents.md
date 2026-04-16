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
    assert "Mission-Critical Engineering" in agents_md
    assert "Python Conventions" in agents_md


def test_render_claude_md(tmp_project, repo_root):
    """Test that init renders CLAUDE.md with baseline + pack fragments."""
    cli.render_claude_md(
        project_dir=tmp_project,
        repo_root=repo_root,
        detected_packs={"python"},
    )

    claude_md = (tmp_project / "CLAUDE.md").read_text()
    assert "Mission-Critical" in claude_md
    assert "Python — Claude Code" in claude_md


def test_render_claude_md_skips_packs_without_claude_md(tmp_project, repo_root):
    """Supply-chain pack has no CLAUDE.md — should not appear."""
    cli.render_claude_md(
        project_dir=tmp_project,
        repo_root=repo_root,
        detected_packs={"supply-chain"},
    )

    claude_md = (tmp_project / "CLAUDE.md").read_text()
    assert "Mission-Critical" in claude_md
    assert "Supply-Chain" not in claude_md


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


def test_copy_copilot_prompts(tmp_project, repo_root):
    """Test that commands are copied as .prompt.md files for Copilot."""
    count = cli.copy_copilot_prompts(
        project_dir=tmp_project,
        repo_root=repo_root,
        defaults=["review", "challenge", "risk-check"],
        detected_packs=set(),
    )

    prompts_dir = tmp_project / ".github" / "copilot" / "prompts"
    assert (prompts_dir / "review.prompt.md").exists()
    assert (prompts_dir / "challenge.prompt.md").exists()
    assert (prompts_dir / "risk-check.prompt.md").exists()
    assert count == 3


def test_copy_copilot_prompts_content_matches_commands(tmp_project, repo_root):
    """Test that Copilot prompt files have the same content as Claude command files."""
    cli.copy_commands(tmp_project, repo_root, ["review"], set())
    cli.copy_copilot_prompts(tmp_project, repo_root, ["review"], set())

    claude_content = (tmp_project / ".claude" / "commands" / "review.md").read_text()
    copilot_content = (tmp_project / ".github" / "copilot" / "prompts" / "review.prompt.md").read_text()
    assert claude_content == copilot_content


def test_copy_copilot_prompts_empty_defaults(tmp_project, repo_root):
    """Test that copy_copilot_prompts handles empty defaults gracefully."""
    count = cli.copy_copilot_prompts(
        project_dir=tmp_project,
        repo_root=repo_root,
        defaults=[],
        detected_packs=set(),
    )

    prompts_dir = tmp_project / ".github" / "copilot" / "prompts"
    assert prompts_dir.exists()
    assert count == 0


def test_copy_copilot_prompts_with_pack_commands(tmp_project, repo_root):
    """Test that pack-specific commands are also copied as Copilot prompts."""
    pack_cmds = repo_root / "packs" / "python" / "commands"
    had_commands = pack_cmds.exists()
    if not had_commands:
        pack_cmds.mkdir(parents=True)
        (pack_cmds / "lint.md").write_text("Run ruff check.\n")

    count = cli.copy_copilot_prompts(tmp_project, repo_root, ["review"], {"python"})
    prompts_dir = tmp_project / ".github" / "copilot" / "prompts"
    assert (prompts_dir / "review.prompt.md").exists()

    if not had_commands:
        assert (prompts_dir / "lint.prompt.md").exists()
        assert count == 2
        import shutil
        shutil.rmtree(pack_cmds)


def test_init_preserves_local_section(tmp_project, repo_root):
    """Test that re-running render preserves local additions below separator."""
    cli.render_agents_md(tmp_project, repo_root, {"python"})
    content = (tmp_project / "AGENTS.md").read_text()
    content += "\n---\nOur team-specific rules.\n"
    (tmp_project / "AGENTS.md").write_text(content)

    cli.render_agents_md(tmp_project, repo_root, {"python"})

    updated = (tmp_project / "AGENTS.md").read_text()
    assert "Our team-specific rules." in updated
