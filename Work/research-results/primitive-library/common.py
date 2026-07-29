#!/usr/bin/env python3
"""Shared Primitive Operator Library validation and index builders.

Fail closed: every error is fatal. No silent warnings.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

LIBRARY_SCHEMA_VERSION = "primitive-library-1.0"
OPERATOR_STATUSES = frozenset(
    {"planned", "in_progress", "complete", "reserved_reference"}
)
THEOREM_ROLES = frozenset(
    {
        "primary_stability",
        "sharpness",
        "bounded_noise_companion",
        "supporting_lemma_bundle",
        "reference_only",
    }
)
GUARANTEE_KINDS = frozenset(
    {"deterministic", "probabilistic", "almost_sure", "mixed"}
)
PRIMITIVE_TYPES = frozenset(
    {
        "scalar_selection",
        "ordering",
        "projection",
        "primitive_search",
        "greedy",
        "reserved_optimization",
    }
)
LEAN_STATUSES = frozenset(
    {"LEAN_FULL", "LEAN_PARTIAL", "LEAN_BLOCKED", "LEAN_ABSENT", "UNKNOWN"}
)
_HEX64 = re.compile(r"^[a-f0-9]{64}$")
_THEOREM_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
_MODULE = re.compile(r"^Research\.[A-Za-z0-9_.]+$")


def library_dir() -> Path:
    return Path(__file__).resolve().parent


def repo_root() -> Path:
    return library_dir().parents[1]


def results_root() -> Path:
    return repo_root() / "research-results"


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        raise ValueError(f"missing_file:{path}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"malformed_json:{path}:{e}") from e


def dump_canonical(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def write_canonical(path: Path, obj: Any) -> None:
    path.write_text(dump_canonical(obj), encoding="utf-8")


def lean_module_to_path(module: str, lean_root: Path) -> Path:
    if not module.startswith("Research."):
        raise ValueError(f"invalid_lean_module:{module}")
    rel = Path(*module.split("."))
    return lean_root / f"{rel}.lean"


def discover_theorem_packages(root: Path | None = None) -> list[Path]:
    """Non-archive metadata.json under research-results/<op>/<thm>/."""
    root = root or results_root()
    out: list[Path] = []
    for meta in sorted(root.glob("*/*/metadata.json")):
        if "_archive" in meta.parts:
            continue
        if meta.parent.parent.name == "primitive-library":
            continue
        # path: research-results/<operator>/<theorem>/metadata.json
        if len(meta.relative_to(root).parts) != 3:
            continue
        out.append(meta)
    return out


def _require(cond: bool, err: str, errors: list[str]) -> None:
    if not cond:
        errors.append(err)


def validate_operators_registry(
    registry: dict[str, Any], *, packages_by_operator: dict[str, list[Path]]
) -> list[str]:
    errors: list[str] = []
    _require(
        registry.get("schema_version") == LIBRARY_SCHEMA_VERSION,
        f"operators.schema_version_expected_{LIBRARY_SCHEMA_VERSION}",
        errors,
    )
    ops = registry.get("operators")
    if not isinstance(ops, list) or not ops:
        return errors + ["operators.operators_missing_or_empty"]

    seen_ids: set[str] = set()
    sequences: dict[int, str] = {}
    for i, entry in enumerate(ops):
        prefix = f"operators[{i}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix}:not_object")
            continue
        oid = entry.get("operator_id")
        if not isinstance(oid, str) or not oid:
            errors.append(f"{prefix}:operator_id_invalid")
            continue
        if oid in seen_ids:
            errors.append(f"duplicate_operator_id:{oid}")
        seen_ids.add(oid)

        status = entry.get("status")
        _require(status in OPERATOR_STATUSES, f"{oid}:invalid_status:{status}", errors)
        reserved = entry.get("reserved")
        implemented = entry.get("implemented")
        theorem_count = entry.get("theorem_count")
        family = entry.get("family")
        sequence = entry.get("sequence")

        _require(isinstance(reserved, bool), f"{oid}:reserved_not_bool", errors)
        _require(isinstance(implemented, bool), f"{oid}:implemented_not_bool", errors)
        _require(
            isinstance(theorem_count, int) and theorem_count >= 0,
            f"{oid}:theorem_count_invalid",
            errors,
        )
        _require(family in PRIMITIVE_TYPES, f"{oid}:invalid_family:{family}", errors)
        _require(
            isinstance(entry.get("display_name"), str) and entry["display_name"],
            f"{oid}:display_name_invalid",
            errors,
        )
        _require(
            isinstance(entry.get("description"), str) and entry["description"],
            f"{oid}:description_invalid",
            errors,
        )

        if status == "reserved_reference":
            _require(reserved is True, f"{oid}:reserved_reference_requires_reserved", errors)
            _require(
                implemented is False,
                f"{oid}:reserved_reference_must_not_be_implemented",
                errors,
            )
            _require(sequence is None, f"{oid}:reserved_reference_sequence_must_be_null", errors)
        else:
            _require(reserved is False, f"{oid}:non_reserved_status_with_reserved", errors)
            _require(
                isinstance(sequence, int) and sequence >= 1,
                f"{oid}:sequence_invalid",
                errors,
            )
            if isinstance(sequence, int):
                if sequence in sequences:
                    errors.append(
                        f"duplicate_sequence:{sequence}:{sequences[sequence]}:{oid}"
                    )
                else:
                    sequences[sequence] = oid

        if status == "complete":
            _require(implemented is True, f"{oid}:complete_requires_implemented", errors)
            pkgs = packages_by_operator.get(oid, [])
            _require(
                theorem_count == len(pkgs),
                f"{oid}:theorem_count_mismatch:registry={theorem_count}:packages={len(pkgs)}",
                errors,
            )
            _require(len(pkgs) >= 1, f"{oid}:complete_requires_packages", errors)
        elif status == "planned":
            _require(implemented is False, f"{oid}:planned_must_not_be_implemented", errors)
            _require(theorem_count == 0, f"{oid}:planned_theorem_count_must_be_0", errors)
            pkgs = packages_by_operator.get(oid, [])
            _require(
                len(pkgs) == 0,
                f"{oid}:planned_must_have_no_packages:{len(pkgs)}",
                errors,
            )
        elif status == "in_progress":
            pkgs = packages_by_operator.get(oid, [])
            _require(
                theorem_count == len(pkgs),
                f"{oid}:theorem_count_mismatch:registry={theorem_count}:packages={len(pkgs)}",
                errors,
            )

        if status != "reserved_reference":
            # In-scope packages must not appear under reserved-only ids.
            pass

    # Packages whose operator is absent from registry (except reserved scanned separately)
    for oid, pkgs in packages_by_operator.items():
        if oid not in seen_ids:
            for p in pkgs:
                errors.append(f"package_operator_not_in_registry:{oid}:{p}")

    return errors


def _validate_authored(
    authored: Any, *, operator: str, theorem_id: str, prefix: str, errors: list[str]
) -> None:
    if not isinstance(authored, dict):
        errors.append(f"{prefix}:authored_not_object")
        return
    for key in (
        "operator",
        "theorem",
        "assumptions",
        "perturbation_model",
        "theorem_role",
        "proof_strategy",
        "limitations",
        "references",
        "lean_theorem_names",
    ):
        _require(key in authored, f"{prefix}:authored.missing:{key}", errors)

    _require(authored.get("operator") == operator, f"{prefix}:authored.operator_mismatch", errors)
    _require(
        authored.get("theorem") == theorem_id, f"{prefix}:authored.theorem_mismatch", errors
    )
    _require(
        authored.get("theorem_role") in THEOREM_ROLES,
        f"{prefix}:authored.invalid_theorem_role:{authored.get('theorem_role')}",
        errors,
    )
    _require(
        isinstance(authored.get("perturbation_model"), str)
        and authored["perturbation_model"],
        f"{prefix}:authored.perturbation_model_invalid",
        errors,
    )
    _require(
        isinstance(authored.get("proof_strategy"), str) and authored["proof_strategy"],
        f"{prefix}:authored.proof_strategy_invalid",
        errors,
    )
    for list_key in ("assumptions", "limitations"):
        val = authored.get(list_key)
        _require(
            isinstance(val, list) and val and all(isinstance(x, str) and x for x in val),
            f"{prefix}:authored.{list_key}_invalid",
            errors,
        )
    refs = authored.get("references")
    _require(
        isinstance(refs, list) and all(isinstance(x, str) and x for x in refs),
        f"{prefix}:authored.references_invalid",
        errors,
    )
    names = authored.get("lean_theorem_names")
    _require(
        isinstance(names, list)
        and names
        and all(isinstance(x, str) and _THEOREM_NAME.match(x) for x in names)
        and len(names) == len(set(names)),
        f"{prefix}:authored.lean_theorem_names_invalid",
        errors,
    )


def _validate_derived(
    derived: Any,
    *,
    meta: dict[str, Any],
    prefix: str,
    errors: list[str],
    repo: Path,
) -> None:
    if not isinstance(derived, dict):
        errors.append(f"{prefix}:derived_not_object")
        return
    for key in (
        "lean_status",
        "statement_digest",
        "proof_digest",
        "certificate_path",
        "placeholder_count",
        "axiom_summary",
        "provenance",
        "verification_timestamp",
    ):
        _require(key in derived, f"{prefix}:derived.missing:{key}", errors)

    status = derived.get("lean_status")
    _require(status in LEAN_STATUSES, f"{prefix}:derived.invalid_lean_status:{status}", errors)
    _require(
        status == meta.get("derived_lean_status"),
        f"{prefix}:derived.lean_status_mismatch_top_level",
        errors,
    )
    for dig_key in ("statement_digest", "proof_digest"):
        dig = derived.get(dig_key)
        _require(
            isinstance(dig, str) and bool(_HEX64.match(dig)),
            f"{prefix}:derived.{dig_key}_invalid",
            errors,
        )
    cert = derived.get("certificate_path")
    _require(
        isinstance(cert, str) and cert.startswith("lean/certificates/"),
        f"{prefix}:derived.certificate_path_invalid",
        errors,
    )
    _require(
        cert == meta.get("lean_certificate_dir"),
        f"{prefix}:derived.certificate_path_mismatch_top_level",
        errors,
    )
    cert_dir = repo / cert if isinstance(cert, str) else None
    if cert_dir is not None:
        _require(cert_dir.is_dir(), f"{prefix}:certificate_dir_missing:{cert}", errors)
        for required in (
            "lean_manifest.json",
            "status_recomputed.json",
            "verifier_transcript.json",
        ):
            _require(
                (cert_dir / required).is_file(),
                f"{prefix}:certificate_file_missing:{cert}/{required}",
                errors,
            )

    _require(
        isinstance(derived.get("placeholder_count"), int)
        and derived["placeholder_count"] >= 0,
        f"{prefix}:derived.placeholder_count_invalid",
        errors,
    )

    ax = derived.get("axiom_summary")
    if not isinstance(ax, dict):
        errors.append(f"{prefix}:derived.axiom_summary_not_object")
    else:
        for k in (
            "imported_axiom_closure_sorted",
            "custom_axiom_ids_sorted",
            "axiom_closure_captured",
        ):
            _require(k in ax, f"{prefix}:derived.axiom_summary.missing:{k}", errors)
        _require(
            isinstance(ax.get("imported_axiom_closure_sorted"), list),
            f"{prefix}:derived.axiom_summary.imported_invalid",
            errors,
        )
        _require(
            isinstance(ax.get("custom_axiom_ids_sorted"), list),
            f"{prefix}:derived.axiom_summary.custom_invalid",
            errors,
        )
        _require(
            isinstance(ax.get("axiom_closure_captured"), bool),
            f"{prefix}:derived.axiom_summary.captured_invalid",
            errors,
        )

    prov = derived.get("provenance")
    if not isinstance(prov, dict):
        errors.append(f"{prefix}:derived.provenance_not_object")
    else:
        for k in (
            "lean_manifest_digest",
            "claim_digest",
            "entry_module_id",
            "store_kind",
        ):
            _require(k in prov, f"{prefix}:derived.provenance.missing:{k}", errors)
        _require(
            isinstance(prov.get("lean_manifest_digest"), str)
            and bool(_HEX64.match(prov["lean_manifest_digest"])),
            f"{prefix}:derived.provenance.lean_manifest_digest_invalid",
            errors,
        )
        _require(
            prov.get("lean_manifest_digest") == meta.get("lean_manifest_digest"),
            f"{prefix}:derived.provenance.digest_mismatch_top_level",
            errors,
        )
        _require(
            isinstance(prov.get("claim_digest"), str)
            and bool(_HEX64.match(prov["claim_digest"])),
            f"{prefix}:derived.provenance.claim_digest_invalid",
            errors,
        )
        _require(
            prov.get("entry_module_id") == meta.get("lean_entry_module"),
            f"{prefix}:derived.provenance.entry_module_mismatch",
            errors,
        )

    ts = derived.get("verification_timestamp")
    _require(
        ts is None or (isinstance(ts, str) and bool(ts)),
        f"{prefix}:derived.verification_timestamp_invalid",
        errors,
    )

    # Cross-check certificate contents when present
    if cert_dir is not None and cert_dir.is_dir():
        try:
            manifest = load_json(cert_dir / "lean_manifest.json")
            status_obj = load_json(cert_dir / "status_recomputed.json")
        except ValueError as e:
            errors.append(f"{prefix}:certificate_unreadable:{e}")
            return
        _require(
            status_obj.get("derived_lean_status") == status,
            f"{prefix}:status_recomputed_mismatch:{status_obj.get('derived_lean_status')}",
            errors,
        )
        _require(
            manifest.get("manifest_digest") == meta.get("lean_manifest_digest"),
            f"{prefix}:manifest_digest_mismatch_certificate",
            errors,
        )
        transcript = manifest.get("transcript") or {}
        if isinstance(derived.get("statement_digest"), str):
            _require(
                derived["statement_digest"] == transcript.get("lean_statement_digest"),
                f"{prefix}:statement_digest_mismatch_certificate",
                errors,
            )
        if isinstance(derived.get("proof_digest"), str):
            _require(
                derived["proof_digest"] == transcript.get("proof_tree_digest"),
                f"{prefix}:proof_digest_mismatch_certificate",
                errors,
            )
        if isinstance(ax, dict):
            _require(
                ax.get("imported_axiom_closure_sorted")
                == transcript.get("imported_axiom_closure_sorted"),
                f"{prefix}:axiom_imported_mismatch_certificate",
                errors,
            )
            _require(
                ax.get("custom_axiom_ids_sorted")
                == transcript.get("custom_axiom_ids_sorted"),
                f"{prefix}:axiom_custom_mismatch_certificate",
                errors,
            )
            _require(
                ax.get("axiom_closure_captured")
                == transcript.get("axiom_closure_captured"),
                f"{prefix}:axiom_captured_mismatch_certificate",
                errors,
            )
        if isinstance(prov, dict):
            _require(
                prov.get("claim_digest") == manifest.get("claim_digest"),
                f"{prefix}:claim_digest_mismatch_certificate",
                errors,
            )
            _require(
                prov.get("store_kind") == manifest.get("store_kind"),
                f"{prefix}:store_kind_mismatch_certificate",
                errors,
            )


def _validate_library(library: Any, *, prefix: str, errors: list[str]) -> None:
    if not isinstance(library, dict):
        errors.append(f"{prefix}:library_not_object")
        return
    for key in (
        "primitive_type",
        "selected_object",
        "instability_mechanism",
        "structural_stability_quantity",
        "perturbation_class",
        "guarantee_kind",
        "stable_region",
        "unstable_region",
        "sharpness",
        "compositional_properties",
        "related_operators",
        "assumptions",
        "limitations",
    ):
        _require(key in library, f"{prefix}:library.missing:{key}", errors)

    _require(
        library.get("primitive_type") in PRIMITIVE_TYPES,
        f"{prefix}:library.invalid_primitive_type:{library.get('primitive_type')}",
        errors,
    )
    _require(
        library.get("guarantee_kind") in GUARANTEE_KINDS,
        f"{prefix}:library.invalid_guarantee_kind:{library.get('guarantee_kind')}",
        errors,
    )
    _require(
        isinstance(library.get("sharpness"), bool),
        f"{prefix}:library.sharpness_not_bool",
        errors,
    )
    for sk in (
        "selected_object",
        "instability_mechanism",
        "structural_stability_quantity",
        "perturbation_class",
        "stable_region",
        "unstable_region",
    ):
        _require(
            isinstance(library.get(sk), str) and library[sk],
            f"{prefix}:library.{sk}_invalid",
            errors,
        )
    for lk in ("compositional_properties", "related_operators", "assumptions", "limitations"):
        val = library.get(lk)
        _require(
            isinstance(val, list) and all(isinstance(x, str) and x for x in val),
            f"{prefix}:library.{lk}_invalid",
            errors,
        )
    _require(
        isinstance(library.get("assumptions"), list) and bool(library.get("assumptions")),
        f"{prefix}:library.assumptions_empty",
        errors,
    )
    _require(
        isinstance(library.get("limitations"), list) and bool(library.get("limitations")),
        f"{prefix}:library.limitations_empty",
        errors,
    )


def validate_package_metadata(
    meta: dict[str, Any],
    *,
    path: Path,
    repo: Path | None = None,
    require_library_schema: bool,
) -> list[str]:
    """Validate one theorem metadata.json.

    When require_library_schema is False (reserved_reference packages), only
    legacy identity fields are checked so Argmax can remain reference-only
    without a full library migration.
    """
    errors: list[str] = []
    repo = repo or repo_root()
    try:
        prefix = str(path.resolve().relative_to(repo.resolve()))
    except ValueError:
        prefix = str(path)

    if not isinstance(meta, dict):
        return [f"{prefix}:metadata_not_object"]

    operator = meta.get("operator")
    crp = meta.get("crp_identifiers")
    if not isinstance(crp, dict):
        errors.append(f"{prefix}:crp_identifiers_missing")
        theorem_id = None
    else:
        theorem_id = crp.get("theorem_id")
        _require(
            crp.get("operator") == operator,
            f"{prefix}:crp.operator_mismatch",
            errors,
        )

    parent_op = path.parent.parent.name
    parent_thm = path.parent.name
    _require(operator == parent_op, f"{prefix}:operator_path_mismatch:{operator}", errors)

    authority = meta.get("math_authority")
    if meta.get("packaging") and isinstance(authority, str):
        # Packaging hop: the directory names the hop, the theorem_id stays with the
        # math authority package that owns the mathematics and the certificate.
        rel = authority.strip("/")
        _require(
            rel.startswith("research-results/")
            and (repo / rel / "metadata.json").is_file(),
            f"{prefix}:math_authority_package_missing:{authority}",
            errors,
        )
        _require(
            theorem_id == Path(rel).name,
            f"{prefix}:theorem_id_not_math_authority:{theorem_id}",
            errors,
        )
    else:
        _require(
            theorem_id == parent_thm, f"{prefix}:theorem_path_mismatch:{theorem_id}", errors
        )

    if not require_library_schema:
        _require(
            isinstance(meta.get("derived_lean_status"), str),
            f"{prefix}:legacy.derived_lean_status_missing",
            errors,
        )
        _require(
            isinstance(meta.get("lean_entry_module"), str)
            and bool(_MODULE.match(meta["lean_entry_module"])),
            f"{prefix}:legacy.lean_entry_module_invalid",
            errors,
        )
        _require(
            isinstance(meta.get("lean_certificate_dir"), str)
            and meta["lean_certificate_dir"].startswith("lean/certificates/"),
            f"{prefix}:legacy.lean_certificate_dir_invalid",
            errors,
        )
        cert = repo / meta["lean_certificate_dir"]
        _require(cert.is_dir(), f"{prefix}:legacy.certificate_missing", errors)
        lean_path = lean_module_to_path(meta["lean_entry_module"], repo / "lean")
        _require(lean_path.is_file(), f"{prefix}:legacy.lean_module_missing:{lean_path}", errors)
        return errors

    _require(
        meta.get("library_schema_version") == LIBRARY_SCHEMA_VERSION,
        f"{prefix}:library_schema_version_invalid",
        errors,
    )
    _require(
        meta.get("derived_lean_status") in LEAN_STATUSES,
        f"{prefix}:derived_lean_status_invalid",
        errors,
    )
    _require(
        isinstance(meta.get("lean_entry_module"), str)
        and bool(_MODULE.match(meta["lean_entry_module"])),
        f"{prefix}:lean_entry_module_invalid",
        errors,
    )
    _require(
        isinstance(meta.get("lean_manifest_digest"), str)
        and bool(_HEX64.match(meta["lean_manifest_digest"])),
        f"{prefix}:lean_manifest_digest_invalid",
        errors,
    )
    _require(
        isinstance(meta.get("title"), str) and meta["title"],
        f"{prefix}:title_invalid",
        errors,
    )

    lean_path = lean_module_to_path(meta["lean_entry_module"], repo / "lean")
    _require(lean_path.is_file(), f"{prefix}:lean_module_file_missing:{lean_path}", errors)

    _validate_authored(
        meta.get("authored"),
        operator=str(operator),
        theorem_id=str(theorem_id),
        prefix=prefix,
        errors=errors,
    )
    _validate_derived(
        meta.get("derived"), meta=meta, prefix=prefix, errors=errors, repo=repo
    )
    _validate_library(meta.get("library"), prefix=prefix, errors=errors)

    # Lean theorem declarations must exist in the module source
    authored = meta.get("authored")
    if isinstance(authored, dict) and lean_path.is_file():
        src = lean_path.read_text(encoding="utf-8")
        for name in authored.get("lean_theorem_names") or []:
            if not isinstance(name, str):
                continue
            pat = re.compile(rf"(?:theorem|lemma)\s+{re.escape(name)}\b")
            _require(
                bool(pat.search(src)),
                f"{prefix}:lean_theorem_missing:{name}",
                errors,
            )

    # Optional until migrated; when present, enforce paper_card contract
    card = meta.get("paper_card")
    if card is not None:
        errors.extend(_validate_paper_card(card, prefix=prefix, pkg=path.parent, operator=str(operator)))

    return errors


def _validate_paper_card(
    card: Any, *, prefix: str, pkg: Path, operator: str
) -> list[str]:
    errors: list[str] = []
    if not isinstance(card, dict):
        return [f"{prefix}:paper_card_not_object"]
    _require(card.get("layout") == "operator-stability-v1", f"{prefix}:paper_card.layout", errors)
    _require(
        card.get("fundamentality") in {"primitive", "derived", "reduction"},
        f"{prefix}:paper_card.fundamentality",
        errors,
    )
    _require(isinstance(card.get("dependencies"), list), f"{prefix}:paper_card.dependencies", errors)
    verified = card.get("verified")
    if not isinstance(verified, dict):
        errors.append(f"{prefix}:paper_card.verified_missing")
    else:
        _require(verified.get("lean_status") == "LEAN_FULL", f"{prefix}:paper_card.verified.status", errors)
        _require(verified.get("domain") == "REAL_MATHLIB", f"{prefix}:paper_card.verified.domain", errors)
    pdf = pkg / f"{operator.replace('-', '_')}_paper.pdf"
    _require(pdf.is_file(), f"{prefix}:operator_paper_pdf_missing:{pdf.name}", errors)
    tex = pkg / "paper.tex"
    if tex.is_file():
        body = tex.read_text(encoding="utf-8")
        for title in (
            "Problem",
            "Stability notion",
            "Definitions",
            "Theorem",
            "Intuition",
            "Examples",
            "Proof",
            "Formal statement",
            "Proof dependencies",
            "Consequences",
        ):
            _require(
                f"\\section{{{title}}}" in body,
                f"{prefix}:paper_missing_section:{title}",
                errors,
            )
    else:
        errors.append(f"{prefix}:paper_tex_missing")
    return errors


def group_packages_by_operator(
    packages: list[Path],
) -> dict[str, list[Path]]:
    out: dict[str, list[Path]] = {}
    for p in packages:
        out.setdefault(p.parent.parent.name, []).append(p)
    return out


def registry_by_id(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {e["operator_id"]: e for e in registry["operators"] if isinstance(e, dict)}


def validate_all_metadata(
    *,
    repo: Path | None = None,
    library: Path | None = None,
) -> list[str]:
    repo = repo or repo_root()
    library = library or library_dir()
    errors: list[str] = []

    registry = load_json(library / "operators.json")
    packages = discover_theorem_packages(repo / "research-results")
    by_op = group_packages_by_operator(packages)
    errors.extend(validate_operators_registry(registry, packages_by_operator=by_op))

    ops = registry_by_id(registry)
    seen_theorem_ids: set[tuple[str, str]] = set()

    for meta_path in packages:
        meta = load_json(meta_path)
        operator = meta_path.parent.parent.name
        theorem_id = meta_path.parent.name
        key = (operator, theorem_id)
        if key in seen_theorem_ids:
            errors.append(f"duplicate_theorem_id:{operator}/{theorem_id}")
        seen_theorem_ids.add(key)

        entry = ops.get(operator)
        if entry is None:
            errors.append(f"package_without_registry_entry:{meta_path}")
            continue
        status = entry.get("status")
        require_full = status in {"complete", "in_progress"}
        # reserved_reference: legacy-only checks; planned should have no packages
        errors.extend(
            validate_package_metadata(
                meta,
                path=meta_path,
                repo=repo,
                require_library_schema=require_full,
            )
        )
        if status == "reserved_reference" and meta.get("library_schema_version"):
            # If someone migrates a reserved package, validate full schema too.
            errors.extend(
                validate_package_metadata(
                    meta,
                    path=meta_path,
                    repo=repo,
                    require_library_schema=True,
                )
            )

    return errors


def build_index(
    *,
    repo: Path | None = None,
    library: Path | None = None,
) -> dict[str, Any]:
    repo = repo or repo_root()
    library = library or library_dir()
    errors = validate_all_metadata(repo=repo, library=library)
    if errors:
        raise ValueError("validation_failed:\n" + "\n".join(errors))

    registry = load_json(library / "operators.json")
    packages = discover_theorem_packages(repo / "research-results")
    ops = registry_by_id(registry)

    theorems: list[dict[str, Any]] = []
    for meta_path in packages:
        meta = load_json(meta_path)
        operator = meta_path.parent.parent.name
        theorem_id = meta_path.parent.name
        entry = ops[operator]
        summary: dict[str, Any] = {
            "operator_id": operator,
            "theorem_id": theorem_id,
            "title": meta.get("title"),
            "operator_status": entry["status"],
            "lean_status": meta.get("derived_lean_status"),
            "lean_entry_module": meta.get("lean_entry_module"),
            "certificate_path": meta.get("lean_certificate_dir"),
            "lean_manifest_digest": meta.get("lean_manifest_digest"),
            "package_path": str(
                meta_path.parent.relative_to(repo / "research-results")
            ),
            "library_schema_version": meta.get("library_schema_version"),
        }
        if entry["status"] in {"complete", "in_progress"} and "library" in meta:
            summary["comparison"] = meta["library"]
            summary["authored"] = {
                "theorem_role": meta["authored"]["theorem_role"],
                "perturbation_model": meta["authored"]["perturbation_model"],
                "proof_strategy": meta["authored"]["proof_strategy"],
                "lean_theorem_names": meta["authored"]["lean_theorem_names"],
            }
            summary["derived"] = {
                "lean_status": meta["derived"]["lean_status"],
                "statement_digest": meta["derived"]["statement_digest"],
                "proof_digest": meta["derived"]["proof_digest"],
                "placeholder_count": meta["derived"]["placeholder_count"],
                "verification_timestamp": meta["derived"]["verification_timestamp"],
            }
            cert_ok = (repo / meta["lean_certificate_dir"] / "status_recomputed.json").is_file()
            summary["certificate_status"] = (
                "present_status_recomputed" if cert_ok else "missing"
            )
        else:
            summary["comparison"] = None
            summary["certificate_status"] = (
                "reference_legacy"
                if entry["status"] == "reserved_reference"
                else "absent"
            )
        theorems.append(summary)

    theorems.sort(key=lambda t: (t["operator_id"], t["theorem_id"]))

    operator_summaries = []
    for entry in sorted(registry["operators"], key=lambda e: (e["status"], e["operator_id"])):
        oid = entry["operator_id"]
        thms = [t for t in theorems if t["operator_id"] == oid]
        operator_summaries.append(
            {
                "operator_id": oid,
                "display_name": entry["display_name"],
                "status": entry["status"],
                "reserved": entry["reserved"],
                "implemented": entry["implemented"],
                "family": entry["family"],
                "sequence": entry["sequence"],
                "theorem_count_registry": entry["theorem_count"],
                "theorem_count_indexed": len(thms),
                "theorem_ids": [t["theorem_id"] for t in thms],
            }
        )

    return {
        "schema_version": LIBRARY_SCHEMA_VERSION,
        "generated_by": "research-results/primitive-library/generate_index.py",
        "operators": operator_summaries,
        "theorems": theorems,
        "counts": {
            "operators": len(operator_summaries),
            "theorems": len(theorems),
            "complete_operators": sum(
                1 for e in operator_summaries if e["status"] == "complete"
            ),
            "planned_operators": sum(
                1 for e in operator_summaries if e["status"] == "planned"
            ),
            "reserved_reference_operators": sum(
                1 for e in operator_summaries if e["status"] == "reserved_reference"
            ),
        },
    }


def validate_index_file(
    *,
    repo: Path | None = None,
    library: Path | None = None,
) -> list[str]:
    repo = repo or repo_root()
    library = library or library_dir()
    errors: list[str] = []
    index_path = library / "index.json"
    if not index_path.is_file():
        return [f"index_missing:{index_path}"]

    try:
        on_disk = load_json(index_path)
        expected = build_index(repo=repo, library=library)
    except ValueError as e:
        return [str(e)]

    on_disk_text = dump_canonical(on_disk)
    expected_text = dump_canonical(expected)
    if on_disk_text != expected_text:
        errors.append("index_not_deterministic_or_stale:regenerate_via_generate_index.py")

    _require(
        on_disk.get("schema_version") == LIBRARY_SCHEMA_VERSION,
        "index.schema_version_invalid",
        errors,
    )
    _require(isinstance(on_disk.get("operators"), list), "index.operators_missing", errors)
    _require(isinstance(on_disk.get("theorems"), list), "index.theorems_missing", errors)

    # Duplicate theorem ids inside index
    seen: set[tuple[str, str]] = set()
    for t in on_disk.get("theorems") or []:
        if not isinstance(t, dict):
            errors.append("index.theorem_not_object")
            continue
        key = (t.get("operator_id"), t.get("theorem_id"))
        if key in seen:
            errors.append(f"index.duplicate_theorem:{key[0]}/{key[1]}")
        seen.add(key)  # type: ignore[arg-type]

    return errors


def fail_if(errors: list[str], *, stream=sys.stderr) -> int:
    if not errors:
        return 0
    for e in errors:
        print(f"ERROR: {e}", file=stream)
    print(f"FAIL: {len(errors)} error(s)", file=stream)
    return 1
