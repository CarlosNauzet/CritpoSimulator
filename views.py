from flask import Blueprint, render_template, request
from models import Purchase, CalculatePurchase, Transactions

router = Blueprint('views', __name__)


@router.route('/purchase', methods=['GET'])
def purchase():
    return render_template('purchase/index.html')


@router.route('/purchase/calculate', methods=['POST'])
def calculate_purchase():
    data = request.form

    purchase_calculator = CalculatePurchase(
        currency_origin=data['from'],
        currency_dest=data['to'],
        currency_origin_qty=float(data['from_qty'])
    )

    purchase_calculator.calculate()

    form_data = {
        'qty':  purchase_calculator.currency_dest_qty,
        'from': data['from'],
        'to': data['to'],
        'from_qty': data['from_qty'],
        'pu': purchase_calculator.get_price_unit()
    }

    return render_template('purchase/calculated.html', data=form_data)


@router.route('/purchase', methods=['POST'])
def do_purchase():
    data = request.form
    purchase = Purchase(
        currency_origin=data['from'],
        currency_dest=data['to'],
        currency_origin_qty=float(data['from_qty']),
        currency_dest_qty=float(data['to_qty']),
        price_unit=float(data['pu'])
    )
    purchase.save()

    return "Compra realizada"


@router.route('/', methods=['GET'])
def index():
    transactions = Transactions()
    return render_template('transactions/index.html', transactions=transactions.get_all())
