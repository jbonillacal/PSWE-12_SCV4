import google.cloud.logging
client = google.cloud.logging.Client()
client.setup_logging()
import functions_framework
import logging
import os
from google.cloud import storage, vision
from google.cloud.vision_v1 import ImageAnnotatorClient

# Initialize Google Cloud clients
storage_client = storage.Client()
vision_client = ImageAnnotatorClient()

@functions_framework.cloud_event
def process_image(cloud_event):
    """Triggered by a new file upload in Cloud Storage.
    Extracts text from an image using Google Cloud Vision API.
    """
    try:
        print("Starting") 
        data = cloud_event.data
        bucket_name = data["bucket"]
        file_name = data["name"]

        logging.info(f"Processing file: {file_name} from bucket: {bucket_name}")

        # Download image
        image_bytes = download_image(bucket_name, file_name)
        if not image_bytes:
            logging.error("Failed to download image.")
            return

        # Extract text using Google Cloud Vision
        extracted_text = extract_text_from_image(image_bytes)

        # Log the extracted text
        logging.info(f"Extracted Text: {extracted_text}")
        print(extracted_text) 

    except Exception as e:
        logging.error(f"Error processing image: {str(e)}", exc_info=True)


def download_image(bucket_name, file_name):
    """Downloads an image from Cloud Storage."""
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_name)
        return blob.download_as_bytes()
    except Exception as e:
        logging.error(f"Error downloading image: {str(e)}")
        return None


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
