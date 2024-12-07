import sys
from flask import Flask, render_template_string, request, session
from modules.utils import get_auth_form, get_favicon, load_html_from_file, welcome_page 

# Прокси-порт для доступа к приложению
base_url = sys.argv[3]

def run_app():
  app = Flask(__name__)
  app.secret_key = 'your_secret_key'  # Установите секретный ключ для сессий

  # Предопределенные учетные данные (в реальном приложении используйте базу данных)
  users = {
      "user1": "password1",
      "user2": "password2"
  }
  html_file = '/work/webApp_Auth/html/base_template.html'
  base_template = load_html_from_file(html_file)

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

  @app.route('/logout')
  def logout():
      session.pop('username', None)  # Удаляем пользователя из сессии
      return index()  # Возвращаем на главную страницу

  app.run(host='0.0.0.0', port=8080)