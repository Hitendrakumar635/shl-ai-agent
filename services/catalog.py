import json
from pathlib import Path

CATALOG_FILE = Path("data/shl_product_catalog.json")


def load_catalog():
    """Load SHL Product Catalog"""
    with open(CATALOG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_all_assessments():
    """Return complete catalog"""
    return load_catalog()


def find_by_name(name: str):
    """Find assessment by name"""
    catalog = load_catalog()

    for assessment in catalog:
        if name.lower() in assessment.get("name", "").lower():
            return assessment

    return None


def get_assessment_names():
    """Return all assessment names"""
    catalog = load_catalog()

    return [
        assessment.get("name", "")
        for assessment in catalog
    ]