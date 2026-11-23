"""Validate Schema v1 format without importing or running benchmark tests."""

import json
from pathlib import Path
import re
import sys

CATEGORIES = {
    "tensor_layout", "storage_aliasing", "tensor_metadata", "materialization",
    "autograd", "checkpointing", "graph_lifecycle", "optimizer_state",
    "compilation", "other",
}
FIELDS = {
    "schema_version", "bug_id", "issue_url", "target_api", "primary_category",
    "tags", "bug_type", "environment", "randomness", "expected_behavior",
    "bug_signature", "verification",
}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate(data, directory_name):
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    if not isinstance(data, dict):
        return ["metadata must be an object"]
    check(set(data) == FIELDS, "fields must match Schema v1 exactly")
    check(type(data.get("schema_version")) is int and data["schema_version"] == 1,
          "schema_version must be integer 1")
    for key in ("bug_id", "issue_url", "target_api", "primary_category",
                "bug_type", "expected_behavior", "bug_signature"):
        check(nonempty(data.get(key)), f"{key} must be a nonempty string")
    bug_id = data.get("bug_id")
    if isinstance(bug_id, str) and re.fullmatch(r"torch_[0-9]+", bug_id):
        check(bug_id == directory_name, "bug_id must match directory")
        check(data.get("issue_url") ==
              f"https://github.com/pytorch/pytorch/issues/{bug_id[6:]}",
              "issue_url must match bug_id")
    else:
        errors.append("bug_id must match torch_<issue_id>")
    category = data.get("primary_category")
    check(isinstance(category, str) and category in CATEGORIES,
          "primary_category is not allowed")
    tags = data.get("tags")
    valid_tags = isinstance(tags, list) and all(nonempty(t) for t in tags)
    check(valid_tags, "tags must be an array of nonempty strings")
    if valid_tags:
        check(len(tags) == len(set(tags)), "tags must be unique")
    check(data.get("randomness") is False, "randomness must be false")
    env = data.get("environment")
    if isinstance(env, dict):
        check(set(env) == {"torch", "python", "platform", "device"},
              "environment fields must be torch, python, platform, device")
        for key in ("torch", "platform", "device"):
            check(nonempty(env.get(key)), f"environment.{key} must be a string")
        check(env.get("python") is None or nonempty(env.get("python")),
              "environment.python must be a string or null (unknown)")
    else:
        errors.append("environment must be an object")
    verification = data.get("verification")
    if isinstance(verification, dict):
        check(set(verification) == {"runs", "passes", "review"},
              "verification fields must be runs, passes, review")
        runs, passes = verification.get("runs"), verification.get("passes")
        check(type(runs) is int and type(passes) is int and 0 <= passes <= runs,
              "verification requires integer 0 <= passes <= runs")
        check(verification.get("review") in ("pending", "approved", "rejected"),
              "review must be pending, approved, or rejected")
    else:
        errors.append("verification must be an object")
    return errors


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"invalid JSON constant: {value}")


def main():
    root = Path(__file__).resolve().parents[1]
    paths = ([Path(arg) for arg in sys.argv[1:]] if sys.argv[1:]
             else sorted((root / "bugs").rglob("metadata.json")))
    if not paths:
        print("FAIL: no metadata files found", file=sys.stderr)
        return 1
    failed = False
    if not sys.argv[1:]:
        cases = [p for p in (root / "bugs").rglob("torch_*") if p.is_dir()]
        case_dirs = set(cases)
        test_dirs = {p.parent for p in (root / "bugs").rglob("test_bug.py")}
        metadata_dirs = {p.parent for p in paths}
        if (len(cases) != 100 or len({p.name for p in cases}) != 100
                or case_dirs != test_dirs or case_dirs != metadata_dirs):
            print("FAIL: expected 100 unique cases, each with test_bug.py and metadata.json",
                  file=sys.stderr)
            failed = True
    for path in paths:
        try:
            data = json.loads(path.read_text(encoding="utf-8"),
                              object_pairs_hook=unique_object,
                              parse_constant=reject_constant)
            errors = validate(data, path.parent.name)
        except (OSError, ValueError) as exc:
            errors = [str(exc)]
        failed |= bool(errors)
        print(f"{'FAIL' if errors else 'OK'}: {path}")
        for error in errors:
            print(f"  {error}")
    print(f"Validated {len(paths)} metadata files: {'FAIL' if failed else 'OK'}")
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
