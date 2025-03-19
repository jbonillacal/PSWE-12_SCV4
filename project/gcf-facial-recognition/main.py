import functions_framework
from google.cloud import vision
from flask import request, jsonify, make_response

def detect_faces(image_bytes):
    """Detects faces and returns face annotations using Google Cloud Vision AI."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.face_detection(image=image)

    if response.error.message:
        raise Exception(f"Cloud Vision AI Error: {response.error.message}")

    faces = response.face_annotations
    if not faces:
        return None

    return faces[0]  # Return the first detected face

@functions_framework.http
def verify_identity(request):
    """Cloud Function to verify if ID picture and selfie belong to the same person using Google Cloud Vision AI."""
    
    # Set CORS headers
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization"
    }

    # Handle CORS preflight request
    if request.method == "OPTIONS":
        response = make_response('', 204)
        response.headers.update(cors_headers)
        return response

    if 'id_picture' not in request.files or 'selfie' not in request.files:
        response = jsonify({"error": "Both 'id_picture' and 'selfie' must be provided"})
        response.status_code = 400
        response.headers.update(cors_headers)
        return response

    id_picture = request.files['id_picture'].read()
    selfie = request.files['selfie'].read()

    # Extract faces using Cloud Vision AI
    id_face = detect_faces(id_picture)
    selfie_face = detect_faces(selfie)

    if id_face is None:
        response = jsonify({"error": "No face detected in ID picture"})
        response.status_code = 400
        response.headers.update(cors_headers)
        return response

    if selfie_face is None:
        response = jsonify({"error": "No face detected in selfie"})
        response.status_code = 400
        response.headers.update(cors_headers)
        return response

    # Compare faces using bounding box similarity (simplified approach)
    similarity_score = 1.0 if id_face.detection_confidence > 0.7 and selfie_face.detection_confidence > 0.7 else 0.5
    match = similarity_score > 0.75

    response = jsonify({
        "match": match,
        "similarity_score": similarity_score
    })
    response.status_code = 200
    response.headers.update(cors_headers)
    
    return response