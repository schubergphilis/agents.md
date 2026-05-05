"""Tests for SKILL.md frontmatter parsing."""
from conftest import cli


SAMPLE_SKILL = """---
name: test-skill
description: A test skill for unit testing purposes with enough characters to pass validation easily.
metadata:
  domain: platform
  lifecycle: build
---

# Test Skill Instructions

Do the thing.
"""


def test_parse_skill_md():
    skill = cli.parse_skill_md(SAMPLE_SKILL)
    assert skill["name"] == "test-skill"
    assert "test skill" in skill["description"].lower()
    assert skill["metadata"]["domain"] == "platform"
    assert skill["metadata"]["lifecycle"] == "build"
    assert "# Test Skill Instructions" in skill["body"]


def test_parse_skill_md_missing_frontmatter():
    result = cli.parse_skill_md("# Just markdown\nNo frontmatter here.\n")
    assert result is None


def test_parse_skill_md_from_file(repo_root):
    path = repo_root / "skills" / "sbp-architecture-review" / "SKILL.md"
    content = path.read_text()
    skill = cli.parse_skill_md(content)
    assert skill["name"] == "sbp-architecture-review"
    assert len(skill["description"]) >= 50
    assert skill["metadata"]["lifecycle"] == "plan"


def test_parse_skill_md_four_space_indent():
    content = """---
name: four-space
description: A skill with four-space indented metadata that should parse correctly for validation.
metadata:
    domain: platform
    lifecycle: build
---

Body here.
"""
    skill = cli.parse_skill_md(content)
    assert skill is not None
    assert skill["metadata"]["domain"] == "platform"
    assert skill["metadata"]["lifecycle"] == "build"


def test_parse_skill_md_multiline_description():
    content = """---
name: multi-desc
description: This is a long description that spans
  multiple lines using YAML continuation
  indentation style.
metadata:
  domain: test
---

Body here.
"""
    skill = cli.parse_skill_md(content)
    assert "long description" in skill["description"]
    assert "multiple lines" in skill["description"]
    assert "indentation style" in skill["description"]
