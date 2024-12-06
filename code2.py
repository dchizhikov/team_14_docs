from google.colab.output import eval_js
from PIL import Image

import io
import json
import os
import requests

from flask import Flask, request, render_template_string, session

# Прокси-порт для доступа к приложению
base_url = eval_js("google.colab.kernel.proxyPort(5000)")
print(base_url)

def get_favicon():
    # Создаем изображение 16x16 пикселей
    img = Image.new('RGB', (16, 16), color='blue')  # Пример: синяя иконка
    img_bytes = io.BytesIO()

    # Сохраняем изображение в формате ICO
    img.save(img_bytes, format='ICO')
    img_bytes.seek(0)  # Возвращаемся в начало объекта BytesIO


def run_app():
  app = Flask(__name__)
  app.secret_key = 'your_secret_key'  # Установите секретный ключ для сессий

  # Предопределенные учетные данные (в реальном приложении используйте базу данных)
  users = {
      "user1": "password1",
      "user2": "password2"
  }

  # Определяем базовый шаблон
  base_template = '''
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>{title}</title>
  </head>
  <body>
      <header>
          <h1>Добро пожаловать в мое приложение!</h1>
          <nav>
              <a href="/">Главная</a>
              <a href="/auth">Вход</a>
              <a href="/logout">Выход</a>
          </nav>
      </header>
      <main>
          {content}
      </main>
  </body>
  </html>
  '''

  @app.route('/favicon.ico')
  def favicon():
      return get_favicon()

  @app.route('/')
  def index():
      title = "Главная страница"
      content = "<h2>Это главная страница!</h2><p>Здесь можно разместить информацию о вашем приложении.</p>"
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
      error_html = f"<p style='color: red;'>{error}</p>" if error else ""
      form_html = f'''
          <form method="POST" action="/auth">
              {error_html}
              <label for="username">Имя:</label><br>
              <input type="text" id="username" name="username" required><br>
              <label for="password">Пароль:</label><br>
              <input type="password" id="password" name="password" required><br>
              <input type="submit" value="Вход"><br>
          </form>
      '''
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