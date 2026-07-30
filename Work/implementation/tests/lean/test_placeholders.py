"""Placeholder scanner tests."""

from system_b.lean.placeholders import scan_text


def test_detects_sorry():
    f = scan_text("theorem t : True := by\n  sorry\n")
    assert any(x.kind == "sorry" for x in f)


def test_ignores_comment_sorry():
    f = scan_text("-- sorry\ntheorem t : True := trivial\n")
    assert not any(x.kind == "sorry" for x in f)


def test_block_comment():
    f = scan_text("/-\n sorry \n-/\ntheorem t : True := trivial\n")
    assert not any(x.kind == "sorry" for x in f)


def test_detects_constant_bypass():
    f = scan_text("constant Evil : False\n")
    assert any(x.kind == "constant" for x in f)


def test_detects_string_not_code_sorry():
    f = scan_text('def msg := "sorry"\ntheorem t : True := trivial\n')
    assert not any(x.kind == "sorry" for x in f)


def test_zero_width_sorry():
    f = scan_text("theorem t : True := by\n  sor\u200bry\n")
    assert any(x.kind == "sorry" for x in f)

