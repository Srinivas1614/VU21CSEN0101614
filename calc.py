from flask import Flask, request, jsonify
import requests
from collections import deque
import time

app = Flask(__name__)

# Configurations
WINDOW_SIZE = 10
API_URL = 'http://third-party-server.com/api/numbers'

# Store for numbers and management
numbers_store = deque(maxlen=WINDOW_SIZE)
unique_numbers = set()

def fetch_number(number_id):
    """Fetch number from third-party server and handle errors."""
    try:
        response = requests.get(f"{API_URL}/{number_id}", timeout=0.5)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching data: {e}")
        return None

@app.route('/numbers/<number_id>', methods=['GET'])
def calculate_average(number_id):
    """Handle the number ID request and calculate average."""
    if number_id not in ['p', 'T', 'e', 'y']:
        return jsonify({'error': 'Invalid number ID'}), 400

    # Fetch number
    start_time = time.time()
    number = fetch_number(number_id)
    end_time = time.time()

    if number is None or (end_time - start_time) > 0.5:
        return jsonify({'error': 'Error fetching data or timeout'}), 500

    # Store unique numbers
    if number not in unique_numbers:
        if len(numbers_store) == WINDOW_SIZE:
            # Remove oldest number if window is full
            oldest_number = numbers_store.popleft()
            unique_numbers.remove(oldest_number)
        
        numbers_store.append(number)
        unique_numbers.add(number)

    # Calculate average if there are enough numbers
    if len(numbers_store) == WINDOW_SIZE:
        avg = sum(numbers_store) / WINDOW_SIZE
    else:
        avg = None

    response = {
        "windowPrevState": list(numbers_store)[:-1] if len(numbers_store) > 1 else [],
        "windowCurrState": list(numbers_store),
        "numbers": list(numbers_store),
        "avg": avg if avg is not None else 'Not enough data'
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9876, debug=True)
