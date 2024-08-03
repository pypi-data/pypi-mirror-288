from datetime import timedelta
from typing import Optional, Sequence, Union

from chalk.features._encoding.outputs import find_feature_or_resolver_by_fqn
from chalk.utils.duration import parse_chalk_duration

# These are the maximum values that can be represented by a Duration proto.
MAX_DURATION_SECONDS = 315576000000
MAX_DURATION_NANOS = 999999999


def convert_raw_duration(duration: Union[str, timedelta]) -> timedelta:
    if isinstance(duration, str):
        duration = parse_chalk_duration(duration)
    return duration


def validate_namespaced_features(features: Optional[Sequence[str]]):
    if features is None:
        return None

    unique_namespace = set()

    for string_feature in features:
        if (feature := find_feature_or_resolver_by_fqn(string_feature)) is None:
            raise ValueError(f"Feature or resolver '{feature}' not found.")

        unique_namespace.add(string_feature.rsplit(".", maxsplit=1)[0])
    if len(unique_namespace) > 1:
        raise ValueError(f"Output features of named query must belong to the same namespace, but got: '{features}'.")
    return features
