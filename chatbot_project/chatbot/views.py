from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import os

# Render the homepage
def index(request):
    return render(request, "chatbot/index.html")

# Determine the project root directory (where manage.py is located)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_file_path = os.path.join(PROJECT_ROOT, 'config.json')

# Load the API key from config.json
with open(config_file_path, 'r') as config_file:
    config = json.load(config_file)
HUGGING_FACE_API_KEY = config.get("HUGGING_FACE_API_KEY")

# Set the inference endpoint URL for Mistral-7B-Instruct-v0.2
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"

def get_huggingface_response(question):
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    # Add parameters to control output length and style
    payload = {
        "inputs": question,
        "parameters": {
            "max_new_tokens": 100,  # Limits the generated text to 50 new tokens (adjust as needed)
            "temperature": 0.1    # Adjusts randomness (lower for more deterministic responses)
        }
    }
    
    try:
        response = requests.post(HUGGING_FACE_API_URL, headers=headers, json=payload)
    except Exception as e:
        print("Request error:", e)
        return "Sorry, there was an error contacting the API."
    
    print("HTTP Status Code:", response.status_code)
    print("Raw Response Text:", repr(response.text))
    
    if response.status_code != 200:
        try:
            error_response = response.json()
            return f"API Error: {error_response.get('error', 'Unknown error')}"
        except Exception:
            return f"API returned status {response.status_code} with no valid JSON error message."
    
    if not response.text.strip():
        print("Empty response received from the API.")
        return "Sorry, I did not receive any response from the API."
    
    try:
        raw_response = response.json()
    except Exception as e:
        print("Error decoding JSON:", e)
        return "Sorry, I could not decode the response."
    
    print("RAW API RESPONSE:", raw_response)
    
    if isinstance(raw_response, dict) and "error" in raw_response:
        return f"API Error: {raw_response['error']}"
    
    try:
        # Assuming the API returns a list with the generated text in the first item
        if isinstance(raw_response, list) and len(raw_response) > 0:
            return raw_response[0]['generated_text']
        else:
            return "Sorry, the API response format was not recognized."
    except (KeyError, IndexError) as e:
        print("Error parsing API response:", e, response.text)
        return "Sorry, I could not generate a response."

@csrf_exempt
def ask(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            question = data.get("question", "")
            answer = get_huggingface_response(question)
            return JsonResponse({"answer": answer})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON input."}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=405)
