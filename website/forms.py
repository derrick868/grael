from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, length, NumberRange,Optional
from flask_wtf.file import FileField, FileRequired


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), length(min=2)])
    password1 = PasswordField('Enter Your Password', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Confirm Your Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Enter Your Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Change Password')


class ShopItemsForm(FlaskForm):
    product_name = StringField('Name of Product', validators=[DataRequired()])
    current_price = FloatField('Current Price', validators=[DataRequired()])
    previous_price = FloatField('Previous Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('Product Picture', validators=[Optional()])  # ✅ Optional for updates
    flash_sale = BooleanField('Flash Sale')
    category = SelectField('Category', coerce=int, validators=[DataRequired()])

    add_product = SubmitField('Add Product')
    update_product = SubmitField('Update')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), length(min=2, max=100)])
    submit = SubmitField('Add Category')
    update_category = SubmitField('Update')

class OrderForm(FlaskForm):
    order_status = SelectField('Order Status', 
                               choices=[('Pending', 'Pending'), 
                                        ('Accepted', 'Accepted'),
                                        ('Out for delivery', 'Out for delivery'),
                                        ('Delivered', 'Delivered'), 
                                        ('Canceled', 'Canceled')],
                               validators=[DataRequired()])
    
    submit = SubmitField('Place Order')
    # Only the update button is necessary here





