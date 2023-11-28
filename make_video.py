import matplotlib.pyplot as plt
from PIL import Image
from multiprocessing import Pool, cpu_count
import numpy as np
import sys
import imageio
import tqdm

file_path = sys.argv[1]
try:
    resolution = int(sys.argv[2])
except IndexError:
    resolution = 1

frames = np.load(file_path)

def make_frame_image(temp):
    data, index, resolution = temp
    fig = plt.figure(figsize=(16*resolution, 9*resolution))
    ax = plt.axes(projection='3d')
    ax.set_xlim(-20, 20)
    ax.set_ylim(-20, 20)
    ax.set_zlim(-20, 20)
    ax.scatter3D(data[0][0,:], data[0][1,:], data[0][2,:], s=1, c='b')
    ax.scatter3D(data[1][0,:], data[1][1,:], data[1][2,:],s=1, c='r')
    ax.set_title(f'frame {index}')
    fig.canvas.draw()
    image = np.array(fig.canvas.buffer_rgba())
    image = np.array(Image.fromarray(image).resize((1920, 1080)))
    ax.clear()
    plt.close(fig)
    result = [index, image]
    return result

def make_video_image(image_frames):
    output_file = 'simulation.mp4'
    writer = imageio.get_writer(output_file, fps=30, macro_block_size=None, format='MP4')
    for image in tqdm.tqdm(image_frames, desc="making video"):
        writer.append_data(image)
    writer.close()
    print(f'video saved as {output_file}')

if __name__ == '__main__':
    p = Pool(cpu_count())
    image_frames = list(tqdm.tqdm(p.imap(make_frame_image, [(frames[i], i, resolution) for i in range(len(frames))]), total=len(frames), desc="rendering images"))
    image_frames = sorted(image_frames, key=lambda x: x[0])
    image_frames = [image_frames[i][1] for i in range(len(image_frames))]
    make_video_image(image_frames)