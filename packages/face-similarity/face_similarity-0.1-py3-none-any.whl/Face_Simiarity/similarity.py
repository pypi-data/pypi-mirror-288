# face_similarity/similarity.py

import cv2
import numpy as np
from skimage.feature import hog
from sklearn.metrics.pairwise import cosine_similarity
import face_recognition

def load_image(image_path):
    return face_recognition.load_image_file(image_path)

def detect_face(image):
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) > 0:
        top, right, bottom, left = face_locations[0]
        face_image = image[top:bottom, left:right]
        face_image = cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR)
        return face_image
    else:
        raise ValueError("No face found in the image.")

def compute_similarity(image1, image2):
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    image1_resized = cv2.resize(image1_gray, (224, 224))
    image2_resized = cv2.resize(image2_gray, (224, 224))

    image1_hog, _ = hog(image1_resized, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True)
    image2_hog, _ = hog(image2_resized, pixels_per_cell=(8, 8), cells_per_block=(2, 2), visualize=True)

    image1_hog = image1_hog.reshape(1, -1)
    image2_hog = image2_hog.reshape(1, -1)

    similarity = cosine_similarity(image1_hog, image2_hog)
    return similarity[0][0]

def compare_faces(passport_image_path, original_photo_path, threshold=0.5):
    passport_image = load_image(passport_image_path)
    face_image = detect_face(passport_image)
    original_photo = cv2.imread(original_photo_path)

    similarity = compute_similarity(face_image, original_photo)
    if similarity > threshold:
        return f"The images are likely of the same person. Cosine Similarity: {similarity}"
    else:
        return f"The images are likely of different people. Cosine Similarity: {similarity}"