from feature_extractor import FeatureExtractor, cosine_sim
from keras.preprocessing.image import load_img, img_to_array
from PIL import Image
import argparse

# fish.jpg -- http://farm1.static.flickr.com/184/446269374_7acbfa7478.jpg
# tiger_shark.jpg -- http://farm2.static.flickr.com/1202/1181025773_3978496781.jpg
# tiger_shark1 -- http://farm2.static.flickr.com/1202/1181025773_3978496781.jpg

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_filename')
    args = parser.parse_args()

    img_src = img_to_array(load_img('tmp/tiger_shark.jpg', target_size=(224, 224))).flatten()
    img_tgt1 = img_to_array(load_img('tmp/tiger_shark1.jpg', target_size=(224, 224))).flatten()
    img_tgt2 = img_to_array(load_img('tmp/fish.jpg', target_size=(224, 224))).flatten()

    raw_sim_score1 = cosine_sim(img_src, img_tgt1)
    raw_sim_score2 = cosine_sim(img_src, img_tgt2)

    print('RAW PIXELS')
    print('raw_sim_score1:', raw_sim_score1)
    print('raw_sim_score2:', raw_sim_score2)

    model = FeatureExtractor('resnet50')

    features_src = model('tmp/tiger_shark.jpg')
    features_tgt1 = model('tmp/tiger_shark1.jpg')
    features_tgt2 = model('tmp/fish.jpg')

    sim_score1 = cosine_sim(features_src, features_tgt1)
    sim_score2 = cosine_sim(features_src, features_tgt2)

    print('FEATURE SPACE')
    print('sim_score1:', sim_score1)
    print('sim_score2:', sim_score2)
