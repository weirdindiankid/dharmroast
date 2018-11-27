import proto.secrets as secrets
import numpy as np
import os
from feature_extractor import FeatureExtractor, cosine_sim
import mysql.connector
from collections import namedtuple
from PIL import Image
from keras.preprocessing.image import load_img, img_to_array

# Is this overkill?
# The fact that you have to ask clearly indicates it's underkill
ImageRoasts = namedtuple('ImageRoasts', ['img_link', 'roasts', 'score'])

class Roaster:
    def __init__(self, img_dir = 'proto/images'):
        self.extractor = FeatureExtractor('resnet50')
        self.img_dir = img_dir
    
    def get_roasts(self, target_img): 
        ''' Assumed img is binary image file that could be called with an open python call '''

        db = mysql.connector.connect(
                user=secrets.MYSQL_USERNAME,
                passwd=secrets.MYSQL_PASSWORD,
                database=secrets.MYSQL_DATABASE,
                host=secrets.MYSQL_HOST)
        cursor = db.cursor()
        sql = "SELECT image_link, c1, c2, c3, c4, c5, c6 FROM roasts"
        cursor.execute(sql)

        target_features = self.extractor(target_img)

        classes = [] 
        for img_link, *roasts in cursor:
            print('Comparing against {}'.format(img_link))
            img_path = os.path.join(self.img_dir, img_link)
            img_features = self.extractor(img_path)
            score = cosine_sim(target_features, img_features)
            classes.append(ImageRoasts(img_link, roasts, score))

        cursor.close()
        db.close()

        image_roast = max(classes, key=lambda x: x.score)
        print('(Img link, score):', img_link, score)
        return image_roast

    def get_roast(self, target_img):
        image_roast = self.get_roasts(target_img)
        roast = np.random.choice(image_roast.roasts) # Can replace with a choose roast function later for more sophisticated choosing maybe
        return image_roast.img_link, roast
