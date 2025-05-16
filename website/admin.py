from flask import Blueprint, render_template, flash, send_from_directory, redirect,request,jsonify,url_for
from flask_login import login_required, current_user
from .forms import ShopItemsForm, OrderForm, CategoryForm
from werkzeug.utils import secure_filename
from .models import Product, Order, Customer,Category
from . import db

admin = Blueprint('admin', __name__)

@admin.route('/media/<path:filename>')
def get_image(filename):
    return send_from_directory('../media', filename)
@admin.route('/add-category', methods=['GET', 'POST'])
@login_required
def add_category():
    if current_user.status != 'admin':
        return render_template('404.html')

    form = CategoryForm()
    if form.validate_on_submit():
        category_name = form.name.data.strip()

        # Check if category already exists
        existing = Category.query.filter_by(name=category_name).first()
        if existing:
            flash('Category already exists!', 'warning')
        else:
            new_category = Category(name=category_name)
            db.session.add(new_category)
            db.session.commit()
            flash(f'Category "{category_name}" added successfully!', 'success')
            return redirect(url_for('admin.add_category'))

    return render_template('add-category.html', form=form)

@admin.route('/category-items', methods=['GET', 'POST'])
@login_required
def category_items():
    if current_user.status == 'admin':
        items = Category.query.all()

        return render_template('category_items.html', items=items)
    return render_template('404.html')

@admin.route('/update-category/<int:item_id>', methods=['GET', 'POST'])
@login_required
def category_item(item_id):
    if current_user.status == 'admin':
        form = CategoryForm()

        category_to_update = Category.query.get(item_id)

        form.name.render_kw = {'placeholder': category_to_update.name}
        

        if form.validate_on_submit():
            category_name = form.name.data


            try:
                Category.query.filter_by(id=item_id).update(dict(name=category_name))

                db.session.commit()
                flash(f'{category_name} updated Successfully')
                print('Category Updated')
                return redirect('/category-items')
            except Exception as e:
                print('Category not Upated', e)
                flash('Category Not Updated!!!')

        return render_template('update_category.html', form=form)
    return render_template('404.html')


@admin.route('/delete-category/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_category(item_id):
    if current_user.status == 'admin':
        try:
            category_to_delete = Category.query.get(item_id)
            db.session.delete(category_to_delete)
            db.session.commit()
            flash('One Category deleted')
            return redirect('/category-items')
        except Exception as e:
            print('Category not deleted', e)
            flash('Category not deleted!!')
        return redirect('/category-items')

    return render_template('404.html')

@admin.route('/add-shop-items', methods=['GET', 'POST'])
@login_required
def add_shop_items():
    if current_user.status == 'admin':
        form = ShopItemsForm()
        form.category.choices = [(c.id, c.name) for c in Category.query.all()]  # ✅ set choices

        if form.validate_on_submit():
            product_name = form.product_name.data
            current_price = form.current_price.data
            previous_price = form.previous_price.data
            in_stock = form.in_stock.data
            flash_sale = form.flash_sale.data
            category_id = form.category.data  # ✅ get selected category

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
            new_shop_item.category_id = category_id  # ✅ set category
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
        category_name= Category.query.all()
        return render_template('shop_items.html', items=items,name=category_name)
    return render_template('404.html')


@admin.route('/update-item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    if current_user.status != 'admin':
        return render_template('404.html')

    form = ShopItemsForm()
    item_to_update = Product.query.get_or_404(item_id)

    # Populate category dropdown
    form.category.choices = [(cat.id, cat.name) for cat in Category.query.order_by(Category.name).all()]

    # Prefill data for user convenience (only on GET)
    if request.method == 'GET':
        form.product_name.data = item_to_update.product_name
        form.previous_price.data = item_to_update.previous_price
        form.current_price.data = item_to_update.current_price
        form.in_stock.data = item_to_update.in_stock
        form.flash_sale.data = item_to_update.flash_sale
        form.category.data = item_to_update.category_id

    if form.validate_on_submit():
        # Use new values or fallback to existing (for file only)
        product_name = form.product_name.data
        current_price = form.current_price.data
        previous_price = form.previous_price.data
        in_stock = form.in_stock.data
        flash_sale = form.flash_sale.data
        category_id = form.category.data

        file = form.product_picture.data
        if file and file.filename:
            file_name = secure_filename(file.filename)
            file_path = f'./media/{file_name}'
            file.save(file_path)
        else:
            file_path = item_to_update.product_picture

        try:
            Product.query.filter_by(id=item_id).update(dict(
                product_name=product_name,
                current_price=current_price,
                previous_price=previous_price,
                in_stock=in_stock,
                flash_sale=flash_sale,
                product_picture=file_path,
                category_id=category_id
            ))
            db.session.commit()
            flash(f'{product_name} updated successfully')
            return redirect('/shop-items')
        except Exception as e:
            print('Product not updated:', e)
            flash('Item not updated!')

    return render_template('update_item.html', form=form)

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
@admin.route('/category/<int:category_id>')
def category_products(category_id):
    category = Category.query.get_or_404(category_id)
    products = Product.query.filter_by(category_id=category_id).all()
    return render_template('category_products.html', category=category, products=products)

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
