from flask import Blueprint, render_template, request
from purchase.models import Purchase
router = Blueprint('purchase', __name__, template_folder='views')


@router.route('/', methods=['GET'])
def index():
    return render_template('purchase.html')


@router.route('/calculate', methods=['POST'])
def calculate_purchase():
    purchase = Purchase()
    data = request.form
    returned_qty = purchase.calculate(
        currency_origin=data['from'],
        currency_dest=data['to'],
        currency_origin_qty=float(data['from_qty'])
    )
    return render_template('calculated.html', qty=returned_qty)
