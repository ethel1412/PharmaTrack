from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired

class StockInForm(FlaskForm):
    source = StringField('Source', validators=[DataRequired()])
    item_name = StringField('Item Name', validators=[DataRequired()])
    batch_number = StringField('Batch Number', validators=[DataRequired()])
    expiry_date = DateField('Expiry Date', format='%Y-%m-%d', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    received_date = DateField('Received Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Stock')

class StockOutForm(FlaskForm):
    department = StringField('Department', validators=[DataRequired()])
    item_name = StringField('Item Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    issued_date = DateField('Issued Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Issue Stock')
