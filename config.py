import os

directory_path = os.getcwd()
repo_name = os.path.basename(directory_path)
repo_up = os.path.dirname(directory_path)

myRepo = repo_up + '/'+repo_name

print('myRepo', myRepo)