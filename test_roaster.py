from PIL import Image
from roaster import Roaster

if __name__ == '__main__':
    roaster = Roaster()

    img = Image.open('tmp/trump_supporter.jpg')
    img.load()

    img_link, roast = roaster.get_roast(img)
    print('Got roast', img_link, roast)
