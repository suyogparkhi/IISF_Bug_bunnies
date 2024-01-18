import conversion
input_folder1 = "C:\\Users\\ekans\\OneDrive\\Documents\\SIF 2023\\dataset\\Folder-1"
input_folder2 = "C:\\Users\\ekans\\OneDrive\\Documents\\SIF 2023\\dataset\\Folder-2"
output_folder_txt = "C:\\Users\\ekans\\OneDrive\\Desktop\\IISF_Bug_bunnies-main\\txt_out"
output_folder_jpg = "C:\\Users\\ekans\\OneDrive\\Desktop\\IISF_Bug_bunnies-main\\img_out"

mapping_folder1, file_counter1 = conversion.process_folder(input_folder1, output_folder_txt, output_folder_jpg, folder_number=1)
mapping_folder2, file_counter2 = conversion.process_folder(input_folder2, output_folder_txt, output_folder_jpg, folder_number=2, file_counter_start=file_counter1)
