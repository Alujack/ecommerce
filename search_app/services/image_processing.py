from tensorflow.keras.applications import VGG16 # type: ignore
from tensorflow.keras.preprocessing import image # type: ignore
from tensorflow.keras.applications.vgg16 import preprocess_input # type: ignore
import numpy as np

# Initialize the model once to avoid reloading it each time
model = VGG16(weights='imagenet', include_top=False)


def extract_image_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    features = model.predict(x)
    return features.flatten().tolist()  # Convert to list for JSON storage


def compare_images(uploaded_image_features, stored_image_features):
    from sklearn.metrics.pairwise import cosine_similarity
    similarity = cosine_similarity(
        [uploaded_image_features], [stored_image_features])
    return similarity[0][0]  # Return the similarity score
