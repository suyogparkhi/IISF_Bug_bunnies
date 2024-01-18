# # import pickle
# # import os
# # from heapq import heapify, heappop, heappush
# # import random

# # def run_minhash(no_shingles, pickle_path, threshold=0.9, n_neighbors=3):
# #     pklHandler = open(pickle_path, 'rb')
# #     docShingleDict = pickle.load(pklHandler)
# #     pklHandler.close()

# #     def find_random_nos(k):
# #         return random.sample(range(no_shingles), k)

# #     folder1_path = "C:\\Users\\ekans\\OneDrive\\Documents\\SIF 2023\\flask\\flask\\txt_out"
# #     files = os.listdir(folder1_path)
# #     num_files = len([f for f in files if os.path.isfile(os.path.join(folder1_path, f))])

# #     random_no_a = find_random_nos(3)
# #     random_no_b = find_random_nos(3)

# #     doc_lowest_shingle_id = {}
# #     for doc, shingle_id_set in docShingleDict.items():
# #         lowest_shingle_id = [min((random_no_a[i] * shingle_id + random_no_b[i]) % no_shingles for shingle_id in shingle_id_set) for i in range(3)]
# #         doc_lowest_shingle_id[doc] = lowest_shingle_id

# #     estimate_matrix = []
# #     for i in range(num_files):
# #         doc1 = "file" + str(i).zfill(2)
# #         doc1_lowest_shingles = doc_lowest_shingle_id.get(doc1, [])
# #         col = []
# #         for j in range(num_files):
# #             doc2 = "file" + str(j).zfill(2)
# #             doc2_lowest_shingles = doc_lowest_shingle_id.get(doc2, [])
# #             count = sum(1 for x, y in zip(doc1_lowest_shingles, doc2_lowest_shingles) if x == y)
# #             col.append(count / 3)
# #         estimate_matrix.append(col)

# #     print("\nList of Documents with J(d1,d2) more than", threshold)
# #     for i in range(num_files):
# #         file1 = "file" + str(i).zfill(2)
# #         for j in range(num_files):
# #             if estimate_matrix[i][j] > threshold and i != j:
# #                 file2 = "file" + str(j).zfill(2)
# #                 shingles_set1 = docShingleDict[file1]
# #                 shingles_set2 = docShingleDict[file2]
# #                 print("d1:", file1, "and d2:", file2)
# #                 print("J(d1,d2):", estimate_matrix[i][j])
# #                 jaccard = len(shingles_set1.intersection(shingles_set2)) / len(shingles_set1.union(shingles_set2))
# #                 print("Jaccard coefficient:", jaccard)
# #                 print()

# #     doc_jaccard = {}

# #     def pop(jaccard_list):
# #         for _ in range(min(n_neighbors, len(jaccard_list))):
# #             estimated_jaccard_c, file_x = heappop(jaccard_list)
# #             print(file_x, end=' ')

# #     print(f"\n{n_neighbors} nearest neighbors for each file with threshold > {threshold}")
# #     for i in range(num_files):
# #         file1 = "file" + str(i).zfill(2)
# #         estimated_jaccard_list = [(-estimate_matrix[i][j], "file" + str(j).zfill(2)) for j in range(num_files) if i != j and estimate_matrix[i][j] > threshold]
# #         heapify(estimated_jaccard_list)
# #         print("\n" + file1 + ":", end=' ')
# #         pop(estimated_jaccard_list)
# # import pickle
# # import os
# # from heapq import heapify, heappop, heappush
# # import random

# # def run_minhash(no_shingles, pickle_path, threshold=0.9, n_neighbors=3):
# #     pklHandler = open(pickle_path, 'rb')
# #     docShingleDict = pickle.load(pklHandler)
# #     pklHandler.close()

# #     def find_random_nos(k):
# #         return random.sample(range(no_shingles), k)

# #     folder1_path = "C:\\Users\\ekans\\OneDrive\\Documents\\SIF 2023\\flask\\flask\\txt_out"
# #     files = os.listdir(folder1_path)
# #     num_files = len([f for f in files if os.path.isfile(os.path.join(folder1_path, f))])

# #     random_no_a = find_random_nos(3)
# #     random_no_b = find_random_nos(3)

# #     doc_lowest_shingle_id = {}
# #     for doc, shingle_id_set in docShingleDict.items():
# #         lowest_shingle_id = [min((random_no_a[i] * shingle_id + random_no_b[i]) % no_shingles for shingle_id in shingle_id_set) for i in range(3)]
# #         doc_lowest_shingle_id[doc] = lowest_shingle_id

