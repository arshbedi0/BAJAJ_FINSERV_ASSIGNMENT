import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import math
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

OFFICIAL_EMAIL = "arshdeep3790.beai23@chitkara.edu.in"
PORT = int(os.environ.get("PORT", 5000))

def generate_fibonacci(n: int) -> list:
    if n <= 0:
        return []
    if n == 1:
        return [0]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib


def filter_primes(nums: list) -> list:
    def is_prime(num):
        if num < 2:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(num)) + 1, 2):
            if num % i == 0:
                return False
        return True
    
    return [num for num in nums if is_prime(num)]


def compute_hcf(nums: list) -> int:
    if not nums:
        return 0
    
    result = nums[0]
    for num in nums[1:]:
        result = math.gcd(result, num)
    return result


def compute_lcm(nums: list) -> int:
    if not nums:
        return 0
    
    def lcm(a, b):
        return abs(a * b) // math.gcd(a, b)
    
    result = nums[0]
    for num in nums[1:]:
        result = lcm(result, num)
    return result


def ask_ai(question: str) -> str:
    try:
        import google.generativeai as genai
        
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            return "Error: GEMINI_API_KEY not set"
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemma-3-12b-it")
        question = f"Answer the following question in one word: {question}"

        response = model.generate_content(question)
        answer_text = response.text.strip()
        
        import re
        words = re.findall(r'\b\w+\b', answer_text)
        if words:
            return words[0]
        return "No response"
    
    except ImportError:
        return "Error: google-generativeai not installed"
    except Exception as e:
        return f"Error: {str(e)}"


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "is_success": True,
        "official_email": OFFICIAL_EMAIL
    }), 200


@app.route("/bfhl", methods=["POST"])
def bfhl():
    try:
        data = request.get_json()
        
        if not data or not isinstance(data, dict):
            return jsonify({
                "is_success": False,
                "official_email": OFFICIAL_EMAIL,
                "error": "Invalid request: body must be valid JSON object"
            }), 400
        
        if "fibonacci" in data:
            value = data["fibonacci"]
            if not isinstance(value, int) or value < 0:
                return jsonify({
                    "is_success": False,
                    "official_email": OFFICIAL_EMAIL,
                    "error": "Invalid input: fibonacci must be a non-negative integer"
                }), 400
            result = generate_fibonacci(value)
            return jsonify({
                "is_success": True,
                "official_email": OFFICIAL_EMAIL,
                "data": result
            }), 200
        
        elif "prime" in data:
            value = data["prime"]
            if not isinstance(value, list) or not all(isinstance(x, int) for x in value):
                return jsonify({
                    "is_success": False,
                    "official_email": OFFICIAL_EMAIL,
                    "error": "Invalid input: prime must be an array of integers"
                }), 400
            result = filter_primes(value)
            return jsonify({
                "is_success": True,
                "official_email": OFFICIAL_EMAIL,
                "data": result
            }), 200
        
        elif "lcm" in data:
            value = data["lcm"]
            if not isinstance(value, list) or not all(isinstance(x, int) and x > 0 for x in value):
                return jsonify({
                    "is_success": False,
                    "official_email": OFFICIAL_EMAIL,
                    "error": "Invalid input: lcm must be an array of positive integers"
                }), 400
            result = compute_lcm(value)
            return jsonify({
                "is_success": True,
                "official_email": OFFICIAL_EMAIL,
                "data": result
            }), 200
        
        elif "hcf" in data:
            value = data["hcf"]
            if not isinstance(value, list) or not all(isinstance(x, int) and x > 0 for x in value):
                return jsonify({
                    "is_success": False,
                    "official_email": OFFICIAL_EMAIL,
                    "error": "Invalid input: hcf must be an array of positive integers"
                }), 400
            result = compute_hcf(value)
            return jsonify({
                "is_success": True,
                "official_email": OFFICIAL_EMAIL,
                "data": result
            }), 200
        
        elif "AI" in data:
            value = data["AI"]
            if not isinstance(value, str) or len(value.strip()) == 0:
                return jsonify({
                    "is_success": False,
                    "official_email": OFFICIAL_EMAIL,
                    "error": "Invalid input: AI must be a non-empty string"
                }), 400
            result = ask_ai(value)
            return jsonify({
                "is_success": True,
                "official_email": OFFICIAL_EMAIL,
                "data": result
            }), 200
        
        else:
            return jsonify({
                "is_success": False,
                "official_email": OFFICIAL_EMAIL,
                "error": "Invalid request: must contain one of: fibonacci, prime, lcm, hcf, AI"
            }), 400
    
    except Exception as e:
        return jsonify({
            "is_success": False,
            "official_email": OFFICIAL_EMAIL,
            "error": f"Internal server error: {str(e)}"
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "is_success": False,
        "official_email": OFFICIAL_EMAIL,
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "is_success": False,
        "official_email": OFFICIAL_EMAIL,
        "error": "Internal server error"
    }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
