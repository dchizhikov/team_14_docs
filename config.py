import os

directory_path = os.getcwd()
folder_name = os.path.basename(directory_path)
parent_directory_path = os.path.dirname(directory_path)

repo_up = parent_directory_path
repo_name = folder_name
myRepo = repo_up + '/'+repo_name

#print('os.path.basename(directory_path)', folder_name)