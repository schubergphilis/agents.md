"""Tests for fragment merging with HTML comment markers."""
from conftest import cli


def test_insert_into_empty_file():
    content = ""
    result = cli.insert_fragment(content, "baseline", "# Hello world\n")
    assert "<!-- BEGIN baseline -->" in result
    assert "# Hello world" in result
    assert "<!-- END baseline -->" in result


def test_insert_preserves_existing_content():
    content = "# My Project\n\nSome existing text.\n"
    result = cli.insert_fragment(content, "pack: python", "Python rules here.\n")
    assert "# My Project" in result
    assert "Some existing text." in result
    assert "<!-- BEGIN pack: python -->" in result
    assert "Python rules here." in result


def test_update_replaces_existing_fragment():
    content = (
        "# Header\n"
        "<!-- BEGIN baseline -->\nOld content\n<!-- END baseline -->\n"
        "Footer\n"
    )
    result = cli.insert_fragment(content, "baseline", "New content\n")
    assert "Old content" not in result
    assert "New content" in result
    assert result.count("<!-- BEGIN baseline -->") == 1
    assert "Footer" in result
    assert "# Header" in result


def test_remove_fragment():
    content = (
        "# Header\n"
        "<!-- BEGIN pack: python -->\nPython stuff\n<!-- END pack: python -->\n"
        "<!-- BEGIN pack: terraform -->\nTF stuff\n<!-- END pack: terraform -->\n"
    )
    result = cli.remove_fragment(content, "pack: python")
    assert "Python stuff" not in result
    assert "pack: python" not in result
    assert "TF stuff" in result
    assert "# Header" in result


def test_preserve_local_section():
    content = (
        "<!-- BEGIN baseline -->\nBaseline\n<!-- END baseline -->\n"
        "<!-- LOCAL -->\nTeam stuff\n<!-- /LOCAL -->\n"
    )
    result = cli.insert_fragment(content, "baseline", "Updated baseline\n")
    assert "Updated baseline" in result
    assert "Team stuff" in result
    assert "<!-- LOCAL -->" in result


def test_insert_multiple_fragments_in_order():
    content = ""
    content = cli.insert_fragment(content, "baseline", "Base\n")
    content = cli.insert_fragment(content, "pack: python", "Py\n")
    content = cli.insert_fragment(content, "pack: terraform", "TF\n")
    lines = content.split("\n")
    base_idx = next(i for i, l in enumerate(lines) if "BEGIN baseline" in l)
    py_idx = next(i for i, l in enumerate(lines) if "BEGIN pack: python" in l)
    tf_idx = next(i for i, l in enumerate(lines) if "BEGIN pack: terraform" in l)
    assert base_idx < py_idx < tf_idx


def test_extract_fragment_ids():
    content = (
        "<!-- BEGIN baseline -->\nX\n<!-- END baseline -->\n"
        "<!-- BEGIN pack: python -->\nY\n<!-- END pack: python -->\n"
    )
    ids = cli.extract_fragment_ids(content)
    assert ids == ["baseline", "pack: python"]
