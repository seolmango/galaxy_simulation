import imageio
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

file_path = sys.argv[1]

frames = np.load(file_path)

image_frames = []
plt.ion()
fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection='3d')
for i in range(len(frames)):
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_zlim(-20, 20)
    ax.scatter3D(frames[i][0][0,:], frames[i][0][1,:], frames[i][0][2,:], s=1, c='b')
    ax.scatter3D(frames[i][1][0,:], frames[i][1][1,:], frames[i][1][2,:],s=1, c='r')
    ax.set_title(f'frame {i}')
    fig.canvas.draw()
    image = np.array(fig.canvas.buffer_rgba())
    image = np.array(Image.fromarray(image).resize((1080, 720)))
    image_frames.append(image)
    plt.pause(0.01)
    ax.clear()
plt.ioff()

output_file = 'simulation.mp4'
writer = imageio.get_writer(output_file, fps=30, macro_block_size=None, format='MP4')

for i in range(len(image_frames)):
    writer.append_data(image_frames[i])
writer.close()