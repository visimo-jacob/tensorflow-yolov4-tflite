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

def detect(input_file, output_file, default=True):
    """
    Call the detect_video file.
    """

    size_arg = "--size 416"
    model_arg = "--model yolov4"
    vid_arg = f"--video {input_file}"
    out_arg = f"--output {output_file}"
    
    if default:
        weights_arg = "--weights ./checkpoints/yolov4-416"
        os.system(f"python detect_video.py {weights_arg} {size_arg} {model_arg} {vid_arg} {out_arg}")
    
    else:
        weights_arg = "--weights ./checkpoints/custom-416"
        os.system(f"python detect_video_custom.py {weights_arg} {size_arg} {model_arg} {vid_arg} {out_arg}")

################################################################################
# Streamlit Deployment
# 
# In order to run this file successfully in a streamlit environment, run the 
# following command from the terminal:
#   streamlit run stack_video.py --server.maxUploadSize 1024
################################################################################

# Title of app
st.title('YOLOv4 Demo')

# Sidebar
st.sidebar.subheader('Tab1')

option = st.selectbox(
    'Pre-Generated Videos',
    [
        f"{dirpath}/{filename}" 
        for (dirpath, dirnames, filenames) in os.walk("detections/stacked/")
        for filename in filenames
    ]
)

# File upload
uploaded_video = st.sidebar.file_uploader(
    label="Video Upload",
    type=['avi', 'mp4']
)

if uploaded_video is None:
    st.write('You selected:', option)

    video_file = open(f"{option}", 'rb')

else:
    upload_name = uploaded_video.name
    upload_name_avi = upload_name.replace('.mp4', '.avi')
    upload_name_base = upload_name_avi.replace('.avi', '')
    upload_folder = f"streamlit_detections/{upload_name_base}"

    if os.path.exists(f'{upload_folder}'):
        st.write('Video has already been analyzed. Retrieved the previously analyzed video.')
    else:
        os.makedirs(f'{upload_folder}')
        os.makedirs(f'{upload_folder}/start')
        os.makedirs(f'{upload_folder}/custom')
        os.makedirs(f'{upload_folder}/default')

        start_file = f'{upload_folder}/start/{upload_name}'

        # Checks and deletes the output file
        # You cant have a existing file or it will through an error
        if os.path.isfile(start_file):
            os.remove(start_file)

        # opens the file 'output.avi' which is accessable as 'out_file'
        with open(start_file, "wb") as out_file:  # open for [w]riting as [b]inary
            out_file.write(uploaded_video.read())

        input_file = f"./{upload_folder}/start/{upload_name}"
        custom_output = f"./{upload_folder}/custom/{upload_name_avi}"
        default_output = f"./{upload_folder}/default/{upload_name_avi}"

        detect(input_file, default_output, default=True)
        detect(input_file, custom_output, default=False)
    
        stack(default_output, custom_output, f"{upload_folder}/{upload_name_base}.mp4")

    video_file = open(f"{upload_folder}/{upload_name_base}.mp4", 'rb')

    uploaded_video = None

video_bytes = video_file.read()
st.video(video_bytes)