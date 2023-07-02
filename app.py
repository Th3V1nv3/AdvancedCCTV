from flask import Flask, render_template, request
import moviepy.editor as mp # this is a library for working with videos

app = Flask(__name__)

@app.route('/')
def index():
    # this is the home page of the website
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # this is the page where the user can upload a video
    if request.method == 'POST':
        # get the uploaded file from the form
        video = request.files['video']
        # save the video to a temporary location
        video.save('temp.mp4')
        # load the video using moviepy
        clip = mp.VideoFileClip('temp.mp4')
        # get the duration and other information of the video
        duration = clip.duration
        width = clip.w
        height = clip.h
        fps = clip.fps
        # render the results page with the video information
        return render_template('results.html', duration=duration, width=width, height=height, fps=fps)
    else:
        # render the upload page with a form to upload a video
        return render_template('upload.html')
