import importlib
import os
import sys

directory_path = os.getcwd()
repo_name = os.path.basename(directory_path)
repo_up = os.path.dirname(directory_path)
folder_modules = '/modules/'
folder_modules_path = repo_up+'/'+repo_name+folder_modules

sys.path.append(repo_up+'/'+repo_name)
sys.path.append(folder_modules_path)

print("Начало")
modules_list = [os.path.splitext(file)[0] for file in os.listdir(folder_modules_path) if file.endswith('.py')]
imported_modules = {}

# Импортируем и перезагружаем модули
for module in modules_list:
    # Динамический импорт модуля
    imported_module = importlib.import_module(module)
#    importlib.reload(imported_module)
    imported_modules[module] = imported_module
print(imported_modules)

gc = imported_modules['git_com']
test = imported_modules['test_my']
code = imported_modules['code_my']
test.test()

base_url=code.base_url #run_app()
print(base_url)
code.run_app()

#'''
print("Конец")