from flask import Flask, render_template, request, flash, redirect, url_for
import os

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
        input_folder1 = request.form['source_directory']
        input_folder2 = request.form['destination_directory']
        output_folder_txt = 'C:\\Users\\ekans\\OneDrive\\Documents\\SIF 2023\\flask\\flask\\txt_out'
        output_folder_jpg = 'C:\\Users\\ekans\\OneDrive\\Documents\\SIF 2023\\flask\\flask\\img_out'
        
        if not input_folder1 or not input_folder2:
            flash('Both source and destination directories are required.', 'error')
        else:
            form.source_dir = os.path.abspath(input_folder1)
            form.dest_dir = os.path.abspath(input_folder2)

            # Process folder1 and folder2
            mapping_folder1, file_counter1 = conversion.process_folder(input_folder1, output_folder_txt, output_folder_jpg, folder_number=1)
            mapping_folder2, file_counter2 = conversion.process_folder(input_folder2, output_folder_txt, output_folder_jpg, folder_number=2, file_counter_start=file_counter1)

             # Combine the mapping dictionaries
            filename_mapping = {**mapping_folder1, **mapping_folder2}
    
            json_file_path = "C:\\Users\\ekans\\OneDrive\\Documents\\SIF 2023\\mapping.json"
            with open(json_file_path, 'w') as json_file:
                json.dump(filename_mapping, json_file, indent=4)
            no_shingles = shingles.main()
            duplicates = minhash.run_minhash(no_shingles, "C:\\Users\\ekans\\OneDrive\\Documents\\SIF 2023\\docShingleDict.pkl")
            if duplicates:
                return render_template('results.html', form=form, duplicates=duplicates)
            else:
                return render_template('results.html', form=form, no_duplicates=True)

    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', form=form, files=files)

def find_duplicates(source_dir, dest_dir):
    source_files = get_all_files(source_dir)
    dest_files = get_all_files(dest_dir)

    duplicate_files = set(source_files) & set(dest_files)
    return list(duplicate_files)

def get_all_files(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files

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

if __name__ == '__main__':
    app.run(debug=True)
