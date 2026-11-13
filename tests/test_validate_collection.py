import unittest

from scripts.validate_collection import SCHEMA_URI, validate_collection


def collection(items=None, variables=None):
    result = {
        "info": {"name": "Example", "schema": SCHEMA_URI},
        "item": items if items is not None else [],
    }
    if variables is not None:
        result["variable"] = variables
    return result


class ValidateCollectionTests(unittest.TestCase):
    def test_accepts_request_and_folder(self):
        data = collection(
            [
                {
                    "name": "Customers",
                    "item": [
                        {
                            "name": "List customers",
                            "request": {"method": "GET", "url": "https://api.example.invalid/customers"},
                        }
                    ],
                }
            ]
        )
        self.assertEqual(validate_collection(data), ([], []))

    def test_rejects_missing_request_method_and_url(self):
        data = collection([{"name": "Broken", "request": {}}])
        errors, _ = validate_collection(data)
        self.assertTrue(any("request.method" in error for error in errors))
        self.assertTrue(any("request.url" in error for error in errors))

    def test_duplicate_sibling_names_are_errors(self):
        request = {"method": "GET", "url": "https://api.example.invalid"}
        data = collection([{"name": "One", "request": request}, {"name": "One", "request": request}])
        errors, _ = validate_collection(data)
        self.assertTrue(any("duplicates sibling name" in error for error in errors))

    def test_environment_variable_is_a_warning_not_an_error(self):
        data = collection([{"name": "List", "request": {"method": "GET", "url": "{{baseUrl}}/items"}}])
        errors, warnings = validate_collection(data)
        self.assertEqual(errors, [])
        self.assertTrue(any("supplied by an environment" in warning for warning in warnings))

    def test_reports_variables_in_request_body(self):
        data = collection(
            [
                {
                    "name": "Create",
                    "request": {
                        "method": "POST",
                        "url": "https://api.example.invalid/items",
                        "body": {"mode": "raw", "raw": '{"id":"{{recordId}}"}'},
                    },
                }
            ]
        )
        _, warnings = validate_collection(data)
        self.assertTrue(any("recordId" in warning for warning in warnings))

    def test_rejects_wrong_schema_uri(self):
        data = collection()
        data["info"]["schema"] = "https://example.invalid/schema"
        errors, _ = validate_collection(data)
        self.assertTrue(any("info.schema" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
