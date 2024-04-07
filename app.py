import os
import random
print(random.randrange(10000,200000))
import datetime
# import mutagen
# from mutagen import mp3,mp4,ogg
# from mutagen.mp3 import MP3
# from mutagen.mp4 import MP4
# from mutagen.ogg import OggFileType
# audio=mutagen(file_name)
# audio.length()
from werkzeug.utils import secure_filename
from flask import Flask,render_template,request,redirect,url_for,flash
from modal import * # importing from modal

############################################################################################################
#curr_dir = os.path.abspath(os.path.dirname(__file__))  # Directory Path
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Refugee.sqlite3" # Database connection for using database values
app.config['SECRET_KEY'] = 'secret' # Admin session available
app.config ['UPLOAD_FOLDER'] = 'static/uploads'
app.app_context().push()
db.init_app(app)
############################################################################################################
# Extra Functions start from here
# Genres=['Pop','Rock','Hip&Hop','Rap','Country','R & B','Folk','Jazz','Heavy Metal','EDM','Soul','Funk','Raggae','Disco','Punk Rock','Classical','House','Techno','Indie Rock']
Languages=['Hindi','English','Punjabi','Marathi','Bengali']
Ratings = [1,2,3,4,5]
ALLOWED_EXTENSIONS = {'.png','.jpg','.jpeg','.ogg','.mp3'}
#def get_duration(file_name,file_path):
 #   if file_path.endswith('.mp3'):
  #      audio = MP3(file_name)
   # elif file_path.endswith('.mp4'):
    #    audio = MP4(file_name)
    #elif file_path.endswith('.ogg'):
     #   audio = OggFileType(file_name)
    #return audio.info.length
def verify_user(list1,email_address,password):
    for i in list1:
        if i.name==email_address and i.uid==password:
            return 1
    return 0
def allowed_file(filename):
    global ALLOWED_EXTENSIONS
    return '.'in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
def verify(email,password):
    if(email=='arinvashisth@gmail.com' and password=='2004'):
        return True
    else:
        return False
def check_gender(var):
    if var=='1':
        return 'Male'
    elif var=='2':
        return 'Female'
    else:
        return 'Rather not say'
#def applogg(ver):
 #   if ver:
  #      inputs = User()
   #     db.session.add(inputs)
    #    db.session.commit()
def verify2(logg):
    if logg=='1':
        return 1
    else:
        return 0
def verlogin(us):
    if us is None:
        return 0
    else:
        return 1
# def check(creator_or_user):
    


# WEBPAGE Functions start from here
""" HOME PAGE"""
@app.route('/',methods=["GET","POST"])
def Home():
    if request.method == "POST":
        name = request.form.get('name')
        address = request.form.get('address')
        email_address = request.form.get('email')
        pass1 = random.randrange(1000000,99999999)
        gender = request.form.get('gender')
        gender = check_gender(gender)
        profile = request.files['profile']
        file_path = None
        if 'file' not in request.files['profile']:
            flash('No file part')
        if profile.filename == '':
            flash('No selected file')
        if profile and allowed_file(profile.filename):
            filename = secure_filename(profile.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            profile.save(file_path)

        dob = request.form.get('dob')
        dob=datetime.datetime.strptime(dob, "%Y-%m-%d").date()
        inputs = Reugee(name=name,address=address,email_address=email_address,uid=pass1,gender=gender,dob=dob,profile=file_path)
        db.session.add(inputs)
        db.session.commit()
        return redirect(url_for('Home'))
    return render_template('register.html')

@app.route('/login',methods=["GET","POST"])
def loginn():
    if request.method=="POST":
        list1=Reugee.query.all()
        uname=request.form.get('name')
        upassid=request.form.get('password')
        if(verify_user(list1,uname,upassid)):
            cred=upassid
            return redirect(url_for('Card',n=cred))

    return render_template('base.html')


@app.route('/card/<string:n>',methods=["GET","POST"])
def Card(n):
    list1=Reugee.query.filter_by(uid=n).first()
    return render_template('car.html',list1=list1)

@app.route('/index',methods=["GET","POST"])
def Index():
    return render_template('index.html')


@app.route('/admin',methods=["GET","POST"])
def Admin():
    list1=Reugee.query.all()
    return render_template('/admin/admin_ref.html',list1=list1)

@app.route('/uquery',methods=["GET","POST"])
def Uquery():
    return render_template('uquery.html')



@app.route('/delete/<int:n>',methods=["GET","POST"])
def dele(n):
    record = Reugee.query.filter_by(id=n).first()
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('Admin'))





if __name__ == "__main__":
    app.run(debug = True,port=3000)