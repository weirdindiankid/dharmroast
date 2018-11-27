from keras.applications import resnet50
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
from PIL import Image

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
        return img

    # Returns numpy array consisting of last convolutional feature layer in model
    def extract_features(self, img):
        if type(img) is str:
            img = self.load_input(img)
        elif isinstance(img, Image.Image):
            wh_tuple = self.input_shape[:2]
            print(img.size, wh_tuple)
            if img.size != wh_tuple:
                print(img, *wh_tuple, Image.NEAREST)
                new_img = img.resize(wh_tuple, Image.NEAREST)
            else:
                new_img = img

            img = img_to_array(new_img)
        else:
            raise Exception("Image must be a string filepath or an instance of PIL.Image.Image")

        img = img[np.newaxis, :] # batch image
        img = resnet50.preprocess_input(img)
        return self.model.predict(img).flatten()

    def __call__(self, img):
        return self.extract_features(img)

def cosine_sim(arr1, arr2):
    return np.dot(arr1, arr2) / np.linalg.norm(arr1) / np.linalg.norm(arr2)
