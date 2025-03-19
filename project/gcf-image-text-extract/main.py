import functions_framework
import logging
import google.cloud.logging
from flask import request, jsonify
from google.cloud import vision
from google.cloud.vision_v1 import ImageAnnotatorClient

client = google.cloud.logging.Client()
client.setup_logging()

# Initialize Google Cloud Vision client
vision_client = ImageAnnotatorClient()

@functions_framework.http
def process_image_http(request):
    """HTTP Cloud Function with CORS support that extracts text from an uploaded image."""
    
    # Allow CORS preflight requests
    if request.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
        return ("", 204, headers)

    try:
        if request.method != "POST":
            return jsonify({"error": "Only POST method is allowed"}), 405

        # Read image bytes directly from request body
        image_bytes = request.data  

        if not image_bytes:
            return jsonify({"error": "Empty image data"}), 400

        # Extract text using Google Cloud Vision API
        extracted_text = extract_text_from_image(image_bytes)

        # JSON response with CORS headers
        response = jsonify({"extracted_text": extracted_text})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    except Exception as e:
        logging.error(f"Error processing image: {str(e)}", exc_info=True)
        response = jsonify({"error": "Internal Server Error"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500


def extract_text_from_image(image_bytes):
    """Extracts text from an image using Google Cloud Vision API."""
    try:
        image = vision.Image(content=image_bytes)
        response = vision_client.text_detection(image=image)

        if response.error.message:
            logging.error(f"Vision API error: {response.error.message}")
            return ""

        texts = response.text_annotations
        return texts[0].description if texts else "No text found"

    except Exception as e:
        logging.error(f"Error extracting text: {str(e)}")
        return ""
