import io
import json
import os
import requests
import sys

from flask import Flask, request, render_template_string, session
from PIL import Image

# Прокси-порт для доступа к приложению
base_url = sys.argv[3]

def get_favicon():
    # Создаем изображение 16x16 пикселей
    img = Image.new('RGB', (16, 16), color='blue')  # Пример: синяя иконка
    img_bytes = io.BytesIO()

    # Сохраняем изображение в формате ICO
    img.save(img_bytes, format='ICO')
    img_bytes.seek(0)  # Возвращаемся в начало объекта BytesIO
#'''
