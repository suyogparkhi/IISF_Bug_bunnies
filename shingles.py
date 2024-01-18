import os
import pickle

def generate_file_paths(folder_path, num_files):
    file_paths = []
    for i in range(num_files):
        file_name = f"file{i:02d}.txt"
        file_path = os.path.join(folder_path, file_name)
        file_paths.append(file_path)
    return file_paths

def update_file(file_path):
    try:
        with open(file_path, "r+", encoding="utf-8", errors="replace") as f:
            words = f.read().split(" ")

            if len(words) < 3:
                f.seek(0)
                f.write(" IISF(IndiaInternationalScienceFestival) ISRO 2023 ")
                f.seek(0)
                words = f.read().split(" ")

        return words

    except UnicodeDecodeError as e:
        print(f"Error decoding file {file_path}: {e}")
        return None

def generate_shingles(file_paths):
    shingle_dict = {}
    doc_shingle_dict = {}
    count = 0

    for file_path in file_paths:
        print(file_path)
        words = update_file(file_path)
        
        if words is None:
            continue

        temp = set()
        for index in range(len(words) - 2):
            shingle = words[index] + " " + words[index + 1] + " " + words[index + 2]
            if shingle not in shingle_dict:
                shingle_dict[shingle] = count
                count += 1
            temp.add(shingle_dict[shingle])

        doc_shingle_dict[os.path.basename(file_path).split(".")[0]] = temp

    return shingle_dict, doc_shingle_dict


def main():
    folder1_path = "C:\\Users\\ekans\\OneDrive\\Desktop\\IISF_Bug_bunnies-main\\txt_out"
    files = os.listdir(folder1_path)
    num_files = len([f for f in files if os.path.isfile(os.path.join(folder1_path, f))])
    folder1_file_paths = generate_file_paths(folder1_path, num_files)

    file_paths = folder1_file_paths

    shingle_dict, doc_shingle_dict = generate_shingles(file_paths)

    output = open("docShingleDict.pkl", 'wb')
    pickle.dump(doc_shingle_dict, output)
    output.close()

    return len(shingle_dict)

