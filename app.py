from flask import Flask, render_template, request, redirect, url_for, flash
import os , folium
import subprocess
import conversion
import shingles
import minhash
import json , test1
# import send_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'tar.gz', 'rpm', 'pix', 'cfg', 'exe', 'min.js', 'log', 'xlsx', 'zip', 'sh', 'bk', 'sql', 'jpeg', 'png', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class CompareForm:
    def __init__(self, source_dir="", dest_dir=""):
        self.source_dir = source_dir
        self.dest_dir = dest_dir

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CompareForm()

    if request.method == 'POST':
        input_folder1 = request.form['folder1']
        input_folder2 = request.form['folder2']
        output_folder_txt = 'txt_out'
        output_folder_jpg = 'img_out'

        # form input
        form.source_dir = os.path.abspath(input_folder1)
        form.dest_dir = os.path.abspath(input_folder2)

        # Process folder1 and folder2
        mapping_folder1, file_counter1 = conversion.process_folder(input_folder1, output_folder_txt, output_folder_jpg, folder_number=1)
        mapping_folder2, file_counter2 = conversion.process_folder(input_folder2, output_folder_txt, output_folder_jpg, folder_number=2, file_counter_start=file_counter1)

        # Combine the mapping dictionaries
        filename_mapping = {**mapping_folder1, **mapping_folder2}

        json_file_path = "mapping.json"
        with open(json_file_path, 'w') as json_file:
            json.dump(filename_mapping, json_file, indent=4)

        no_shingles = shingles.main()
        duplicates = minhash.run_minhash(no_shingles, "docShingleDict.pkl")

        if duplicates:
            return render_template('results.html', form=form, duplicates=duplicates, json_file_path=json_file_path)
        else:
            return render_template('results.html', form=form, no_duplicates=True)

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', form=form, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    files = request.files.getlist('file')

    for file in files:
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    return redirect(url_for('index'))

@app.route('/delete/<filename>')
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect(url_for('index'))

@app.route('/delete_files', methods=['POST'])
def delete_files():
    selected_files = request.form.getlist('selected_files')
    for filename in selected_files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
    return redirect(url_for('index'))

@app.route('/delete_files_from_results', methods=['POST'])
def delete_files_from_results():
    selected_files = request.form.getlist('selected_files')

    # Read the mapping.json file
    with open('mapping.json', 'r') as json_file:
        filename_mapping = json.load(json_file)

    # Delete the selected files from the original directories
    for filename in selected_files:
        file_path = filename_mapping.get(filename)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

    flash('Selected files have been deleted successfully.', 'success')

    # Redirect to the same results.html
    return redirect(url_for('index'))
    
@app.route('/geospatial')
def geospatial():
    return render_template('st_js.html')

# @app.route('/submit_form', methods=['POST'])
# def submit_form():
#     selected_state = request.form.get('stt')
#     with open('geojson1.geojson', 'r') as file:
#         data = json.load(file)

#     filtered_features = [feature for feature in data['features'] if feature['properties']['NAME_1'] == selected_state]

#     filtered_data = {
#         "type": "FeatureCollection",
#         "crs": data["crs"],
#         "features": filtered_features
#     }

#     with open('filtered_geojson.geojson', 'w') as output_file:
#         json.dump(filtered_data, output_file, indent=2)

#     return ("Loading !!!!")

@app.route('/submit_form', methods=['POST'])
def submit_form():
    selected_state = request.form.get('stt')
    with open('geojson1.geojson', 'r') as file:
        data = json.load(file)

    filtered_features = [feature for feature in data['features'] if feature['properties']['NAME_1'] == selected_state]

    filtered_data = {
        "type": "FeatureCollection",
        "crs": data["crs"],
        "features": filtered_features
    }

    with open('filtered_geojson.geojson', 'w') as output_file:
        json.dump(filtered_data, output_file, indent=2)

    # Trigger JavaScript to redirect to /catalog after the "Loading!!!" message
    return '''
    <script>
        alert("Loading !!!!");
        window.location.href = '/catalog';
    </script>
    '''

@app.route('/catalog')

def catalog():
    geojson_file = 'filtered_geojson.geojson'

    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)
    folium.GeoJson(geojson_file).add_to(m)

    map_path = 'templates/map.html'
    m.save(map_path)
    return render_template('map.html')


if __name__ == '__main__':
    app.run(debug=True)
