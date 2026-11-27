import numpy as np

from config import load
from gcode import strokes_to_gcode

square = np.array([[0, 0], [41, 0], [40, 40], [0, 40], [0, 0]], dtype=float)
gcode = strokes_to_gcode([square], load())

with open("square.gcode", "w") as f:
    f.write(gcode)
print(gcode)
