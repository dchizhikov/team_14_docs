import io
from flask import Response, session
from PIL import Image

def load_html_from_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def get_favicon():
    # Создаем изображение 16x16 пикселей
    img = Image.new('RGB', (16, 16), color='blue')  # Пример: синяя иконка
    img_bytes = io.BytesIO()

    # Сохраняем изображение в формате ICO
    img.save(img_bytes, format='ICO')
    img_bytes.seek(0)  
    return Response(img_bytes.getvalue(), mimetype='image/x-icon')

def get_auth_form(error=None):
  # Путь к HTML-файлу
  html_file = '/work/webApp_Auth/html/auth_form.html'

  # Загрузка HTML-кода из файла
  form_html = load_html_from_file(html_file)

  # Заменяем плейсхолдер на сообщение об ошибке
  error_html = f"<p style='color: red;'>{error}</p>" if error else "<p> </p>"
  form_html = form_html.replace("{error_html}", error_html)

  return form_html

def welcome_page():
    if 'username' in session:
        return f"<h1>Добро пожаловать, {session['username']}!</h1><a href='/logout'>Выйти</a>"
    else:
        return "Ошибка: вы не авторизованы.", 403