# #     estimate_matrix = []
# #     for i in range(num_files):
# #         doc1 = "file" + str(i).zfill(2)
# #         doc1_lowest_shingles = doc_lowest_shingle_id.get(doc1, [])
# #         col = []
# #         for j in range(num_files):
# #             doc2 = "file" + str(j).zfill(2)
# #             doc2_lowest_shingles = doc_lowest_shingle_id.get(doc2, [])
# #             count = sum(1 for x, y in zip(doc1_lowest_shingles, doc2_lowest_shingles) if x == y)
# #             col.append(count / 3)
# #         estimate_matrix.append(col)

# #     print("\nList of Documents with J(d1,d2) more than", threshold)

# #     redundancy_sets = set()

# #     for i in range(num_files):
# #         file1 = "file" + str(i).zfill(2)
# #         redundant_set = set([file1])
# #         for j in range(num_files):
# #             if estimate_matrix[i][j] > threshold and i != j:
# #                 file2 = "file" + str(j).zfill(2)
# #                 redundant_set.add(file2)
# #                 shingles_set1 = docShingleDict[file1]
# #                 shingles_set2 = docShingleDict[file2]
# #                 print("d1:", file1, "and d2:", file2)
# #                 print("J(d1,d2):", estimate_matrix[i][j])
# #                 jaccard = len(shingles_set1.intersection(shingles_set2)) / len(shingles_set1.union(shingles_set2))
# #                 print("Jaccard coefficient:", jaccard)
# #                 print()

# #         # Check if any element in the redundant set is already in any other set
# #         if not any(redundant_set.intersection(s) for s in redundancy_sets):
# #             redundancy_sets.add(frozenset(redundant_set))

# #     print("\nRedundancy Sets:")
# #     for idx, redundant_set in enumerate(redundancy_sets, 1):
# #         print(f"Redundancy Set {idx}: {redundant_set}")

# #     doc_jaccard = {}

# #     def pop(jaccard_list):
# #         for _ in range(min(n_neighbors, len(jaccard_list))):
# #             estimated_jaccard_c, file_x = heappop(jaccard_list)
# #             print(file_x, end=' ')

# #     print(f"\n{n_neighbors} nearest neighbors for each file with threshold > {threshold}")
# #     for i in range(num_files):
# #         file1 = "file" + str(i).zfill(2)
# #         estimated_jaccard_list = [(-estimate_matrix[i][j], "file" + str(j).zfill(2)) for j in range(num_files) if i != j and estimate_matrix[i][j] > threshold]
# #         heapify(estimated_jaccard_list)
# #         print("\n" + file1 + ":", end=' ')
# #         pop(estimated_jaccard_list)

# #     return redundancy_sets

# import pickle
# import os
# from heapq import heapify, heappop, heappush
# import random

# def run_minhash(no_shingles, pickle_path, threshold=0.9, n_neighbors=3):
#     pklHandler = open(pickle_path, 'rb')
#     docShingleDict = pickle.load(pklHandler)
#     pklHandler.close()

#     def find_random_nos(k):
#         return random.sample(range(no_shingles), k)

#     folder1_path = "C:\\Users\\ekans\\OneDrive\\Documents\\SIF 2023\\flask\\flask\\txt_out"
#     files = os.listdir(folder1_path)
#     num_files = len([f for f in files if os.path.isfile(os.path.join(folder1_path, f))])

#     random_no_a = find_random_nos(3)
#     random_no_b = find_random_nos(3)

#     doc_lowest_shingle_id = {}
#     for doc, shingle_id_set in docShingleDict.items():
#         lowest_shingle_id = [min((random_no_a[i] * shingle_id + random_no_b[i]) % no_shingles for shingle_id in shingle_id_set) for i in range(3)]
#         doc_lowest_shingle_id[doc] = lowest_shingle_id

#     estimate_matrix = []
#     for i in range(num_files):
#         doc1 = "file" + str(i).zfill(2)
#         doc1_lowest_shingles = doc_lowest_shingle_id.get(doc1, [])
#         col = []
#         for j in range(num_files):
#             doc2 = "file" + str(j).zfill(2)
#             doc2_lowest_shingles = doc_lowest_shingle_id.get(doc2, [])
#             count = sum(1 for x, y in zip(doc1_lowest_shingles, doc2_lowest_shingles) if x == y)
#             col.append(count / 3)
#         estimate_matrix.append(col)

#     print("\nList of Documents with J(d1,d2) more than", threshold)

#     redundancy_sets = set()

#     for i in range(num_files):
#         file1 = "file" + str(i).zfill(2)
#         redundant_set = set([file1])
#         for j in range(num_files):
#             if estimate_matrix[i][j] > threshold and i != j:
#                 file2 = "file" + str(j).zfill(2)
#                 redundant_set.add(file2)
#                 shingles_set1 = docShingleDict[file1]
#                 shingles_set2 = docShingleDict[file2]
#                 print("d1:", file1, "and d2:", file2)
#                 print("J(d1,d2):", estimate_matrix[i][j])
#                 jaccard = len(shingles_set1.intersection(shingles_set2)) / len(shingles_set1.union(shingles_set2))
#                 print("Jaccard coefficient:", jaccard)
#                 print()

