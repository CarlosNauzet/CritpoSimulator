from flask import Blueprint, render_template, request

router = Blueprint('purchase', __name__, template_folder='views')


@router.route('/', methods=['GET'])
def index():
    return render_template('form.html')


@router.route('/', methods=['POST'])
def create_purchase():
    print(request.form['to'])
    return
