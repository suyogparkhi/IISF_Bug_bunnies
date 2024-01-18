from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess
import conversion
import shingles
import minhash
import json , folium
from flask import send_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'C:\\Users\\ekans\\OneDrive\\Desktop\\IISF_Bug_bunnies-main\\uploads'
app.config['SECRET_KEY'] = 'your_secret_key'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'tar.gz', 'rpm', 'pix', 'cfg', 'exe', 'min.js', 'log', 'xlsx', 'zip', 'sh', 'bk', 'sql', 'jpeg', 'png', 'jpg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class CompareForm:
    def __init__(self, source_dir="", dest_dir=""):
        self.source_dir = source_dir
        self.dest_dir = dest_dir

duplicates = [[]]

@app.route('/', methods=['GET', 'POST'])
def index():
    form = CompareForm()

    if request.method == 'POST':
        input_folder1 = request.form['folder1']
        input_folder2 = request.form['folder2']
        output_folder_txt = 'C:\\Users\\ekans\\OneDrive\\Desktop\\IISF_Bug_bunnies-main\\txt_out'
        output_folder_jpg = 'C:\\Users\\ekans\\OneDrive\\Desktop\\IISF_Bug_bunnies-main\\img_out'

        # form input
        form.source_dir = os.path.abspath(input_folder1)
        form.dest_dir = os.path.abspath(input_folder2)

        # Process folder1 and folder2
        mapping_folder1, file_counter1 = conversion.process_folder(input_folder1, output_folder_txt, output_folder_jpg, folder_number=1)
        mapping_folder2, file_counter2 = conversion.process_folder(input_folder2, output_folder_txt, output_folder_jpg, folder_number=2, file_counter_start=file_counter1)

        # Combine the mapping dictionaries
        filename_mapping = {**mapping_folder1, **mapping_folder2}

        json_file_path = "C:\\Users\\ekans\\OneDrive\\Desktop\\IISF_Bug_bunnies-main\\mapping.json"
        with open(json_file_path, 'w') as json_file:
            json.dump(filename_mapping, json_file, indent=4)

        no_shingles = shingles.main()
        duplicates = minhash.run_minhash(no_shingles, "C:\\Users\\ekans\\OneDrive\\Desktop\\IISF_Bug_bunnies-main\\docShingleDict.pkl")
        if duplicates:
            return render_template('results.html', form=form, duplicates=duplicates, json_file_path=json_file_path, filename_mapping=filename_mapping)
        else:
            return render_template('results.html', form=form, no_duplicates=True)

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', form=form, files=files)

def get_file_size(file_name):
    converted_file_path = os.path.join('C:\\Users\\ekans\\OneDrive\\Desktop\\IISF_Bug_bunnies-main\\txt_out', f'{file_name}.txt')

    try:
        size_in_bytes = os.path.getsize(converted_file_path)
        size_in_kb = size_in_bytes / 1024  # Convert bytes to kilobytes
        return f"{size_in_kb:.2f}"  # Displaying size with two decimal places
    except FileNotFoundError:
        return 'N/A'

# ... (your existing code) ...

app.jinja_env.globals.update(get_file_size=get_file_size)

@app.route('/open_file/<filename>', methods=['GET'])
def open_file(filename):
    # Assuming the converted files are stored in 'txt_out' with the same filename
    converted_file_path = os.path.join('C:\\Users\\ekans\\OneDrive\\Desktop\\IISF_Bug_bunnies-main\\txt_out', f'{filename}.txt')

    try:
        # Get the size of the converted file in kilobytes
        with open(converted_file_path, 'r') as converted_file:
            content = converted_file.read()

        return render_template('display_file.html', filename=filename, content=content)
    except FileNotFoundError:
        flash(f'File {filename} not found.', 'error')
        return redirect(url_for('index'))


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
    return redirect(url_for('index'))  # Redirect to the main page after deleting the file

@app.route('/delete_files', methods=['POST'])
def delete_files():
    selected_files = request.form.getlist('selected_files')
    for filename in selected_files:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)

    flash('Selected files have been deleted successfully.', 'success')
    return redirect(url_for('index')) 

@app.route('/delete_files_from_results', methods=['POST'])
def delete_files_from_results():
    selected_files = request.form.getlist('selected_files')

    # Read the mapping.json file
    with open('C:\\Users\\ekans\\OneDrive\\Desktop\\IISF_Bug_bunnies-main\\mapping.json', 'r') as json_file:
        filename_mapping = json.load(json_file)

    # Delete the selected files from the original directories
    for filename in selected_files:
        file_path = filename_mapping.get(filename)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

    flash('Selected files have been deleted successfully.', 'success')

    # Redirect back to the same results.html
    return redirect(request.referrer)



def get_file_size(file_name):
    # Read the mapping.json file
    with open('C:\\Users\\ekans\\OneDrive\\Desktop\\IISF_Bug_bunnies-main\\mapping.json', 'r') as json_file:
        filename_mapping = json.load(json_file)

    # Get the file path using the file name
    file_path = filename_mapping.get(file_name)

    if file_path:
        try:
            # If the file path is found, return its size
            return os.path.getsize(file_path)
        except os.error:
            return 'N/A'  # or any other default value if an error occurs
    else:
        return 'N/A'  # or any other default value if the file name is not in the mapping

# ... (other parts of your app.py code) ...

app.jinja_env.globals.update(get_file_size=get_file_size)

@app.route('/geospatial')
def geospatial():
    return render_template('st_js.html')

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

