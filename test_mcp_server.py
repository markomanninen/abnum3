import unittest
import json
from mcp_server import app, AVAILABLE_CODES # Assuming AVAILABLE_CODES is accessible

# Manually define some codes for testing based on common abnum codes
# This is safer than relying on AVAILABLE_CODES directly if its population has issues
# or for more predictable tests.
TEST_GREEK_CODE = 'grc' # greek
TEST_HEBREW_CODE = 'heb' # hebrew
TEST_ENGLISH_CODE = 'eng' # english


class TestMCPServer(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        # Ensure test codes are actually available in the app's context if dynamic
        # For now, we assume 'grc', 'heb', 'eng' are generally available in abnum
        global AVAILABLE_CODES
        if not AVAILABLE_CODES: # If mcp_server.AVAILABLE_CODES was empty for some reason
            AVAILABLE_CODES = [TEST_GREEK_CODE, TEST_HEBREW_CODE, TEST_ENGLISH_CODE]


    def _post_json(self, endpoint, data):
        return self.app.post(endpoint,
                             data=json.dumps(data),
                             content_type='application/json')

    # 4. Test calculate_value (success cases)
    def test_calculate_value_add(self):
        payload = {
            "tool_name": "calculate_value",
            "parameters": {
                "text": "Logos",
                "code": TEST_GREEK_CODE,
                "operation": "add"
            }
        }
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(data.get("result", {}).get("value"))
        self.assertIsNone(data.get("error"))
        # Value for "Logos" in Greek: L(30) + o(70) + g(3) + o(70) + s(200) = 373
        self.assertEqual(data["result"]["value"], 373)

    def test_calculate_value_multiply(self):
        payload = {
            "tool_name": "calculate_value",
            "parameters": {
                "text": "Ace", # A=1, c=3, e=5 (using 'eng' simple mapping for test)
                "code": TEST_ENGLISH_CODE, # Assuming 'eng' uses a simple 1-26 or similar
                "operation": "multiply"
            }
        }
        # Need to know the exact values for 'eng' code in abnum to verify
        # For 'eng' as defined in letter_value.py: a=1, c=3, e=5. 1*3*5 = 15
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(data.get("result", {}).get("value"))
        self.assertIsNone(data.get("error"))
        self.assertEqual(data["result"]["value"], 15) # 1 * 3 * 5 = 15 for "Ace"

    def test_calculate_value_different_code(self):
        # Aleph=1, Beth=2, Gimel=3. 1+2+3 = 6
        payload = {
            "tool_name": "calculate_value",
            "parameters": {
                "text": "אבג", # Aleph, Beth, Gimel
                "code": TEST_HEBREW_CODE,
                "operation": "add"
            }
        }
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(data.get("result", {}).get("value"))
        self.assertIsNone(data.get("error"))
        self.assertEqual(data["result"]["value"], 6)

    # 5. Test find_text_by_value (success cases)
    def test_find_text_by_value_non_cumulative(self):
        payload = {
            "tool_name": "find_text_by_value",
            "parameters": {
                "text": "one two three one four", # o:2,n:1,e:5->8; t:7,w:4,o:2->13; t:7,h:6,r:5,e:5,e:5->28; f:6,o:2,u:6,r:5->19
                "target_value": 8, # Value of "one" with 'eng' code (2+1+5=8)
                "code": TEST_ENGLISH_CODE,
                "cumulative": False
            }
        }
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(data.get("result", {}).get("matches"))
        self.assertIsNone(data.get("error"))
        self.assertEqual(data["result"]["matches"], ["one", "one"])

    def test_find_text_by_value_cumulative(self):
        # Using Greek: o(70) Λογος(373) εστι(285) το(370) φως(1500)
        # o + Logos = 70 + 373 = 443
        payload = {
            "tool_name": "find_text_by_value",
            "parameters": {
                "text": "o Λογος εστι το φως",
                "target_value": 443,
                "code": TEST_GREEK_CODE,
                "cumulative": True
            }
        }
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(data.get("result", {}).get("matches"))
        self.assertIsNone(data.get("error"))
        self.assertIn("o Λογος", data["result"]["matches"])

    def test_find_text_by_value_no_matches(self):
        payload = {
            "tool_name": "find_text_by_value",
            "parameters": {
                "text": "word test",
                "target_value": 9999,
                "code": TEST_ENGLISH_CODE,
                "cumulative": False
            }
        }
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(data["result"]["matches"], [])
        self.assertIsNone(data.get("error"))

    # 6. Test Error Conditions
    def test_invalid_tool_name(self):
        payload = {"tool_name": "non_existent_tool", "parameters": {}}
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNone(data.get("result"))
        # Server checks for empty parameters first if all tools require non-empty params
        self.assertIn("Missing parameters", data.get("error", ""))

    def test_missing_tool_name(self):
        payload = {"parameters": {}}
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNone(data.get("result"))
        self.assertEqual(data.get("error"), "Missing tool_name")

    def test_missing_parameters_top_level(self):
        payload = {"tool_name": "calculate_value"} # Missing "parameters" field
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 400) # Based on current server logic
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNone(data.get("result"))
        self.assertEqual(data.get("error"), "Missing parameters")


    def test_calculate_value_missing_params_text(self):
        payload = {"tool_name": "calculate_value", "parameters": {"code": TEST_GREEK_CODE}}
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNone(data.get("result"))
        self.assertIn("Missing 'text' or 'code'", data.get("error", ""))

    def test_calculate_value_missing_params_code(self):
        payload = {"tool_name": "calculate_value", "parameters": {"text": "hello"}}
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNone(data.get("result"))
        self.assertIn("Missing 'text' or 'code'", data.get("error", ""))

    def test_calculate_value_invalid_code(self):
        payload = {
            "tool_name": "calculate_value",
            "parameters": {"text": "hello", "code": "invalid_code"}
        }
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNone(data.get("result"))
        self.assertTrue(data.get("error", "").startswith("Invalid code 'invalid_code'."))

    def test_calculate_value_invalid_operation(self):
        payload = {
            "tool_name": "calculate_value",
            "parameters": {"text": "hello", "code": TEST_GREEK_CODE, "operation": "subtract"}
        }
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNone(data.get("result"))
        self.assertEqual(data.get("error"), "Invalid operation 'subtract'. Must be 'add' or 'multiply'.")

    def test_find_text_by_value_missing_params_text(self):
        payload = {
            "tool_name": "find_text_by_value",
            "parameters": {"target_value": 10, "code": TEST_GREEK_CODE}
        }
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNone(data.get("result"))
        self.assertIn("Missing 'text', 'target_value', or 'code'", data.get("error", ""))

    def test_find_text_by_value_missing_params_target(self):
        payload = {
            "tool_name": "find_text_by_value",
            "parameters": {"text": "sample", "code": TEST_GREEK_CODE}
        }
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNone(data.get("result"))
        self.assertIn("Missing 'text', 'target_value', or 'code'", data.get("error", ""))

    def test_find_text_by_value_missing_params_code(self):
        payload = {
            "tool_name": "find_text_by_value",
            "parameters": {"text": "sample", "target_value": 10}
        }
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNone(data.get("result"))
        self.assertIn("Missing 'text', 'target_value', or 'code'", data.get("error", ""))

    def test_find_text_by_value_invalid_code(self):
        payload = {
            "tool_name": "find_text_by_value",
            "parameters": {"text": "hello", "target_value": 10, "code": "invalid_code"}
        }
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNone(data.get("result"))
        self.assertTrue(data.get("error", "").startswith("Invalid code 'invalid_code'."))

    def test_find_text_by_value_invalid_target_type(self):
        payload = {
            "tool_name": "find_text_by_value",
            "parameters": {"text": "hello", "target_value": "10", "code": TEST_GREEK_CODE} # target_value is string
        }
        response = self._post_json('/invoke_tool', payload)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNone(data.get("result"))
        self.assertEqual(data.get("error"), "'target_value' must be an integer.")

    def test_abnum_exception_calculate_value(self):
        payload = {
            "tool_name": "calculate_value",
            "parameters": {"text": "text123", "code": TEST_GREEK_CODE} # Contains numbers
        }
        response = self._post_json('/invoke_tool', payload)
        # The server catches AbnumException and returns a JSON error, still with 200 OK for the HTTP request itself
        # as the API call was successful, but the operation within failed predictably.
        # If we want 500 or 4xx for this, server logic needs change. Current server returns error string in JSON.
        self.assertEqual(response.status_code, 200) # Server handles it, returns JSON error
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNone(data.get("result"))
        expected_error_msg = f"String 'text123' contains unsupported characters for the letter value calculation."
        self.assertEqual(data.get("error"), expected_error_msg)

if __name__ == '__main__':
    unittest.main()
