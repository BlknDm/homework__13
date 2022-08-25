from json import JSONDecodeError
from flask import render_template, Blueprint, request, logging
from project.functions import save_picture, func_add_post

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')


@loader_blueprint.route('/post')
def add_post_page():
    return render_template('post_form.html')


@loader_blueprint.route('/post', methods=['POST'])
def add_post():
    picture = request.files.get('picture')
    content = request.form.get('content')

    if not picture or not content:
        return 'Нет картинки и/или текста'

    if picture.filename.split('.')[-1] not in ['jpeg', 'png']:
        return 'Неверное расширение файла'

    try:
        picture_path: str = '/' + save_picture(picture)
    except FileNotFoundError:
        logging.info('Файл не найден')
        return 'Файл не найден'
    except JSONDecodeError:
        return 'Невалидный файл'

    post: dict = func_add_post({'pic': picture_path, 'content': content})
    return render_template('post_uploaded.html', post=post)
