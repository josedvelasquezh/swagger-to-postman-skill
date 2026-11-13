#!/usr/bin/env python3
"""Offline structural checks for Postman Collection v2.1 JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SCHEMA_URI = "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
VARIABLE_PATTERN = re.compile(r"\{\{\s*([^{}\s]+)\s*\}\}")


def validate_collection(data: Any) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for structural issues in a collection object."""
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["Top-level JSON value must be an object."], warnings

    info = data.get("info")
    if not isinstance(info, dict):
        errors.append("Missing required object: info.")
    else:
        if not isinstance(info.get("name"), str) or not info["name"].strip():
            errors.append("info.name must be a non-empty string.")
        if info.get("schema") != SCHEMA_URI:
            errors.append(f"info.schema must be {SCHEMA_URI}.")

    items = data.get("item")
    if not isinstance(items, list):
        errors.append("Missing required array: item.")
        return errors, warnings

    declared_variables: set[str] = set()
    variables = data.get("variable", [])
    if variables is not None:
        if not isinstance(variables, list):
            errors.append("variable must be an array when present.")
        else:
            for index, variable in enumerate(variables):
                if not isinstance(variable, dict) or not isinstance(variable.get("key"), str):
                    errors.append(f"variable[{index}] must be an object with a string key.")
                else:
                    declared_variables.add(variable["key"])

    request_count = 0

    def visit(group: list[Any], location: str) -> None:
        nonlocal request_count
        sibling_names: set[str] = set()
        for index, item in enumerate(group):
            item_location = f"{location}[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{item_location} must be an object.")
                continue
            name = item.get("name")
            if not isinstance(name, str) or not name.strip():
                errors.append(f"{item_location}.name must be a non-empty string.")
            elif name in sibling_names:
                errors.append(f"{item_location} duplicates sibling name {name!r}.")
            else:
                sibling_names.add(name)

            if "request" in item:
                request_count += 1
                request = item["request"]
                if not isinstance(request, dict):
                    errors.append(f"{item_location}.request must be an object.")
                    continue
                method = request.get("method")
                if not isinstance(method, str) or not method.strip():
                    errors.append(f"{item_location}.request.method must be a non-empty string.")
                url = request.get("url")
                if isinstance(url, str):
                    url_text = url
                elif isinstance(url, dict):
                    raw = url.get("raw")
                    if isinstance(raw, str):
                        url_text = raw
                    else:
                        url_text = json.dumps(url, ensure_ascii=False)
                else:
                    url_text = ""
                if not url_text.strip():
                    errors.append(f"{item_location}.request.url must contain a URL or URL object.")
                else:
                    for variable_name in VARIABLE_PATTERN.findall(url_text):
                        if variable_name not in declared_variables:
                            warnings.append(
                                f"{item_location} uses {{{{{variable_name}}}}}, which is not declared "
                                "at collection scope; confirm it is supplied by an environment."
                            )
            elif "item" in item:
                children = item["item"]
                if not isinstance(children, list):
                    errors.append(f"{item_location}.item must be an array for a folder.")
                else:
                    visit(children, f"{item_location}.item")
            else:
                errors.append(f"{item_location} must contain either request or item.")

    visit(items, "item")
    if request_count == 0:
        warnings.append("Collection contains no requests.")
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("collection", type=Path, help="Path to Postman Collection v2.1 JSON")
    args = parser.parse_args(argv)

    try:
        with args.collection.open("r", encoding="utf-8") as source:
            data = json.load(source)
    except FileNotFoundError:
        print(f"ERROR: File not found: {args.collection}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"ERROR: Could not read {args.collection}: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate_collection(data)
    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")
    if errors:
        print(f"Validation failed with {len(errors)} error(s) and {len(warnings)} warning(s).")
        return 1
    print(f"Collection structure is valid ({len(warnings)} warning(s)).")
    print("This check does not validate live API behavior or full Postman import compatibility.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
