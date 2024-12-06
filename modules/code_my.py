import io
import json
import os
import requests
import sys

from flask import Flask, render_template_string, request, Response, session
from PIL import Image

# Прокси-порт для доступа к приложению
base_url = sys.argv[3]

def load_html_from_file(filename):
  with open(filename, 'r', encoding='utf-8') as file:
      return file.read()

def run_app():
  app = Flask(__name__)
  app.secret_key = 'your_secret_key'  # Установите секретный ключ для сессий

  # Предопределенные учетные данные (в реальном приложении используйте базу данных)
  users = {
      "user1": "password1",
      "user2": "password2"
  }
  html_file = '/content/webApp_Auth/html/base_template.html'
  base_template = load_html_from_file(html_file)

  def get_favicon():
    # Создаем изображение 16x16 пикселей
    img = Image.new('RGB', (16, 16), color='blue')  # Пример: синяя иконка
    img_bytes = io.BytesIO()

    # Сохраняем изображение в формате ICO
    img.save(img_bytes, format='ICO')
    img_bytes.seek(0)  
    return Response(img_bytes.getvalue(), mimetype='image/x-icon')
#'''

  @app.route('/favicon.ico')
  def favicon():
      return get_favicon()

  @app.route('/')
  def index():
      title = "Главная страница"
      content = "<h2>Главная</h2><p>Информация о приложении.</p>"
      return render_template_string(base_template.format(title=title, content=content))

  @app.route('/auth', methods=['GET', 'POST'])
  def auth():
      error = None  # Переменная для хранения сообщения об ошибке
      if request.method == 'POST':
          username = request.form.get('username')
          password = request.form.get('password')
          
          # Проверка учетных данных
          if username in users and users[username] == password:
              session['username'] = username  # Сохраняем имя пользователя в сессии
              return welcome_page()  # Возвращаем страницу приветствия
          else:
              error = "Неверное имя или пароль."  # Устанавливаем сообщение об ошибке

      title = "Авторизация"
      content = get_auth_form(error)
      return render_template_string(base_template.format(title=title, content=content))

  def get_auth_form(error=None):
    # Путь к HTML-файлу
    html_file = '/content/webApp_Auth/html/auth_form.html'

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

  @app.route('/logout')
  def logout():
      session.pop('username', None)  # Удаляем пользователя из сессии
      return index()  # Возвращаем на главную страницу

  app.run()