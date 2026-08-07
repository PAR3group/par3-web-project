import os
import uuid
import json
from werkzeug.utils import secure_filename
from flask import Blueprint, request, redirect, url_for, render_template
from par3.views.auth_views import login_required, admin_required
from par3.models import ShopProduct, ProductReview
from par3 import db

bp = Blueprint('shop', __name__, url_prefix='/shop')


def product_to_dict(product):
    return {
        'id': product.id,
        'brand': product.brand,
        'title': product.title,
        'rating': product.rating,
        'reviewCount': product.review_count,
        'price': product.price,
        'mainImg': url_for('static', filename=f'img/shop_imgs/{product.main_img}'),
        'detailImg': url_for('static', filename=f'img/shop_imgs/{product.detail_img}') if product.detail_img else '',
        'features': product.features or [],
        'reviews': [r.content for r in product.reviews],
        'shipping': product.shipping,
        'origin': product.origin,
    }


@bp.route('/')
def main():
    products = ShopProduct.query.all()
    return render_template('shop/shop.html', products=[product_to_dict(p) for p in products])


@bp.route('/<int:id>')
def detail(id):
    product = ShopProduct.query.get_or_404(id)
    return render_template('shop/shop_detail.html', product=product_to_dict(product))


@bp.route('/cart')
def cart():
    id = request.args.get('id', type=int)
    product = ShopProduct.query.get_or_404(id) if id else None
    return render_template('shop/shop_cart.html', product=product_to_dict(product) if product else None)


@bp.route('/buy')
def buy():
    id = request.args.get('id', type=int)
    product = ShopProduct.query.get_or_404(id) if id else None
    return render_template('shop/shop_buy.html', product=product_to_dict(product) if product else None)


@bp.route('/add', methods=['GET'])
@admin_required
def add_product_form():
    return render_template('shop/shop_add.html')


@bp.route('/add', methods=['POST'])
@admin_required
def add_product():
    brand = request.form.get('brand')
    title = request.form.get('title')
    price = request.form.get('price')

    file = request.files.get('main_img')

    if file and file.filename:
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1] if '.' in filename else 'png'
        filename = f"{uuid.uuid4().hex}.{ext}"
        save_path = os.path.join('static', 'img', 'shop_imgs', filename)
        file.save(save_path)
    else:
        filename = 'no_image.png'

    new_product = ShopProduct(
        brand=brand,
        title=title,
        price=int(price),
        main_img=filename,
    )
    db.session.add(new_product)
    db.session.commit()

    return redirect(url_for('shop.main'))


@bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    return {'success': True, 'product_id': product_id, 'quantity': quantity}