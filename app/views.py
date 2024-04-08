# Important imports
from app import app
from flask import request, render_template, url_for
import os
import cv2
import numpy as np
from PIL import Image
import random
import string
import easyocr  # Using easyocr instead of pytesseract

# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = 'app/static/uploads'


# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():
    # Execute if request is get
    if request.method == "GET":
        full_filename = 'images/white_bg.jpg'
        return render_template("index.html", full_filename=full_filename)

    # Execute if request is post
    if request.method == "POST":
        image_upload = request.files['image_upload']
        imagename = image_upload.filename
        image = Image.open(image_upload)

        # Converting image to array
        image_arr = np.array(image.convert('RGB'))
        # Converting image to grayscale
        gray_img_arr = cv2.cvtColor(image_arr, cv2.COLOR_BGR2GRAY)
        # Converting image back to RGB
        image = Image.fromarray(gray_img_arr)

        # Printing lowercase
        letters = string.ascii_lowercase
        # Generating unique image name for dynamic image display
        name = ''.join(random.choice(letters) for i in range(10)) + '.png'
        full_filename = 'uploads/' + name

        # Using EasyOCR to extract text
        reader = easyocr.Reader(['en'])  # 'en' is for English
        results = reader.readtext(gray_img_arr)

        # Extracting text and bounding boxes
        text_list = [text[1] for text in results]  # Extracting the text from results

        # Converting list of text to a single string separated by new lines
        new_string = "\n".join(text_list)

        # Saving image to display in html
        img = Image.fromarray(image_arr, 'RGB')
        img.save(os.path.join(app.config['INITIAL_FILE_UPLOADS'], name))
        # Returning template, filename, extracted text
        return render_template('index.html', full_filename=full_filename, text=new_string.split("\n"))


# Main function
if __name__ == '__main__':
    app.run(debug=True)
