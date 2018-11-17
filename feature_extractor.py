import keras
from keras.applications import resnet50
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.imagenet_utils import decode_predictions
import matplotlib.pyplot as plt
import numpy as np
import argparse

class FeatureExtractor:
    # Asssumes input_shape is (image_height, image_width, channels)
    def __init__(self, name, input_shape=(224, 224, 3)):
        assert len(input_shape) == 3

        self.input_shape = input_shape
        self.name = name.lower()

        if name == 'resnet50':
            self.model = resnet50.ResNet50(
                include_top=False,
                weights='imagenet',
                input_tensor=None,
                input_shape=input_shape,
                pooling=None
            )

        else:
            raise ValueError('For now, the model must be resnet50')

    def load_input(self, fname): 
        orig = load_img(fname, target_size=self.input_shape[:2])
        img = img_to_array(orig) # convert to numpy array
        batch_img = img[np.newaxis, :] # batch image
        final_img = resnet50.preprocess_input(batch_img)
        return final_img

    # Returns numpy array consisting of last convolutional feature layer in model
    def extract_features(self, img):
        if type(img) is str:
            img = self.load_input(img)

        return self.model.predict(img).flatten()

def cosine_sim(arr1, arr2):
    return np.dot(arr1, arr2) / np.linalg.norm(arr1) / np.linalg.norm(arr2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_filename')
    args = parser.parse_args()

    img_src = img_to_array(load_img('tmp/tiger_shark.jpg', target_size=(224, 224))).flatten()
    img_tgt1 = img_to_array(load_img('tmp/tiger_shark1.jpg', target_size=(224, 224))).flatten()
    img_tgt2 = img_to_array(load_img('tmp/plankton.jpg', target_size=(224, 224))).flatten()

    raw_sim_score1 = cosine_sim(img_src, img_tgt1)
    raw_sim_score2 = cosine_sim(img_src, img_tgt2)

    print('RAW PIXELS')
    print('raw_sim_score1:', raw_sim_score1)
    print('raw_sim_score2:', raw_sim_score2)

    model = FeatureExtractor('resnet50')

    features_src = model.extract_features('tmp/tiger_shark.jpg')
    features_tgt1 = model.extract_features('tmp/tiger_shark1.jpg')
    features_tgt2 = model.extract_features('tmp/plankton.jpg')

    sim_score1 = cosine_sim(features_src, features_tgt1)
    sim_score2 = cosine_sim(features_src, features_tgt2)

    print('FEATURE SPACE')
    print('sim_score1:', sim_score1)
    print('sim_score2:', sim_score2)
