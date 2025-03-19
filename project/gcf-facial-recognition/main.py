import functions_framework
from google.cloud import vision
from flask import request, jsonify, make_response
import numpy as np

def detect_face_landmarks(image_bytes):
    """Detects face landmarks and returns their positions using Google Cloud Vision AI."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.face_detection(image=image)

    if response.error.message:
        raise Exception(f"Cloud Vision AI Error: {response.error.message}")

    faces = response.face_annotations
    if not faces:
        return None

    return faces[0].landmarks  # Return facial landmarks

def compute_similarity(landmarks1, landmarks2):
    """Computes Euclidean distance between two sets of facial landmarks."""
    if not landmarks1 or not landmarks2:
        return 0  # No landmarks detected in one or both images

    points1 = np.array([[lm.position.x, lm.position.y, lm.position.z] for lm in landmarks1])
    points2 = np.array([[lm.position.x, lm.position.y, lm.position.z] for lm in landmarks2])

    # Ensure both images have the same number of landmarks
    min_length = min(len(points1), len(points2))
    points1, points2 = points1[:min_length], points2[:min_length]

    distance = np.linalg.norm(points1 - points2)
    
    # Normalize similarity score (lower distance = higher similarity)
    similarity_score = np.exp(-distance / 100.0)  # Scaling for better comparison

    return similarity_score

@functions_framework.http
def verify_identity(request):
    """Cloud Function to verify if ID picture and selfie belong to the same person using Google Cloud Vision AI."""
    
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

    id_picture = request.files['id_picture'].read()
    selfie = request.files['selfie'].read()

    id_landmarks = detect_face_landmarks(id_picture)
    selfie_landmarks = detect_face_landmarks(selfie)

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
    match = similarity_score > 0.7  # Adjust threshold for better accuracy

    response = jsonify({
        "match": match,
        "similarity_score": similarity_score
    })
    response.status_code = 200
    response.headers.update(cors_headers)
    
    return response
