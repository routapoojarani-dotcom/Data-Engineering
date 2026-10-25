from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_expected_repository_structure():
    expected = [
        "README.md",
        "ingestion/sqoop_import.sh",
        "src/pyspark_etl.py",
        "sql/01_schema.sql",
        "sql/02_load_templates.sql",
        "sql/03_analytical_queries.sql",
        "docs/DATA_MODEL.md",
        "docs/DATA_PROVENANCE.md",
        "docs/ENGINEERING_NOTES.md",
    ]

    missing = [path for path in expected if not (ROOT / path).exists()]
    assert not missing, f"Missing expected files: {missing}"


def test_public_sql_has_no_original_credentials():
    sql_text = "\n".join(
        (ROOT / "sql" / name).read_text(encoding="utf-8")
        for name in [
            "01_schema.sql",
            "02_load_templates.sql",
            "03_analytical_queries.sql",
        ]
    )

    assert "STUDENT123" not in sql_text
    assert "443061449916" not in sql_text
