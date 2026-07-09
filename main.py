from flask import Flask, render_template, request ,redirect,url_for
import uuid
from werkzeug.utils import secure_filename
import os

from generate_process import text_to_audio, create_reels

UPLOAD_FOLDER = 'user_upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        rec_id = str(request.form.get("uuid"))
        desc = str(request.form.get("text"))
        
        save_folder = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
        os.makedirs(save_folder, exist_ok=True)

        with open(os.path.join(save_folder, "desc.txt"), "w") as f:
            f.write(desc)

        input_files = []
        for key, value in request.files.items():
            file = request.files[key]
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(save_folder, filename))
                input_files.append(filename)
                
        with open(os.path.join(save_folder, "input.txt"), "w") as f:
            for fl in input_files:
                f.write(f"file '{fl}'\nduration 1\n")   
        #from generate_process.py
        text_to_audio(rec_id)
        create_reels(rec_id) 
            
        return redirect(url_for('gallery'))
        
    fresh_id = str(uuid.uuid1())
    return render_template("create.html", my_uuid=fresh_id)

@app.route("/gallery")
def gallery():
    reels = os.listdir("static/reels")
    print(reels)
    return render_template("gallery.html", reels = reels)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
