from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import moviepy.editor as mp # this is a library for working with videos
import random

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
        searchKey = db.Column(db.String(100), nullable=False)
        accuracy = db.Column(db.Float, nullable=False)

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
        searchKey = request.form.get("searchKey")
        # save the video to a temporary location
        videoName = video.filename
        video.save('temp.mp4')
        # load the video using moviepy
        clip = mp.VideoFileClip('temp.mp4')
        # get the duration and other information of the video
        duration = clip.duration
        startTime = str(random.randint(0,59)) + ":" + str(random.randint(0, 59))
        accuracy = 94

        metadata = Metadata(user_id = 1 , duration = "duration" , startTime = startTime , videoName = videoName ,searchKey = searchKey ,accuracy = accuracy)
        #with app.app_context():
            #db.create_all()
            #db.session.add(metadata)
            #db.session.commit()

        # render the results page with the video information
        return render_template('results.html', duration = duration , startTime = startTime , videoName = videoName ,searchKey = searchKey , accuracy = accuracy)
    else:
        # render the upload page with a form to upload a video
        return render_template('upload.html')

@app.route('/history')
def history():
    # this is the home page of the website
    return render_template('history.html')