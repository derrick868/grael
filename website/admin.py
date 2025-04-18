from flask import Blueprint, render_template, flash, send_from_directory, redirect,request,jsonify,url_for
from flask_login import login_required, current_user
from .forms import ShopItemsForm, OrderForm
from werkzeug.utils import secure_filename
from .models import Product, Order, Customer
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)


@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.status == 'admin':
        form = ShopItemsForm()

        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data

            file_name = secure_filename(file.filename)

            file_path = f'./media/{file_name}'

            file.save(file_path)

            new_shop_item = Product()
            new_shop_item.product_name = product_name
            new_shop_item.current_price = current_price
            new_shop_item.previous_price = previous_price
            new_shop_item.in_stock = in_stock
            new_shop_item.flash_sale = flash_sale

            new_shop_item.product_picture = file_path

            try:
                db.session.add(new_shop_item)
                db.session.commit()
                flash(f'{product_name} added Successfully')
                print('Product Added')
                return render_template('add-shop-items.html', form=form)
            except Exception as e:
                print(e)
                flash('Product Not Added!!')

        return render_template('add-shop-items.html', form=form)

    return render_template('404.html')

@admin.route('/shop-items', methods=['GET', 'POST'])
@login_required
def shop_items():
    if current_user.status == 'admin':
        items = Product.query.order_by(Product.date_added).all()
        return render_template('shop_items.html', items=items)
    return render_template('404.html')


@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.status == 'admin':
        form = ShopItemsForm()

        item_to_update = Product.query.get(item_id)

        form.product_name.render_kw = {'placeholder': item_to_update.product_name}
        form.previous_price.render_kw = {'placeholder': item_to_update.previous_price}
        form.current_price.render_kw = {'placeholder': item_to_update.current_price}
        form.in_stock.render_kw = {'placeholder': item_to_update.in_stock}
        form.flash_sale.render_kw = {'placeholder': item_to_update.flash_sale}

        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data

            file = form.product_picture.data

            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'

            file.save(file_path)

            try:
                Product.query.filter_by(id=item_id).update(dict(product_name=product_name,
                                                                current_price=current_price,
                                                                previous_price=previous_price,
                                                                in_stock=in_stock,
                                                                flash_sale=flash_sale,
                                                                product_picture=file_path))

                db.session.commit()
                flash(f'{product_name} updated Successfully')
                print('Product Upadted')
                return redirect('/shop-items')
            except Exception as e:
                print('Product not Upated', e)
                flash('Item Not Updated!!!')

        return render_template('update_item.html', form=form)
    return render_template('404.html')

@admin.route('/delete-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    if current_user.status == 'admin':
        try:
            item_to_delete = Product.query.get(item_id)
            db.session.delete(item_to_delete)
            db.session.commit()
            flash('One Item deleted')
            return redirect('/shop-items')
        except Exception as e:
            print('Item not deleted', e)
            flash('Item not deleted!!')
        return redirect('/shop-items')

    return render_template('404.html')

@admin.route('/admin-page')
@login_required
def admin_page():
    if current_user.status == 'admin':
        return render_template('admin.html')
    return render_template('404.html')


@admin.route('/view-orders')
@login_required
def order_view():
    if current_user.status == 'admin':
        orders = Order.query.all()
        return render_template('view_orders.html', orders=orders)
    return render_template('404.html')


@admin.route('/update-order/<int:order_id>', methods=['GET', 'POST'])
@login_required
def update_order(order_id):
    if current_user.status == 'admin':
        form = OrderForm()

        order = Order.query.get(order_id)

        if order is None:  # Check if the order exists
            flash('Order not found', 'error')
            return redirect('/view-orders')

        if form.validate_on_submit():
            status = form.order_status.data
            order.status = status

            try:
                db.session.commit()
                flash(f'Order {order_id} Updated successfully', 'success')
                return redirect('/view-orders')
            except Exception as e:
                db.session.rollback()  # Rollback if there’s an error
                flash(f'Error updating order {order_id}: {e}', 'error')
                return redirect('/view-orders')

        # If it's a GET request, or the form is not valid, render the form again
        return render_template('order_update.html', form=form, order=order)

    return render_template('404.html')


@admin.route('/customers')
@login_required
def display_customers():
    if current_user.status == 'admin':
        customers = Customer.query.all()
        return render_template('customers.html', customers=customers)
    return render_template('404.html')
    
@admin.route('/update-role/<int:id>', methods=['POST'])
@login_required
def update_role(id):
    if current_user.status != 'admin':  # Ensure only admins can update roles
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403

    customer = Customer.query.get_or_404(id)
    data = request.get_json()

    if 'status' in data:
        new_status = data['status']  # 'admin' or 'user'

        if new_status not in ['admin', 'user']:  # Ensure only valid roles are accepted
            return jsonify({'success': False, 'error': 'Invalid role'}), 400

        try:
            customer.status = new_status  # Update the role using status
            db.session.commit()
            return jsonify({'success': True, 'message': 'Role updated successfully'})
        except Exception as e:
            db.session.rollback()  # Rollback changes if something goes wrong
            return jsonify({'success': False, 'error': str(e)}), 500

    return jsonify({'success': False, 'error': 'Invalid data'}), 400



@admin.route('/delete-customer/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def delete_customer(customer_id):
    if current_user.status == 'admin':
        try:
            customer_to_delete = Customer.query.get(customer_id)

            # ✅ Prevent deleting yourself
            if customer_to_delete.id == current_user.id:
                flash("You can't delete yourself!", 'warning')
                return redirect(url_for('customers'))

            db.session.delete(customer_to_delete)
            db.session.commit()
            flash('Client deleted successfully!', 'success')
        except Exception as e:
            print('Client not deleted:', e)
            flash('Client could not be deleted!', 'danger')
        
        return redirect('/customers')

    return render_template('404.html')
