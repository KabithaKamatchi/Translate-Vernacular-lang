from flask import (Flask, flash, make_response, redirect, render_template,
                   request, session, url_for)
import secrets
import bcrypt

from app import *

from modules.utils import *
from modules.preprocessor import *

common_language = {
    "Bengali": "ben_Beng",
    "Gujarati": "guj_Gujr",
    "Hindi": "hin_Deva",
    "Kannada": "kan_Knda",
    "Malayalam": "mal_Mlym",
    "Marathi": "mar_Deva",
    "Nepali": "npi_Deva",
    "Sinhala": "sin_Sinh",
    "Tamil": "tam_Taml",
    "Telugu": "tel_Telu",
    "Urdu": "urd_Arab",
    "English": "eng_Latn"
}

@app.route('/test')
def test():
    return render_template('dashboard.html')

@app.route('/')
def home():
    return render_template('index.html')

#SignUp
@app.route('/register', methods=["POST", "GET"])
def signup():
    message = ''
    if "email" in session:
        return redirect('/dashboard')

    if request.method == "POST":
        user = request.form.get("name")
        email = request.form.get("email")
        lang = request.form.getlist("lang")
        lang.pop(0)
        password1 = request.form.get("password")
        password2 = request.form.get("cpassword")

        user_found = db.user.find_one({"name": user})
        email_found = db.user.find_one({"email": email})
        
        user_key = secrets.token_urlsafe(16)

        if user_found:
            message = 'There already is a user by that name'
            return render_template('login.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('login.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('login.html', message=message)

        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed, 'key': user_key, 'lang': lang}
            db.user.insert_one(user_input)
            
            user_data = db.user.find_one({"email": email})
            new_email = user_data['email']
   
            return redirect('/dashboard')

    return render_template('register.html',common_language = common_language)

#Login
@app.route('/login', methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect('/dashboard')

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
       
        email_found = db.user.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']
            
            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect('/dashboard')
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)

    return render_template('login.html', message=message)

#logout
@app.route("/logout", methods=["POST", "GET"])
def logout():
    if "email" in session:
        session.pop("email", None)
        return redirect('/login')
    else:
        return redirect('/login')



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard():
    if "email" in session:
        return render_template('dashboard.html')
    else:
        return redirect('/login')

@app.route('/services')
def service():
    return render_template('services.html')

@app.route('/text', methods=["POST", "GET"])
def text():
    if "email" in session:
        if request.method == "POST":
            lag = request.form.get("lag")
            text = request.form.get("text") 
            sourceLang = dectLang(text)
            translatedText = text2textTranslation(source=sourceLang, target=lag, text=text)
            return render_template('text.html', translatedText=translatedText,common_language = common_language)
        return render_template('text.html',common_language = common_language)

    else:
        return redirect('/login')

# input - video file and language
# output - translated audio filepath
@app.route('/video', methods=["POST", "GET"])
def video():
    if "email" in session:
        
        if request.method == "POST":
            file = request.files['file']
            language = ""
            if file.filename == '' :
                flash('No image selected for uploading')
                return redirect(request.url)   
    
            else:
                audiofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'audio')
                translatedaudiofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'translatedaudio')
                videofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'video')
                videopath = os.path.join(videofolder, file.filename)
                translatedaudiopath = os.path.join(translatedaudiofolder, file.filename)
                combinedvideopath = os.path.join(app.config['UPLOAD_FOLDER'], 'combinedvideo',file.filename)
                file.save(videopath)
                audiopath = extract_video_audio(videopath,file.filename,audiofolder)
                translated_text = englishaudio_englishtext(audiopath,language)
                text_audio(translated_text,language,translatedaudiopath)
                combine_audio_video(videopath,translatedaudiopath,combinedvideopath)
                return combinedvideopath
        #     # lag = request.form.get("lag")
        #     text = request.form.get("text")
        #     lag= "tam_Taml"
        #     sourceLang = dectLang(text)
        #     translatedText = text2textTranslation(source=sourceLang, target=lag, text=text)
        #     return render_template('text.html', translatedText=translatedText)
        return render_template('videotovideo.html')

    else:
        return redirect('/login')


# input - audio file and language
# output - translated audio filepath
@app.route('/audio', methods=["POST", "GET"])
def audio():
    if "email" in session:
        
        if request.method == "POST":
            file = request.files['file']
            language = ""
            if file.filename == '' :
                flash('No image selected for uploading')
                return redirect(request.url)   
    
            else:
                audiopath = os.path.join(app.config['UPLOAD_FOLDER'], 'audio',file.filename)
                translatedaudiofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'translatedaudio')
                translatedaudiopath = os.path.join(translatedaudiofolder, file.filename)
                file.save(audiopath)
                translated_text = englishaudio_englishtext(file.filename,language)
                text_audio(translated_text,language,translatedaudiopath)
                return translatedaudiopath
        #     # lag = request.form.get("lag")
        #     text = request.form.get("text")
        #     lag= "tam_Taml"
        #     sourceLang = dectLang(text)
        #     translatedText = text2textTranslation(source=sourceLang, target=lag, text=text)
        #     return render_template('text.html', translatedText=translatedText)
        return render_template('videotovideo.html')

    else:
        return redirect('/login')
    

# input - url and language
# output - translated video filepath
@app.route('/youtubevideo', methods=["POST", "GET"])
def youtubevideo():
    if "email" in session:
        
        if request.method == "POST":
            url = ""
            language = ""
            if url == '' :
                flash('No url is selected for translating')
                return redirect(request.url)   
    
            else:
                videofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'video')
                filename = download_youtube_video(url,videofolder)
                audiofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'audio')
                translatedaudiofolder = os.path.join(app.config['UPLOAD_FOLDER'], 'translatedaudio')
                videopath = os.path.join(videofolder, filename)
                translatedaudiopath = os.path.join(translatedaudiofolder, filename)
                combinedvideopath = os.path.join(app.config['UPLOAD_FOLDER'], 'combinedvideo', filename)
                audiopath = extract_video_audio(videopath,filename,audiofolder)
                translated_text = englishaudio_englishtext(audiopath,language)
                text_audio(translated_text,language,translatedaudiopath)
                combine_audio_video(videopath,translatedaudiopath,combinedvideopath)
                return combinedvideopath
        #     # lag = request.form.get("lag")
        #     text = request.form.get("text")
        #     lag= "tam_Taml"
        #     sourceLang = dectLang(text)
        #     translatedText = text2textTranslation(source=sourceLang, target=lag, text=text)
        #     return render_template('text.html', translatedText=translatedText)
        return render_template('videotovideo.html')

    else:
        return redirect('/login')