#         # Check if any element in the redundant set is already in any other set
#         if not any(redundant_set.intersection(s) for s in redundancy_sets):
#             redundancy_sets.add(frozenset(redundant_set))

#     print("\nRedundancy Sets:")
#     print("{" + ', '.join([str(s) for s in redundancy_sets]) + "}")

#     doc_jaccard = {}

#     def pop(jaccard_list):
#         for _ in range(min(n_neighbors, len(jaccard_list))):
#             estimated_jaccard_c, file_x = heappop(jaccard_list)
#             print(file_x, end=' ')

#     print(f"\n{n_neighbors} nearest neighbors for each file with threshold > {threshold}")
#     for i in range(num_files):
#         file1 = "file" + str(i).zfill(2)
#         estimated_jaccard_list = [(-estimate_matrix[i][j], "file" + str(j).zfill(2)) for j in range(num_files) if i != j and estimate_matrix[i][j] > threshold]
#         heapify(estimated_jaccard_list)
#         print("\n" + file1 + ":", end=' ')
#         pop(estimated_jaccard_list)

#     return redundancy_sets

import pickle
import os
from heapq import heapify, heappop, heappush
import random

def run_minhash(no_shingles, pickle_path, threshold=0.9, n_neighbors=3):
    pklHandler = open(pickle_path, 'rb')
    docShingleDict = pickle.load(pklHandler)
    pklHandler.close()

    def find_random_nos(k):
        return random.sample(range(no_shingles), k)

    folder1_path = "C:\\Users\\ekans\\OneDrive\\Desktop\\IISF_Bug_bunnies-main\\txt_out"
    files = os.listdir(folder1_path)
    num_files = len([f for f in files if os.path.isfile(os.path.join(folder1_path, f))])

    random_no_a = find_random_nos(3)
    random_no_b = find_random_nos(3)

    doc_lowest_shingle_id = {}
    for doc, shingle_id_set in docShingleDict.items():
        lowest_shingle_id = [min((random_no_a[i] * shingle_id + random_no_b[i]) % no_shingles for shingle_id in shingle_id_set) for i in range(3)]
        doc_lowest_shingle_id[doc] = lowest_shingle_id

    estimate_matrix = []
    for i in range(num_files):
        doc1 = "file" + str(i).zfill(2)
        doc1_lowest_shingles = doc_lowest_shingle_id.get(doc1, [])
        col = []
        for j in range(num_files):
            doc2 = "file" + str(j).zfill(2)
            doc2_lowest_shingles = doc_lowest_shingle_id.get(doc2, [])
            count = sum(1 for x, y in zip(doc1_lowest_shingles, doc2_lowest_shingles) if x == y)
            col.append(count / 3)
        estimate_matrix.append(col)

    print("\nList of Documents with J(d1,d2) more than", threshold)

    redundancy_sets = set()

    for i in range(num_files):
        file1 = "file" + str(i).zfill(2)
        redundant_set = set([file1])
        for j in range(num_files):
            if estimate_matrix[i][j] > threshold and i != j:
                file2 = "file" + str(j).zfill(2)
                redundant_set.add(file2)
                shingles_set1 = docShingleDict[file1]
                shingles_set2 = docShingleDict[file2]
                print("d1:", file1, "and d2:", file2)
                print("J(d1,d2):", estimate_matrix[i][j])
                jaccard = len(shingles_set1.intersection(shingles_set2)) / len(shingles_set1.union(shingles_set2))
                print("Jaccard coefficient:", jaccard)
                print()

        # Check if any element in the redundant set is already in any other set
        if not any(redundant_set.intersection(s) for s in redundancy_sets):
            redundancy_sets.add(frozenset(redundant_set))

    print("\nRedundancy Sets:")
    for idx, redundant_set in enumerate(redundancy_sets, 1):
        print(f"Redundancy Set {idx}: {redundant_set}")

    doc_jaccard = {}

    def pop(jaccard_list):
        for _ in range(min(n_neighbors, len(jaccard_list))):
            estimated_jaccard_c, file_x = heappop(jaccard_list)
            print(file_x, end=' ')

    print(f"\n{n_neighbors} nearest neighbors for each file with threshold > {threshold}")
    for i in range(num_files):
        file1 = "file" + str(i).zfill(2)
        estimated_jaccard_list = [(-estimate_matrix[i][j], "file" + str(j).zfill(2)) for j in range(num_files) if i != j and estimate_matrix[i][j] > threshold]
        heapify(estimated_jaccard_list)
        print("\n" + file1 + ":", end=' ')
        pop(estimated_jaccard_list)

    return redundancy_sets
