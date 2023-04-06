from flask import Flask
from transaction.controllers import router as transaction_route
from purchase.controllers import router as purchase_router

app = Flask(__name__)

app.register_blueprint(transaction_route, url_prefix="/transactions")
app.register_blueprint(purchase_router, url_prefix="/purchase")