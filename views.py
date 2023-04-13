from flask import Blueprint, render_template, request, redirect
from models import Purchase, CalculatePurchase, Transactions, Status

router = Blueprint('views', __name__)


@router.route('/purchase', methods=['GET'])
def purchase():
    return render_template('purchase/index.html', data={})


@router.route('/purchase/calculate', methods=['POST'])
def calculate_purchase():
    data = request.form

    purchase_calculator = CalculatePurchase(
        currency_origin=data['from'],
        currency_dest=data['to'],
        currency_origin_qty=float(data['from_qty'])
    )
    transactions = Transactions()

    balance = transactions.get_currency_balance(data['from'])
    if data['from'] != 'EUR' and balance < float(data['from_qty']):
        form_data = {
            'from': data['from'],
            'to': data['to'],
            'from_qty': data['from_qty'],
            'error': f"You don't have enough quantity of {data['from']}. Available {balance}"
        }
        return render_template('purchase/index.html', data=form_data)

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

    return redirect(f"/?fromPurchase=true", code=302)


@router.route('/', methods=['GET'])
def index():
    transactions = Transactions()
    return render_template('transactions/index.html', transactions=transactions.get_all())


@router.route('/status', methods=['GET'])
def status():
    status = Status()
    transactions = Transactions()

    balance_by_currency = status.get_balance_by_currency()
    total_euro_investment_amount = status.get_current_euro_invesment_amount(
        balance_by_currency
    )
    initial_euro_investment = transactions.get_initial_euros_investment()

    return render_template(
        'status/index.html',
        data=balance_by_currency,
        total_euro_investment=total_euro_investment_amount,
        initial_euro_investment=initial_euro_investment
    )
