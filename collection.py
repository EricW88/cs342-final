import pandas as pd
import pickle
import numpy as np
from PIL import Image

frame = 0
def to_image(x, proj, view):
    p = proj @ view @ np.array(list(x) + [1])
    return np.array([p[0] / p[-1], -p[1] / p[-1]])

def save_image(image, file, player, frame):
    im = Image.fromarray(image)
    im.save("{file}.{player}.{frame}.png".format(file=file, player = player, frame = str(frame).zfill(5)))

def save_csv(array, file, player, frame):  
    df = pd.DataFrame(array)
    df.to_csv('{file}.{player}.{frame}.csv'.format(file=file, player = player, frame = str(frame).zfill(5)))

file = "yoshua_jurgen"
with (open(file, "rb")) as openfile:
    while True:
        try:
            temp = pickle.load(openfile)
            save_image(temp['team1_images'][0], file, 'p1', frame)
            save_image(temp['team1_images'][1], file, 'p2', frame)
            save_image(temp['team2_images'][0], file, 'p3', frame)
            save_image(temp['team2_images'][1], file, 'p4', frame)
            coords = temp['soccer_state']['ball']['location']
            view1 = temp['team1_state'][0]['camera']['view']
            proj1 = temp['team1_state'][0]['camera']['projection']
            view2 = temp['team1_state'][1]['camera']['view']
            proj2 = temp['team1_state'][1]['camera']['projection']
            view3 = temp['team2_state'][0]['camera']['view']
            proj3 = temp['team2_state'][0]['camera']['projection']
            view4 = temp['team2_state'][1]['camera']['view']
            proj4 = temp['team2_state'][1]['camera']['projection']

            # print(to_image(coords, proj1, view1))
            save_csv(to_image(coords, proj1, view1), file, 'p1', frame)
            save_csv(to_image(coords, proj2, view2), file, 'p2', frame)
            save_csv(to_image(coords, proj3, view3), file, 'p3', frame)
            save_csv(to_image(coords, proj4, view4), file, 'p4', frame)

            frame += 1
        except EOFError:
            break
print(frame)