import functions_framework
import numpy as np
import logging
import google.cloud.logging
import requests
import re
import json
from google.cloud import vision
from flask import request, jsonify, make_response


client = google.cloud.logging.Client()
client.setup_logging()

def detect_face_landmarks(image_bytes):
    """Detects face landmarks and returns their positions using Google Cloud Vision AI."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.face_detection(image=image)

    if response.error.message:
        raise Exception(f"Cloud Vision AI Error: {response.error.message}")

    faces = response.face_annotations
    if not faces or not faces[0].landmarks:
        return None  # No landmarks detected, return None instead of an empty list

    return faces[0].landmarks 

def compute_similarity(landmarks1, landmarks2):
    """Computes Euclidean distance between two sets of facial landmarks."""
    if not landmarks1 or not landmarks2:
        return 0  # No landmarks detected in one or both images

    points1 = np.array([[lm.position.x, lm.position.y, lm.position.z] for lm in landmarks1])
    points2 = np.array([[lm.position.x, lm.position.y, lm.position.z] for lm in landmarks2])

    # Match lengths to avoid shape mismatch errors
    min_length = min(len(points1), len(points2))
    points1 = points1[:min_length]
    points2 = points2[:min_length]

    # Compute Euclidean distance
    distance = np.linalg.norm(points1 - points2)
    
    # Normalize similarity score
    similarity_score = np.exp(-distance / 100.0)  # Scaling for better comparison

    return similarity_score

def call_image_text_extract(id_picture_bytes):
    url = "https://us-central1-cenfotec2024.cloudfunctions.net/gcf-image-text-extract"
    headers = {
        "Content-Type": "application/octet-stream"
    }
    response = requests.post(url, headers=headers, data=id_picture_bytes)
    print(response.json())  # Extracted text or error response
    extracted_text = json_response.get("extracted_text", "")
    json_output = parse_extracted_text(extracted_text)
    print(json_output)


def parse_extracted_text(extracted_text):
    """Parses extracted text to generate structured JSON data."""
    # Initialize the dictionary with default values
    parsed_data = {
        "country": None,
        "id": None,
        "name": None,
        "lastName1": None,
        "lastName2": None
    }

    # Split text into lines for easier processing
    lines = extracted_text.split("\n")

    for line in lines:
        line = line.strip()

        # Extract country (first line)
        if "REPÚBLICA" in line:
            parsed_data["country"] = line

        # Extract ID (assuming format X XXXX XXXX)
        match = re.search(r"\b\d{1} \d{4} \d{4}\b", line)
        if match:
            parsed_data["id"] = match.group(0)

        # Extract name fields
        if line.startswith("Nombre:"):
            parsed_data["name"] = line.replace("Nombre:", "").strip()
        elif line.startswith("1° Apellido:"):
            parsed_data["lastName1"] = line.replace("1° Apellido:", "").strip()
        elif line.startswith("2° Apellido:"):
            parsed_data["lastName2"] = line.replace("2° Apellido:", "").strip()

    return json.dumps(parsed_data, ensure_ascii=False, indent=4)


@functions_framework.http
def verify_identity(request):
    """Cloud Function to verify if ID picture and selfie belong to the same person using Google Cloud Vision AI."""
    logging.info("This is an INFO log")
    # Explicitly set the allowed headers for CORS
    cors_headers = {
        "Access-Control-Allow-Origin": "*",  # Or specify 'http://localhost:8080' if needed
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With"
    }

    # Handle CORS Preflight Request (OPTIONS)
    if request.method == "OPTIONS":
        response = make_response("", 204)
        response.headers.update(cors_headers)
        return response

    # Check if required files are included in request
    if 'id_picture' not in request.files or 'selfie' not in request.files:
        response = jsonify({"error": "Both 'id_picture' and 'selfie' must be provided"})
        response.status_code = 400
        response.headers.update(cors_headers)
        return response

    id_picture_bytes = request.files['id_picture'].read()
    selfie_bytes = request.files['selfie'].read()

    id_landmarks = detect_face_landmarks(id_picture_bytes)
    selfie_landmarks = detect_face_landmarks(selfie_bytes)      

    if id_landmarks is None:
        response = jsonify({"error": "No face detected in ID picture"})
        response.status_code = 400
        response.headers.update(cors_headers)
        return response

    if selfie_landmarks is None:
        response = jsonify({"error": "No face detected in selfie"})
        response.status_code = 400
        response.headers.update(cors_headers)
        return response

    similarity_score = compute_similarity(id_landmarks, selfie_landmarks)
    match = similarity_score > 0.4  # Adjust threshold for better accuracy

    call_image_text_extract(id_picture_bytes)

    response = jsonify({
        "match": bool(match),  # Ensure it is JSON serializable
        "similarity_score": float(similarity_score)  # Ensure it is a valid number
    })
    response.status_code = 200
    response.headers.update(cors_headers)
    
    return response