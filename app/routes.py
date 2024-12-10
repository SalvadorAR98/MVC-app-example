from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app import db
from app.models import Product, Category
import os
from werkzeug.utils import secure_filename
import datetime

bp = Blueprint('routes', __name__)

# Función para verificar archivos permitidos
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# CRUD para Productos
@bp.route('/product/new', methods=['GET', 'POST'])
@bp.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
def manage_product(product_id=None):
    # Obtener el producto si existe, o inicializarlo como None
    product = Product.query.get(product_id) if product_id else None

    # Obtener las categorías para el formulario
    categories = Category.query.all()

    if request.method == 'POST':
        # Procesar los datos enviados desde el formulario
        name = request.form.get('name')  # Obtener el nombre del producto
        stock = int(request.form.get('stock', 0))  # Obtener el stock, por defecto 0
        price = float(request.form.get('price', 0))  # Obtener el precio, por defecto 0.0
        category_id = int(request.form.get('category_id', 0))  # Obtener la categoría, por defecto 0

        # Crear o actualizar el producto
        if product:
            product.name = name
            product.stock = stock
            product.price = price
            product.category_id = category_id
        else:
            new_product = Product(
                name=name,
                stock=stock,
                price=price,
                category_id=category_id,
            )
            db.session.add(new_product)

        # Guardar los cambios en la base de datos
        db.session.commit()
        flash('Producto guardado exitosamente.')
        return redirect(url_for('routes.index'))

    # Renderizar el formulario para GET
    return render_template('product_form.html', product=product, categories=categories)



@bp.route('/product/<int:product_id>/delete')
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Producto eliminado exitosamente.')
    return redirect(url_for('routes.index'))

# CRUD para Categorías
@bp.route('/category/new', methods=['GET', 'POST'])
def new_category():
    categories = Category.query.all()
    if request.method == 'POST':
        name = request.form['name']
        # Verificar si la categoría ya existe
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            return render_template(
                'category_form.html',
                categories=categories,
                error_message=f'La categoría "{name}" ya existe.'
            )
        # Si no existe, agregarla
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('routes.new_category'))
    return render_template('category_form.html', categories=categories)

@bp.route('/category/delete/<int:category_id>', methods=['GET'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Categoría eliminada exitosamente.')
    return redirect(url_for('routes.new_category'))



