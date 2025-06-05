# MCP Server API Documentation

## Overview

The MCP (Master Control Program) Server provides an HTTP interface to interact with various tools, primarily focused on the `abnum` library for Gematria calculations and text analysis. It allows users to calculate numerical values of texts based on different ancient and modern language codes and find text segments that match a specific numerical value.

## Base URL

For local development, the server runs at:
`http://localhost:5000`

## Endpoint: `/invoke_tool`

All tool interactions are done through this single endpoint.

-   **Method:** `POST`
-   **Content-Type:** `application/json`
-   **Request Body:** A JSON object specifying the `tool_name` and its `parameters`.
    ```json
    {
        "tool_name": "name_of_the_tool",
        "parameters": {
            "param1": "value1",
            "param2": "value2"
        }
    }
    ```
-   **Response:** The server returns a JSON object containing a `result` field on success or an `error` field if something went wrong.
    -   Success: `{"result": { ... }, "error": null}`
    -   Error: `{"result": null, "error": "Error message"}`

---

## Tools

### 1. `calculate_value`

**Description:** Calculates the numerical value of a given text string based on a specified Gematria code and operation (addition or multiplication).

**`tool_name`:** `"calculate_value"`

**Parameters:**

| Name        | Type   | Required? | Default | Description                                                                 |
| :---------- | :----- | :-------- | :------ | :-------------------------------------------------------------------------- |
| `text`      | string | Yes       |         | The text string to calculate the value for.                                 |
| `code`      | string | Yes       |         | The Gematria code to use (see "Available Abnum Codes" below).             |
| `operation` | string | No        | `"add"` | The mathematical operation to apply: `"add"` for sum, `"multiply"` for product. |

**Example Successful Request (Addition):**

```json
{
    "tool_name": "calculate_value",
    "parameters": {
        "text": "Logos",
        "code": "grc",
        "operation": "add"
    }
}
```

**Example Successful Response (Addition):**

```json
{
    "result": {
        "value": 373
    },
    "error": null
}
```

**Example Successful Request (Multiplication):**

```json
{
    "tool_name": "calculate_value",
    "parameters": {
        "text": "Ace",
        "code": "eng",
        "operation": "multiply"
    }
}
```

**Example Successful Response (Multiplication):**

```json
{
    "result": {
        "value": 15
    },
    "error": null
}
```

**Example Error Response (Invalid Code):**

```json
{
    "result": null,
    "error": "Invalid code 'invalid'. Available codes: ['grc', 'heb', 'eng', 'fin', 'cop', 'arm', 'ara', 'syc', 'phn', 'brh', 'san']"
}
```

**Example Error Response (Text contains unsupported characters):**
(Note: HTTP status code is 200 here as the server handles this specific error gracefully within the API structure)
```json
{
    "result": null,
    "error": "String 'text123' contains unsupported characters for the letter value calculation."
}
```

---

### 2. `find_text_by_value`

**Description:** Searches within a given text for words or sequences of words (if cumulative) that sum up to a target numerical value, based on a specified Gematria code.

**`tool_name`:** `"find_text_by_value"`

**Parameters:**

| Name           | Type    | Required? | Default | Description                                                                         |
| :------------- | :------ | :-------- | :------ | :---------------------------------------------------------------------------------- |
| `text`         | string  | Yes       |         | The text string to search within.                                                   |
| `target_value` | integer | Yes       |         | The numerical value to search for.                                                  |
| `code`         | string  | Yes       |         | The Gematria code to use (see "Available Abnum Codes" below).                     |
| `cumulative`   | boolean | No        | `false` | If `true`, finds sequences of words that sum to `target_value`. If `false`, finds individual words. |

**Example Successful Request (Non-cumulative):**

```json
{
    "tool_name": "find_text_by_value",
    "parameters": {
        "text": "one two three one four",
        "target_value": 8,
        "code": "eng",
        "cumulative": false
    }
}
```

**Example Successful Response (Non-cumulative):**

```json
{
    "result": {
        "matches": ["one", "one"]
    },
    "error": null
}
```

**Example Successful Request (Cumulative):**

```json
{
    "tool_name": "find_text_by_value",
    "parameters": {
        "text": "o Logos estin to phos",
        "target_value": 443,
        "code": "grc",
        "cumulative": true
    }
}
```
*Value for "o Logos" (o=70, Logos=373) in Greek is 443.*

**Example Successful Response (Cumulative):**

```json
{
    "result": {
        "matches": ["o Logos"]
    },
    "error": null
}
```

**Example Error Response (Missing Parameter):**

```json
{
    "result": null,
    "error": "Missing 'text', 'target_value', or 'code' in parameters"
}
```

---

## Available `abnum` Codes

The `code` parameter in the tools corresponds to the Gematria systems available in the `abnum` library. The following codes can be used:

-   `grc` (Ancient Greek)
-   `heb` (Hebrew)
-   `eng` (English - specific system, see abnum documentation for details)
-   `fin` (Finnish)
-   `cop` (Coptic)
-   `arm` (Aramaic)
-   `ara` (Arabic)
-   `syc` (Classical Syriac)
-   `phn` (Phoenician)
-   `brh` (Brahmi)
-   `san` (Sanskrit - note: may have empty value map in some abnum versions)

---

## `curl` Example

Here's an example of how to use `curl` to calculate the value of the Greek word "Logos":

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{
    "tool_name": "calculate_value",
    "parameters": {
        "text": "Logos",
        "code": "grc",
        "operation": "add"
    }
}' \
http://localhost:5000/invoke_tool
```

**Expected Output:**

```json
{
  "result": {
    "value": 373
  },
  "error": null
}
```

---
