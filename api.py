import os
from dotenv import load_dotenv
from groq import Groq
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # type: ignore

load_dotenv()

app = Flask(__name__)
CORS(app)

# Ensure API_KEY is loaded correctly
api_key = os.environ.get("API_KEY")
if not api_key:
    raise ValueError("API_KEY is missing in environment variables")

client = Groq(
    api_key=os.environ.get("API_KEY"),
    timeout=30  # Set a custom timeout (in seconds)
)

def get_users():
    url = "https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=10"
    response = requests.get(url, timeout=20)
    if response.status_code==200:
        return response.json()
    else:
        return{"error":f"Failed to fetch users: {response.status_code}"}
   


def get_response(text):
    try:
        print(f"Requesting Groq API with query: {text}")  # Log the query
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are a Doctor also give some advice to regular check up on health.
                    Provide response in consistent manner around 50 words."""
                },
                {
                    "role": "user",
                    "content": text,
                },
            ],
            model="llama3-8b-8192",
        )
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        print(f"Error in get_response: {str(e)}")
        raise


@app.route("/", methods=["GET"])
def checkHealth():
    try:
        return jsonify({"status": "Health check ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/response", methods=["POST"])
def response():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "Missing 'query' in the request body"}), 400
        query = data.get("query")
        print(query)
        response = get_response(query)
        # Mock response instead of calling Groq API
        return jsonify({"response": response})
        # return jsonify({"response": "This is a mock response. Groq API call would be here."})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred while processing your request"}), 500


@app.route("/test_users", methods=["GET"])
def test_users():
    try:
        response = get_users()
        users = response.get("data", {}).get("data", [])
        return jsonify(users)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
