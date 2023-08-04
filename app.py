from flask import Flask, render_template, request,make_response , redirect,url_for
from flask_sqlalchemy import SQLAlchemy
import moviepy.editor as mp # this is a library for working with videos
import random
from fpdf import FPDF
from datetime import date

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
        
rout = 0

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
        id = 0

        metadata = Metadata(user_id = 1 , duration = "duration" , startTime = startTime , videoName = videoName ,searchKey = searchKey ,accuracy = accuracy)
        with app.app_context():
            #db.create_all()
            db.session.add(metadata)
            db.session.commit()
            db.session.refresh(metadata)
            id = metadata.id

        # render the results page with the video information
        return render_template('results.html', duration = duration , startTime = startTime , videoName = videoName ,searchKey = searchKey , accuracy = accuracy ,id = id )
    else:
        # render the upload page with a form to upload a video
        return render_template('upload.html')

@app.route('/history')
def history():
    metadataList = Metadata.query.all()
    # this is the home page of the website
    return render_template('history.html',metadataList = metadataList)

@app.route('/download/<int:id>', methods=['GET', 'POST'])
def download(id):
    metadata = Metadata.query.get_or_404(id)

    pdf = FPDF()
 
    # Add a page
    pdf.add_page()

    pdf.set_font("Arial", size = 15)

    pdf.cell(200, 10, txt = "PDF analyser",ln = 1, align = 'R')
    pdf.cell(200, 10, txt = "Video name "+metadata.videoName,ln = 4, align = 'L')
    pdf.cell(200, 10, txt = "Duration "+str(metadata.duration),ln = 5, align = 'L')
    pdf.cell(200, 10, txt = "Start time "+metadata.startTime,ln = 6, align = 'L')
    pdf.cell(200, 10, txt = "Search key "+metadata.searchKey,ln = 7, align = 'L')
    pdf.cell(200, 10, txt = "Accuracy "+str(metadata.accuracy),ln = 4, align = 'L')
    #---------------------------------
    pdf.output("output.pdf")  

    # Return the PDF file as a response
    response = make_response(open("output.pdf", "rb").read())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=output.pdf"
    return response

@app.route('/login/<int:route>')
def login(route):
 
    return render_template('login.html' , route = route)

@app.route('/createAccount')
def createAccount():

    return render_template('createAccount.html')

   
@app.route('/verifyLogin' , methods=['GET', 'POST'])
def verifyLogin():
    username = request.form["username"]
    password = request.form["password"]
    route = request.form["route"]

    #user = User.query.filter_by(user_name=username).first()
    print("the route um is - "+route)
    if route == '1':
        return redirect(url_for('upload'))
    else :
        return redirect(url_for('history'))

@app.route('/accountCreation' , methods=['GET', 'POST'])
def accountCreation():
    username = request.form["username"]
    password = request.form["password"]

    #user = User.query.filter_by(user_name=username).first()
    
 
    return redirect('/login/'+str(rout))