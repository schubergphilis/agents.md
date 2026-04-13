"""Tests for AGENTS.md rendering via concatenation."""
from conftest import cli


def test_render_concatenates_baseline_and_packs(tmp_project, repo_root):
    cli.render_agents_md(tmp_project, repo_root, {"python"})
    content = (tmp_project / "AGENTS.md").read_text()
    assert "Mission-Critical Engineering" in content
    assert "Python Conventions" in content


def test_render_without_packs(tmp_project, repo_root):
    cli.render_agents_md(tmp_project, repo_root, set())
    content = (tmp_project / "AGENTS.md").read_text()
    assert "Mission-Critical Engineering" in content
    assert "Python" not in content


def test_render_preserves_local_below_separator(tmp_project, repo_root):
    cli.render_agents_md(tmp_project, repo_root, {"python"})
    content = (tmp_project / "AGENTS.md").read_text()
    content += "\n---\nOur team rules here.\n"
    (tmp_project / "AGENTS.md").write_text(content)

    cli.render_agents_md(tmp_project, repo_root, {"python"})
    updated = (tmp_project / "AGENTS.md").read_text()
    assert "Our team rules here." in updated
    assert "Mission-Critical Engineering" in updated


def test_render_removes_old_packs_on_update(tmp_project, repo_root):
    cli.render_agents_md(tmp_project, repo_root, {"python"})
    assert "Python Conventions" in (tmp_project / "AGENTS.md").read_text()

    cli.render_agents_md(tmp_project, repo_root, set())
    assert "Python Conventions" not in (tmp_project / "AGENTS.md").read_text()


def test_render_packs_in_sorted_order(tmp_project, repo_root):
    cli.render_agents_md(tmp_project, repo_root, {"supply-chain", "python"})
    content = (tmp_project / "AGENTS.md").read_text()
    py_idx = content.index("Python Conventions")
    sc_idx = content.index("Supply-Chain Hardening")
    assert py_idx < sc_idx  # python before supply-chain (sorted)
