from flask import Blueprint, render_template, request
from purchase.models import Purchase
router = Blueprint('purchase', __name__, template_folder='views')


@router.route('/', methods=['GET'])
def index():
    return render_template('purchase.html')


@router.route('/calculate', methods=['POST'])
def calculate_purchase():
    data = request.form

    purchase = Purchase(
        currency_origin=data['from'],
        currency_dest=data['to'],
        currency_origin_qty=float(data['from_qty'])
    )

    purchase.calculate()

    form_data = {
        'qty':  purchase.currency_dest_qty,
        'from': data['from'],
        'to': data['to'],
        'from_qty': data['from_qty'],
        'pu': purchase.get_price_unit()
    }

    return render_template('calculated.html', data=form_data)
