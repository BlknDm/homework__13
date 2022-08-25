from json import JSONDecodeError

from flask import render_template, Blueprint, request
from project.functions import get_posts_by_world

main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')


@main_blueprint.route('/')
def main_page():
    return render_template('index.html')


@main_blueprint.route('/search/')
def search_page():
    search_query = request.args.get('s', '')
    try:
        posts = get_posts_by_world(search_query)
    except FileNotFoundError:
        return 'Файл не найден'
    except JSONDecodeError:
        return 'Невалидный файл'
    return render_template('post_list.html', posts=posts)
