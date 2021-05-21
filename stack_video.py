import streamlit as st
import glob, os
from pprint import pprint
from moviepy.editor import VideoFileClip, clips_array, vfx

def stack(file1, file2, nameout, audio=False):
    """
    Stack two videos on top of each other.
    """
    clip1 = VideoFileClip(file1, audio=audio)
    clip2 = VideoFileClip(file2, audio=audio)
    final_clip = clips_array([
        [clip1], # First row (add to this list if you want more than one video in row)
        [clip2] # Second row (add to this list if you want more than one video in row)
    ])
    final_clip.write_videofile(nameout)


list_of_files = {}
for (dirpath, dirnames, filenames) in os.walk("detections/default/"):
    for filename in filenames:
        if filename.endswith('.avi'): 
            default = os.path.join(dirpath, filename)
            custom = os.path.join(dirpath.replace('default', 'custom'), filename)
            nameout = os.path.join("detections/stacked", dirpath.split('/')[-1].replace('default_', ''),  filename.replace('.avi', '.mp4'))
            if os.path.isfile(nameout):
                pprint(f'Already created {nameout}.')
            else:
                pprint(default)
                pprint(custom)
                pprint(nameout)
                stack(default, custom, nameout)
