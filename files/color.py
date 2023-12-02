import cv2
import numpy as np
import matplotlib.pyplot as plt
from colorthief import ColorThief 


ct = ColorThief("pictures/Starwars.png")
dominant_color = ct.get_color(quality = 1)

print(dominant_color)
plt.imshow([[dominant_color]])
plt.show()









