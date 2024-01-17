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
        source_dir = request.form['source_directory']
        dest_dir = request.form['destination_directory']

        if not source_dir or not dest_dir:
            flash('Both source and destination directories are required.', 'error')
        else:
            form.source_dir = os.path.abspath(source_dir)
            form.dest_dir = os.path.abspath(dest_dir)

            duplicates = find_duplicates(source_dir, dest_dir)
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
