# In order for text recognition to work, we're going to need to preprocess the image a ton
# Consider filtering out pixels that aren't nearly white, since all data on the smash screen is clearly white...

from PIL import Image
