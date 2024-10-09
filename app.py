from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import StockInForm, StockOutForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Add Flask-Migrate here

# Models
class StockIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    batch_number = db.Column(db.String(50), nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    received_date = db.Column(db.Date, default=datetime.utcnow)

class StockOut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    issued_date = db.Column(db.Date, default=datetime.utcnow)

# Routes
@app.route('/')
def dashboard():
    stocks_in = StockIn.query.all()
    stocks_out = StockOut.query.all()
    return render_template('dashboard.html', stocks_in=stocks_in, stocks_out=stocks_out)

@app.route('/stock-in', methods=['GET', 'POST'])
def stock_in():
    form = StockInForm()
    if form.validate_on_submit():
        stock = StockIn(
            source=form.source.data,
            item_name=form.item_name.data,
            batch_number=form.batch_number.data,
            expiry_date=form.expiry_date.data,
            quantity=form.quantity.data,
            received_date=form.received_date.data
        )
        db.session.add(stock)
        db.session.commit()
        flash('Stock has been added!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('stock_in.html', form=form)

@app.route('/stock-out', methods=['GET', 'POST'])
def stock_out():
    form = StockOutForm()
    if form.validate_on_submit():
        stock_out = StockOut(
            department=form.department.data,
            item_name=form.item_name.data,
            quantity=form.quantity.data,
            issued_date=form.issued_date.data
        )
        db.session.add(stock_out)
        db.session.commit()
        flash('Stock has been issued!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('stock_out.html', form=form)

@app.route('/reports')
def reports():
    stocks_in = StockIn.query.all()
    stocks_out = StockOut.query.all()
    return render_template('reports.html', stocks_in=stocks_in, stocks_out=stocks_out)

if __name__ == '__main__':
    app.run(debug=True)
