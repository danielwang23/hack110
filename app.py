from flask import Flask, render_template, request
from colorthief import ColorThief 
from scipy.spatial import KDTree
from webcolors import hex_to_rgb, CSS3_HEX_TO_NAMES
import os


# The purpose of the flask file is to create a dynamic page, otherwise if you just used a href to index2.html it would just be a static page

app: Flask = Flask(__name__, static_folder='/Users/danielwang/hack110/pictures')
 
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/color")
def color():

    ct = ColorThief("pictures/Starwars.png")
    dominant_color = ct.get_color(quality = 1)
    color_as_a_string = convert_rgb_to_names(dominant_color)

    return render_template('index2.html', dominant_color_string = color_as_a_string)

def convert_rgb_to_names(rgb_tuple):
    
    # a dictionary of all the hex and their respective names in css3
    css3_db = CSS3_HEX_TO_NAMES
    names = []
    rgb_values = []
    for color_hex, color_name in css3_db.items():
        names.append(color_name)
        rgb_values.append(hex_to_rgb(color_hex))
    
    kdt_db = KDTree(rgb_values)
    distance, index = kdt_db.query(rgb_tuple)
    return f'closest match: {names[index]}'

UPLOAD_FOLDER = 'pictures'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'fileInput' not in request.files:
        return 'No file part'

    file = request.files['fileInput']

    if file.filename == '':
        return 'No selected file'

    if file:
        filename = file.filename
        # file.save(filename)
        
 
        ct = ColorThief(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        dominant_color = ct.get_color(quality = 1)
        color_as_a_string = convert_rgb_to_names(dominant_color)

        # return f'File uploaded successfully: {filename}'
        return render_template('index2.html', dominant_color_string = color_as_a_string, filename = "/pictures/" + filename)

if __name__ == '__main__':
    app.run(debug=True)