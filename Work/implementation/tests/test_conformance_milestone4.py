"""Milestone 4 — conformance harness."""

from conformance.harness import run_harness, write_report


def test_conformance_harness_all_traces():
    report = run_harness()
    assert report.passed, report.to_json()
    ids = {r.trace_id for r in report.results}
    for i in range(1, 26):
        assert f"TR-INT-{i:02d}" in ids


def test_conformance_writes_machine_readable(tmp_path):
    path = tmp_path / "conformance_report.json"
    report = write_report(path)
    assert path.exists()
    assert report.passed
    assert '"passed": true' in path.read_text()
