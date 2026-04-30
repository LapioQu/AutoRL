from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = PROJECT_ROOT / "docs"


def test_phase11_required_docs_exist() -> None:
    required = [
        PROJECT_ROOT / "README.md",
        DOCS_DIR / "operations_manual.md",
        DOCS_DIR / "requirements_traceability.md",
        DOCS_DIR / "test_protocol.md",
        DOCS_DIR / "doc_01_use_case_diagram.md",
        DOCS_DIR / "doc_02_dfd_level_0.md",
        DOCS_DIR / "doc_03_component_diagram.md",
        DOCS_DIR / "doc_04_sequence_stay_switch.md",
        DOCS_DIR / "doc_05_state_machine.md",
        DOCS_DIR / "doc_06_er_schema.md",
        DOCS_DIR / "doc_07_deployment_diagram.md",
        DOCS_DIR / "doc_08_requirements_traceability.md",
        DOCS_DIR / "doc_09_moscow_requirements.md",
        DOCS_DIR / "doc_10_operational_instruction.md",
    ]
    missing = [str(path) for path in required if not path.exists()]
    assert not missing, f"missing required Phase 11 docs: {missing}"


def test_requirements_traceability_covers_all_required_groups() -> None:
    text = (DOCS_DIR / "requirements_traceability.md").read_text(encoding="utf-8")
    for group_name in (
        "Architecture Decisions",
        "Use Cases",
        "Functional Requirements",
        "Non-Functional Requirements",
        "UI Acceptance Criteria",
        "API Endpoints",
        "CLI Commands",
        "Storage Elements",
        "System and Experimental Validation Items",
        "Documentation Deliverables",
    ):
        assert group_name in text


def test_test_protocol_mentions_final_verification_scope() -> None:
    text = (DOCS_DIR / "test_protocol.md").read_text(encoding="utf-8")
    required_markers = (
        "Import Smoke",
        "Full pytest Regression",
        "CLI Smoke Matrix",
        "API Smoke Matrix",
        "UI Smoke Matrix",
        "Performance and Memory Checks",
        "Documentation Completeness Check",
    )
    for marker in required_markers:
        assert marker in text


def test_requirements_inventory_contains_doc_deliverables() -> None:
    text = (DOCS_DIR / "requirements_inventory.md").read_text(encoding="utf-8")
    for marker in ("DOC-01", "DOC-02", "DOC-03", "DOC-04", "DOC-05", "DOC-06", "DOC-07", "DOC-08", "DOC-09", "DOC-10"):
        assert marker in text
