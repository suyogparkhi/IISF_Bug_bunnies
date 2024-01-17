import os
from PyPDF2 import PdfReader
from PIL import Image
from dbfread import DBF
from pyproj import Proj

def convert_pdf_to_text(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()

            # Remove spaces from each line and concatenate
            text += ''.join(page_line.strip() for page_line in page_text.split('\n'))

    return text

def convert_tif_to_jpg(tif_path, output_folder):
    try:
        img = Image.open(tif_path)
        jpg_filename = os.path.splitext(os.path.basename(tif_path))[0] + '_folderJPG.jpg'
        jpg_path = os.path.join(output_folder, jpg_filename)
        img.save(jpg_path, 'JPEG')
        return jpg_path
    except Exception as e:
        print(f"Error converting {tif_path} to JPG: {e}")
        return None
    
    

def convert_file_to_txt(file_name, output_folder, folder_number, file_counter):
    # Determine the file type based on the extension
    file_extension = os.path.splitext(file_name)[1].lower()

    try:
        if file_extension == '.pdf':
            content = convert_pdf_to_text(file_name)
            txt_filename = f'file{file_counter:02d}.txt'
            txt_file_path = os.path.join(output_folder, txt_filename)
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(content)
        elif file_extension == '.dbf':
            records = list(DBF(file_name))
            txt_filename = f'file{file_counter:02d}.txt'
            txt_file_path = os.path.join(output_folder, txt_filename)
            with open(txt_file_path, 'w') as txt:
                for record in records:
                    txt.write(str(record) + '\n')
        elif file_extension == '.prj':
            txt_filename = f'file{file_counter:02d}.txt'
            txt_file_path = os.path.join(output_folder, txt_filename)
            with open(file_name, 'r') as prj, open(txt_file_path, 'w') as txt:
                txt.write(prj.read())
        elif file_extension in ['.tif', '.tiff']:
            # Handle TIF files
            txt_filename = f'file{file_counter:02d}.txt'
            txt_file_path = os.path.join(output_folder, txt_filename)
            jpg_path = convert_tif_to_jpg(file_name, output_folder)
            if jpg_path:
                print(f'Converted {file_name} to {jpg_path}')
                return jpg_path
            else:
                return None
        elif file_extension in ['.shx', '.sbx', '.shp']:
            # Handle SHX, SBX, SHP files
            txt_filename = f'file{file_counter:02d}.txt'
            txt_file_path = os.path.join(output_folder, txt_filename)
            # Add your logic here for SHX, SBX, SHP files
            # For now, just read in binary mode and write as text
            with open(file_name, 'rb') as data, open(txt_file_path, 'w') as txt_file:
                try:
                    content = data.read().decode('utf-8')
                except UnicodeDecodeError:
                    print(f"Warning: {file_name} is not a text file. Treating as binary.")
                    return None
                txt_file.write(content)
        else:
            # For other file types, read in binary mode and write as text
            txt_filename = f'file{file_counter:02d}.txt'
            txt_file_path = os.path.join(output_folder, txt_filename)
            with open(file_name, 'rb') as data, open(txt_file_path, 'w') as txt_file:
                try:
                    content = data.read().decode('utf-8')
                except UnicodeDecodeError:
                    print(f"Warning: {file_name} is not a text file. Treating as binary.")
                    return None
                txt_file.write(content)

        return txt_file_path

    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        return None

def process_folder(input_folder, output_folder_txt, output_folder_jpg, folder_number, file_counter_start=0):
    file_counter = file_counter_start
    redundancy_mapping = {}

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            file_path = os.path.join(root, file)

            # Process TIF files separately and continue to the next iteration
            if file.lower().endswith(('.tif', '.tiff','jpg', 'jpeg', 'png')):
                jpg_path = convert_tif_to_jpg(file_path, output_folder_jpg)
                if jpg_path:
                    print(f'Converted {file} to {jpg_path}')
                continue

            txt_file_path = convert_file_to_txt(file_path, output_folder_txt, folder_number, file_counter)
            if txt_file_path:
                print(f'Converted {file} to {txt_file_path}')
                redundancy_mapping[os.path.basename(txt_file_path)] = os.path.join(root, file)
                file_counter += 1
    return redundancy_mapping, file_counter



