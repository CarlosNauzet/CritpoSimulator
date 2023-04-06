from flask import Blueprint, render_template, request
from purchase.models import Purchase
router = Blueprint('purchase', __name__, template_folder='views')


@router.route('/', methods=['GET'])
def index():
    return render_template('purchase.html')


@router.route('/calculate', methods=['POST'])
def calculate_purchase():
    data = request.form

    purchase = Purchase()
    returned_qty = purchase.calculate(
        currency_origin=data['from'],
        currency_dest=data['to'],
        currency_origin_qty=float(data['from_qty'])
    )

    form_data = {
        'qty':returned_qty,
        'from': data['from'],
        'to' : data['to'],
        'from_qty' : data['from_qty'],
        'pu': purchase.exchange_rate
    }
    return render_template('calculated.html', data=form_data)
