import urllib.request
from PIL import Image

urllib.request.urlretrieve("https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Full_Moon_Luc_Viatour.jpg/1015px-Full_Moon_Luc_Viatour.jpg", "tst.jpg")
img = Image.open("tst.png")
img.show()