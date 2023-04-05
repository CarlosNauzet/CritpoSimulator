from flask import Blueprint, render_template, request
from purchase.models import Purchase
router = Blueprint('purchase', __name__, template_folder='views')


@router.route('/', methods=['GET'])
def index():
    return render_template('form.html')


@router.route('/', methods=['POST'])
def create_purchase():
    purchase = Purchase()
    data = request.form
    returned_qty = purchase.calculate(
        currency_origin=data['from'],
        currency_dest=data['to'],
        currency_origin_qty=float(data['from_qty'])
    )
    return f"You will buy {returned_qty} {data['to']}"
