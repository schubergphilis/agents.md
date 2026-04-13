"""Tests for AI tool detection and project stack detection."""
from pathlib import Path
from conftest import cli


def test_detect_claude_code(tmp_home):
    (tmp_home / ".claude").mkdir()
    tools = cli.detect_tools(tmp_home)
    assert "claude-code" in tools
    assert tools["claude-code"]["skills_dir"] == tmp_home / ".claude" / "skills"


def test_detect_copilot(tmp_home):
    (tmp_home / ".copilot").mkdir()
    tools = cli.detect_tools(tmp_home)
    assert "copilot" in tools


def test_detect_opencode(tmp_home):
    (tmp_home / ".config" / "opencode").mkdir(parents=True)
    tools = cli.detect_tools(tmp_home)
    assert "opencode" in tools


def test_detect_no_tools(tmp_home):
    tools = cli.detect_tools(tmp_home)
    assert tools == {}


def test_detect_stack_python(tmp_project):
    (tmp_project / "pyproject.toml").write_text("[project]\nname = 'foo'\n")
    detection_rules = {
        "python": {"files": ["pyproject.toml", "setup.py"], "pack": "python", "depends": []},
        "terraform": {"files": ["*.tf"], "pack": "terraform", "depends": []},
    }
    packs = cli.detect_stack(tmp_project, detection_rules)
    assert "python" in packs
    assert "terraform" not in packs


def test_detect_stack_with_depends(tmp_project):
    (tmp_project / ".github" / "workflows").mkdir(parents=True)
    (tmp_project / ".github" / "workflows" / "ci.yml").write_text("name: CI\n")
    detection_rules = {
        "github-actions": {
            "files": [".github/workflows/*.yml"],
            "pack": "github-actions",
            "depends": ["supply-chain"],
        },
    }
    packs = cli.detect_stack(tmp_project, detection_rules)
    assert "github-actions" in packs
    assert "supply-chain" in packs


def test_detect_stack_glob_pattern(tmp_project):
    (tmp_project / "main.tf").write_text('resource "aws_instance" "x" {}\n')
    detection_rules = {
        "terraform": {"files": ["*.tf"], "pack": "terraform", "depends": []},
    }
    packs = cli.detect_stack(tmp_project, detection_rules)
    assert "terraform" in packs
