from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import moviepy.editor as mp # this is a library for working with videos

app = Flask(__name__)
app.jinja_env.add_extension ('jinja2.ext.loopcontrols')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'User( {self.user_name}, {self.password})'
    
class Metadata(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, nullable=False)
        duration = db.Column(db.String(16), nullable=False)
        startTime = db.Column(db.String(16), nullable=False)
        videoName = db.Column(db.String(200), nullable=False)
        searchKey = db.Column(db.Float, nullable=False)

        def __repr__(self):
            return f'Matadata( {self.user_name}, {self.password})'
        

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
        startTime = clip.start
        width = clip.w
        height = clip.h
        fps = clip.fps

        metadata = Metadata(user_id = 1 , duration = duration , startTime = startTime , videoName = "testeName 123" , )
        # render the results page with the video information
        return render_template('results.html', duration=duration, width=width, height=height, fps=fps)
    else:
        # render the upload page with a form to upload a video
        return render_template('upload.html')

@app.route('/history')
def history():
    # this is the home page of the website
    return render_template('history.html')