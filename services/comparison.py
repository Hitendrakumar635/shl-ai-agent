from services.catalog import load_catalog

catalog = load_catalog()


def compare_assessments(query: str):

    query = query.lower()

    matches = []

    for item in catalog:

        if item["name"].lower() in query:
            matches.append(item)

    if len(matches) < 2:
        return None

    comparison = []

    for item in matches:

        comparison.append({

            "name": item["name"],

            "description": item.get("description", ""),

            "job_levels": ", ".join(item.get("job_levels", [])),

            "test_type": ", ".join(item.get("keys", [])),

            "url": item.get("link")
        })

    return comparison