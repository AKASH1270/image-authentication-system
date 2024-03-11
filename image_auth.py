from flask import Flask, request, render_template, redirect, url_for, flash
from PIL import Image
import hashlib

app = Flask(__name__)
app.secret_key = 'some_secret_key'  # In a real-world scenario, use a strong key.
users_db = {}
def hash_image(image_file):
    """Return a hash of the image."""
    image = Image.open(image_file)
    # Convert image to RGB and then to a byte sequence
    image_bytes = image.convert('RGB').tobytes()
    return hashlib.sha256(image_bytes).hexdigest()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        image_file = request.files['image']

        # Hash the image and store it
        users_db[username] = hash_image(image_file)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        image_file = request.files['image']

        # Hash the submitted image and compare it to the stored hash
        submitted_hash = hash_image(image_file)
        stored_hash = users_db.get(username)

        if submitted_hash == stored_hash:
            return "Successfully Authenticated!"
        else:
            flash("Authentication failed!")
            return redirect(url_for('login'))

    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
