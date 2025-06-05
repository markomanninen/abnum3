from flask import Flask, request, jsonify
from abnum.main import Abnum, AbnumException
from abnum import letter_value # To access codes like letter_value.greek
import operator # For multiplication
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# Dynamically get available codes from letter_value.data
AVAILABLE_CODES = letter_value.data.keys()

@app.route('/invoke_tool', methods=['POST'])
def invoke_tool_route():
    logging.info(f"Received request for /invoke_tool")
    data = request.get_json()
    if not data:
        logging.error("Invalid JSON payload received.")
        return jsonify({"result": None, "error": "Invalid JSON payload"}), 400

    tool_name = data.get('tool_name')
    parameters = data.get('parameters', {})

    logging.info(f"Tool name: {tool_name}, Parameters: {parameters}")

    if not tool_name:
        logging.error("Missing tool_name in request.")
        return jsonify({"result": None, "error": "Missing tool_name"}), 400

    if not parameters: # Assuming parameters are always needed. Adjust if some tools don't need them.
        logging.error(f"Missing parameters for tool: {tool_name}.")
        return jsonify({"result": None, "error": "Missing parameters"}), 400

    if tool_name == "calculate_value":
        text = parameters.get('text')
        code = parameters.get('code')
        operation = parameters.get('operation', 'add') # Default to 'add'

        if not text or not code:
            logging.error(f"Missing 'text' or 'code' in parameters for calculate_value. Parameters: {parameters}")
            return jsonify({"result": None, "error": "Missing 'text' or 'code' in parameters"}), 400

        if code not in AVAILABLE_CODES:
            logging.error(f"Invalid code '{code}' for calculate_value. Available: {list(AVAILABLE_CODES)}")
            return jsonify({"result": None, "error": f"Invalid code '{code}'. Available codes: {list(AVAILABLE_CODES)}"}), 400

        try:
            logging.info(f"Attempting to instantiate Abnum with code: {code} for calculate_value")
            abnum_instance = Abnum(code)
            calculated_value = 0
            if operation == "multiply":
                logging.info(f"Performing 'multiply' operation for calculate_value on text: '{text}'")
                calculated_value = abnum_instance.value(text, func=operator.mul, init=1)
            elif operation == "add":
                logging.info(f"Performing 'add' operation for calculate_value on text: '{text}'")
                calculated_value = abnum_instance.value(text) # uses default add operation
            else:
                logging.error(f"Invalid operation '{operation}' for calculate_value.")
                return jsonify({"result": None, "error": f"Invalid operation '{operation}'. Must be 'add' or 'multiply'."}), 400

            logging.info(f"calculate_value successful. Text: '{text}', Code: '{code}', Operation: '{operation}', Result: {calculated_value}")
            return jsonify({"result": {"value": calculated_value}, "error": None})

        except AbnumException as e:
            logging.error(f"AbnumException in calculate_value: {str(e)}. Parameters: {parameters}", exc_info=True)
            return jsonify({"result": None, "error": str(e)})
        except Exception as e:
            logging.error(f"Unexpected error in calculate_value: {str(e)}. Parameters: {parameters}", exc_info=True)
            return jsonify({"result": None, "error": f"An unexpected error occurred: {str(e)}"}), 500

    elif tool_name == "find_text_by_value":
        text = parameters.get('text')
        target_value = parameters.get('target_value')
        code = parameters.get('code')
        cumulative = parameters.get('cumulative', False) # Default to False

        if not text or target_value is None or not code: # target_value can be 0, so check for None
            logging.error(f"Missing 'text', 'target_value', or 'code' in parameters for find_text_by_value. Parameters: {parameters}")
            return jsonify({"result": None, "error": "Missing 'text', 'target_value', or 'code' in parameters"}), 400

        if not isinstance(target_value, int):
            logging.error(f"'target_value' is not an integer for find_text_by_value. Received: {target_value}")
            return jsonify({"result": None, "error": "'target_value' must be an integer."}), 400

        if code not in AVAILABLE_CODES:
            logging.error(f"Invalid code '{code}' for find_text_by_value. Available: {list(AVAILABLE_CODES)}")
            return jsonify({"result": None, "error": f"Invalid code '{code}'. Available codes: {list(AVAILABLE_CODES)}"}), 400

        try:
            logging.info(f"Attempting to instantiate Abnum with code: {code} for find_text_by_value")
            abnum_instance = Abnum(code)
            logging.info(f"Performing 'find' operation for find_text_by_value. Text: '{text}', Target: {target_value}, Cumulative: {cumulative}")
            matches = abnum_instance.find(text, target_value, cumulative=cumulative)
            logging.info(f"find_text_by_value successful. Text: '{text}', Target: {target_value}, Matches: {len(matches)} found.")
            return jsonify({"result": {"matches": matches}, "error": None})

        except AbnumException as e:
            logging.error(f"AbnumException in find_text_by_value: {str(e)}. Parameters: {parameters}", exc_info=True)
            return jsonify({"result": None, "error": str(e)})
        except Exception as e:
            logging.error(f"Unexpected error in find_text_by_value: {str(e)}. Parameters: {parameters}", exc_info=True)
            return jsonify({"result": None, "error": f"An unexpected error occurred: {str(e)}"}), 500

    else:
        logging.warning(f"Unknown tool_name requested: {tool_name}")
        return jsonify({"result": None, "error": f"Unknown tool_name: {tool_name}"}), 400

if __name__ == '__main__':
    logging.info("Starting Flask development server.")
    app.run(debug=True, host='0.0.0.0', port=5000)
