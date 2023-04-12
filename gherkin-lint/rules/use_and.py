def run(feature: dict):
    errors = []

    child: dict
    for child in feature["children"]:
        node = child.get("rule") or child.get(
            "background") or child.get("scenario")
        previous_keyword = None

        if node["steps"]:
            for step in node["steps"]:
                keyword = step["keyword"].strip()
                if keyword == "And":
                    continue
                if keyword == previous_keyword:
                    errors.append(create_error(step))

                previous_keyword = keyword
    return errors


def create_error(step):
    return {
        "message": f"Step '{step['keyword']}{step['text']}' should use And instead of {step['keyword'].strip()}",
        "rule": "use_and",
        "line": step["location"]["line"]
    }
