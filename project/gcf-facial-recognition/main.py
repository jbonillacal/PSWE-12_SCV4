import functions_framework
import numpy as np
import logging
import google.cloud.logging
import requests
import re
import json
import datetime
from google.cloud import vision, pubsub_v1
from flask import request, jsonify, make_response

# Initialize Google Cloud clients
client = google.cloud.logging.Client()
client.setup_logging()
pubsub_client = pubsub_v1.PublisherClient()

# Define the Pub/Sub topic name
PROJECT_ID = "cenfotec2024"  
TOPIC_NAME = "facial-recognition-topic"
TOPIC_PATH = pubsub_client.topic_path(PROJECT_ID, TOPIC_NAME)


def detect_face_landmarks(image_bytes):
    """Detects face landmarks and returns their positions using Google Cloud Vision AI."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.face_detection(image=image)

    if response.error.message:
        raise Exception(f"Cloud Vision AI Error: {response.error.message}")

    faces = response.face_annotations
    if not faces or not faces[0].landmarks:
        return None  # No landmarks detected

    return faces[0].landmarks


def compute_similarity(landmarks1, landmarks2):
    """Computes Euclidean distance between two sets of facial landmarks."""
    if not landmarks1 or not landmarks2:
        return 0  # No landmarks detected in one or both images

    # Sort landmarks by type to ensure proper alignment
    landmarks1 = sorted(landmarks1, key=lambda lm: lm.type_)
    landmarks2 = sorted(landmarks2, key=lambda lm: lm.type_)

    points1 = np.array([[lm.position.x, lm.position.y, lm.position.z] for lm in landmarks1])
    points2 = np.array([[lm.position.x, lm.position.y, lm.position.z] for lm in landmarks2])

    min_length = min(len(points1), len(points2))
    points1 = points1[:min_length]
    points2 = points2[:min_length]

    distance = np.linalg.norm(points1 - points2)
    similarity_score = np.exp(-distance / 50.0)  # Adjust scale for better accuracy

    logging.info(f"Similarity Score: {similarity_score}")
    return similarity_score


def call_image_text_extract(id_picture_bytes):
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
        "requestDate": datetime.datetime.utcnow().isoformat(),  # Current timestamp
        "companyId": "1"  # Static company ID
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
        future.result()  # Wait for completion
        logging.info("Message published successfully to Pub/Sub.")
    except Exception as e:
        logging.error(f"Error publishing to Pub/Sub: {e}")


@functions_framework.http
def verify_identity(request):
    """Cloud Function to verify if ID picture and selfie belong to the same person."""
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

    logging.info(f"ID Picture has {len(id_landmarks)} landmarks")
    logging.info(f"Selfie has {len(selfie_landmarks)} landmarks")
    logging.info(f"Computed Similarity Score: {similarity_score}")

    match = similarity_score > 0.1 

    json_response = call_image_text_extract(id_picture_bytes)
    extracted_text = json_response.get("extracted_text", "")

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
