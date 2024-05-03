import imageio
import os
import glob
from PIL import Image as Im
import numpy as np
import sys
import argparse
import re

def images_to_gif(array, filename):
    frames = [Im.fromarray(image) for image in array]
    frame_one = frames[0]
    frame_one.save(filename, format="GIF", append_images=frames,
               save_all=True, duration=100, loop=0)

# https://www.blog.pythonlibrary.org/2021/06/23/creating-an-animated-gif-with-python/
def make_gif(frame_folder, output_folder, output_name, start: int, end: int):
    dir_list = os.listdir(frame_folder)
    forward_images = []
    backward_images = []
    if re.search("flow_[0-9][0-9][0-9][0-9]_to_[0-9][0-9][0-9][0-9]\.(jpg|png)$", dir_list[0]):
        for filename in dir_list:
            flow = filename.split('.')[0].split('_')
            first = int(flow[1])
            second = int(flow[3])
            if second > first:
                forward_images.append(imageio.imread(f'{frame_folder}/{filename}'))
            else:
                backward_images.append(imageio.imread(f'{frame_folder}/{filename}'))
    elif re.search("frame_[0-9][0-9][0-9][0-9]\.(jpg|png)$", dir_list[0]):
        for filename in dir_list:
            flow = filename.split('.')[0].split('_')
            frame = int(flow[-1])
            if frame < start:
                continue
            elif frame > end:
                break
            else:
                forward_images.append(imageio.imread(f'{frame_folder}/{filename}'))
    else:
        raise ValueError('Unknown file name structure')

    if forward_images != []:
        images_to_gif(forward_images, f'{output_folder}/{output_name}_forward.gif')
    
    if backward_images != []:
        images_to_gif(backward_images[::-1], f'{output_folder}/{output_name}_backward.gif')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='MakeGif',
                    description='Makes a gif from a folder of images named flow_XXXX_XXXX.png')
    parser.add_argument('path', help='The path to the images')
    parser.add_argument('-o', '--output_path', default='./', help='The path to write the output to')
    parser.add_argument('-n', '--output_name', default='', help='The name to append to the gif')
    parser.add_argument('-s', '--start', default=0, help='The starting frame')
    parser.add_argument('-e', '--end', default=10, help='The ending frame')

    args = parser.parse_args()
    if args.path == args.output_path:
        raise ValueError('The paths must not match')

    make_gif(args.path, args.output_path, args.output_name, int(args.start), int(args.end))