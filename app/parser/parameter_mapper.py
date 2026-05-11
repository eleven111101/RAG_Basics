import yaml

def load_parameter_mapping():
    with open(
        "app/config/parameter_mapping.yaml",
        "r",
        encoding="utf-8"
    ) as f:
        mapping = yaml.safe_load(f)
    return mapping


def normalize_parameters(parameters):
    mapping = load_parameter_mapping()
    normalized = {}
    for raw_key, value in parameters.items():
        canonical_key = mapping.get(
            raw_key,
            raw_key
        )
        normalized[canonical_key] = value
    return normalized