import functions_framework
import logging
import google.cloud.logging
import requests
import re
import json
import datetime
import tempfile
import os
from google.cloud import pubsub_v1
from flask import request, jsonify, make_response
from deepface import DeepFace

# Initialize Google Cloud clients
client = google.cloud.logging.Client()
client.setup_logging()
pubsub_client = pubsub_v1.PublisherClient()

# Define the Pub/Sub topic name
PROJECT_ID = "cenfotec2024"  
TOPIC_NAME = "facial-recognition-topic"
TOPIC_PATH = pubsub_client.topic_path(PROJECT_ID, TOPIC_NAME)


def save_temp_image(image_bytes):
    """Saves an image from bytes to a temporary file and returns the path."""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    temp_file.write(image_bytes)
    temp_file.close()
    return temp_file.name


def compare_faces(id_picture_bytes, selfie_bytes):
    """Uses DeepFace to verify if two images belong to the same person."""
    try:
        # Save images temporarily
        id_picture_path = save_temp_image(id_picture_bytes)
        selfie_path = save_temp_image(selfie_bytes)

        # Run DeepFace verification
        result = DeepFace.verify(img1_path=id_picture_path, img2_path=selfie_path, model_name="VGG-Face")

        logging.info(f"DeepFace result: {result}")

        # Extract match result
        match = result["verified"]
        similarity_score = result["distance"]

        return match, similarity_score

    except Exception as e:
        logging.error(f"DeepFace Error: {str(e)}")
        return False, None

    finally:
        # Cleanup: Remove temp image files
        try:
            os.remove(id_picture_path)
            os.remove(selfie_path)
            logging.info("Temporary images deleted successfully.")
        except Exception as cleanup_error:
            logging.error(f"Error deleting temp files: {cleanup_error}")



def call_image_text_extract(id_picture_bytes):
    """Calls an external function to extract text from the ID image."""
    url = "https://us-central1-cenfotec2024.cloudfunctions.net/gcf-image-text-extract"
    headers = {"Content-Type": "application/octet-stream"}
    response = requests.post(url, headers=headers, data=id_picture_bytes)
    return response.json()


def parse_extracted_text(extracted_text, match, similarity_score):
    """Parses extracted text to generate structured JSON data."""
    parsed_data = {
        "country": None,
        "id": None,
        "name": None,
        "lastName1": None,
        "lastName2": None,
        "match": bool(match),
        "similarityScore": float(similarity_score),
        "requestDate": datetime.datetime.utcnow().isoformat(),
        "companyId": "1"
    }

    lines = extracted_text.split("\n")

    for line in lines:
        line = line.strip()

        if "REPÚBLICA" in line:
            parsed_data["country"] = line

        match_id = re.search(r"\b\d{1} \d{4} \d{4}\b", line)
        if match_id:
            parsed_data["id"] = match_id.group(0)

        if line.startswith("Nombre:"):
            parsed_data["name"] = line.replace("Nombre:", "").strip()
        elif line.startswith("1° Apellido:"):
            parsed_data["lastName1"] = line.replace("1° Apellido:", "").strip()
        elif line.startswith("2° Apellido:"):
            parsed_data["lastName2"] = line.replace("2° Apellido:", "").strip()

    return json.dumps(parsed_data, ensure_ascii=False, indent=4)


def publish_to_pubsub(message):
    """Publishes a message to the Pub/Sub topic."""
    try:
        future = pubsub_client.publish(TOPIC_PATH, message.encode("utf-8"))
        future.result()
        logging.info("Message published successfully to Pub/Sub.")
    except Exception as e:
        logging.error(f"Error publishing to Pub/Sub: {e}")


@functions_framework.http
def verify_identity(request):
    """Cloud Function to verify if an ID picture and selfie belong to the same person."""
    logging.info("Processing identity verification request")

    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With"
    }

    if request.method == "OPTIONS":
        response = make_response("", 204)
        response.headers.update(cors_headers)
        return response

    if 'id_picture' not in request.files or 'selfie' not in request.files:
        response = jsonify({"error": "Both 'id_picture' and 'selfie' must be provided"})
        response.status_code = 400
        response.headers.update(cors_headers)
        return response

    id_picture_bytes = request.files['id_picture'].read()
    selfie_bytes = request.files['selfie'].read()

    # Compare faces using DeepFace
    match, similarity_score = compare_faces(id_picture_bytes, selfie_bytes)

    # Call image text extraction
    json_response = call_image_text_extract(id_picture_bytes)
    extracted_text = json_response.get("extracted_text", "")

    # Parse extracted text
    json_output = parse_extracted_text(extracted_text, match, similarity_score)

    logging.info("JSON Output: %s", json_output)

    # Publish to Pub/Sub
    publish_to_pubsub(json_output)

    response = jsonify({
        "match": bool(match),
        "similarity_score": float(similarity_score)
    })
    response.status_code = 200
    response.headers.update(cors_headers)

    return response