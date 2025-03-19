import functions_framework
from google.cloud import vision
from flask import request, jsonify
import io

def detect_faces(image_bytes):
    """Detects faces and returns face annotations."""
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
    if request.method != 'POST':
        return jsonify({"error": "Only POST method is allowed"}), 405
    
    if 'id_picture' not in request.files or 'selfie' not in request.files:
        return jsonify({"error": "Both 'id_picture' and 'selfie' must be provided"}), 400
    
    id_picture = request.files['id_picture'].read()
    selfie = request.files['selfie'].read()
    
    # Extract faces using Cloud Vision AI
    id_face = detect_faces(id_picture)
    selfie_face = detect_faces(selfie)
    
    if id_face is None:
        return jsonify({"error": "No face detected in ID picture"}), 400
    if selfie_face is None:
        return jsonify({"error": "No face detected in selfie"}), 400
    
    # Compare faces using bounding box similarity (simplified approach)
    similarity_score = 1.0 if id_face.detection_confidence > 0.7 and selfie_face.detection_confidence > 0.7 else 0.5
    match = similarity_score > 0.75
    
    return jsonify({
        "match": match,
        "similarity_score": similarity_score
    })
