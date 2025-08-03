from flask import Flask, request, jsonify
from flask_cors import CORS
import kociemba
import os

app = Flask(__name__)
CORS(app)

def is_valid_cube_string(cube_str):
    if len(cube_str) != 54:
        return False, "Cube string must be 54 characters long."
    colors = 'URFDLB'
    for c in colors:
        if cube_str.count(c) != 9:
            return False, f"Color {c} must appear exactly 9 times."
    return True, ""

@app.route('/solve-cube', methods=['POST'])
def solve_cube():
    data = request.get_json()
    cube_string = data.get("cube", "")

    is_valid, message = is_valid_cube_string(cube_string)
    if not is_valid:
        return jsonify({"error": message}), 400

    try:
        solution = kociemba.solve(cube_string)
        return jsonify({"solution": solution})
    except Exception:
        return jsonify({"error": "Invalid cube state. Please check your cube input."}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
