from flask import Blueprint, render_template
from transaction.models import Transactions

router = Blueprint("transaction", __name__, template_folder='views')

@router.route('/')
def index():
    transactions = Transactions()
    return render_template('index.html', transactions=transactions.get_all())