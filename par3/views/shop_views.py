import json
from flask import Blueprint, request, redirect, url_for, render_template, g
from par3.views.auth_views import login_required, admin_required
from par3.models import ShopProduct, ProductReview, CartItem
from par3 import db, storage

bp = Blueprint('shop', __name__, url_prefix='/shop')


def resolve_shop_image(value):
    # Supabase Storage에 올린 상품 이미지는 절대 URL, 시드 데이터로 들어간 기존 이미지는
    # static/img/shop_imgs/ 안의 파일명이므로 둘을 구분해서 처리한다.
    if not value:
        return ''
    if value.startswith('http://') or value.startswith('https://'):
        return value
    return url_for('static', filename=f'img/shop_imgs/{value}')


def product_to_dict(product):
    return {
        'id': product.id,
        'brand': product.brand,
        'title': product.title,
        'rating': product.rating,
        'reviewCount': product.review_count,
        'price': product.price,
        'mainImg': resolve_shop_image(product.main_img),
        'detailImg': resolve_shop_image(product.detail_img),
        'features': product.features or [],
        'reviews': [
            {
                'content': r.content,
                'rating': r.rating if r.rating is not None else product.rating,
            }
            for r in product.reviews
        ],
        'shipping': product.shipping,
        'origin': product.origin,
    }


def cart_items_to_list(user):
    items = CartItem.query.filter_by(user_id=user.id).order_by(CartItem.id.asc()).all()
    result = []
    for ci in items:
        item = product_to_dict(ci.product)
        item['quantity'] = ci.quantity
        item['cartItemId'] = ci.id
        result.append(item)
    return result


@bp.route('/')
def main():
    products = ShopProduct.query.all()
    return render_template('shop/shop.html', products=[product_to_dict(p) for p in products])


@bp.route('/<int:id>')
def detail(id):
    product = ShopProduct.query.get_or_404(id)
    return render_template('shop/shop_detail.html', product=product_to_dict(product))


@bp.route('/cart')
@login_required
def cart():
    return render_template('shop/shop_cart.html', cart_items=cart_items_to_list(g.user))


@bp.route('/buy')
def buy():
    id = request.args.get('id', type=int)
    qty = request.args.get('qty', type=int) or 1

    if id:
        product = ShopProduct.query.get_or_404(id)
        order_items = [{**product_to_dict(product), 'quantity': max(1, qty)}]
    else:
        if g.user is None:
            return redirect(url_for('auth.login', next=request.path))
        order_items = cart_items_to_list(g.user)
        if not order_items:
            return redirect(url_for('shop.cart'))

    shipping_info = None
    if g.user is not None:
        shipping_info = {
            'name': g.user.username,
            'phone': g.user.phonenumber,
            'address': g.user.home_address or '',
        }

    return render_template('shop/shop_buy.html', order_items=order_items, shipping_info=shipping_info)


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
        main_img = storage.upload_image(file, 'shop')
    else:
        main_img = 'no_image.png'

    new_product = ShopProduct(
        brand=brand,
        title=title,
        price=int(price),
        main_img=main_img,
    )
    db.session.add(new_product)
    db.session.commit()

    return redirect(url_for('shop.main'))


@bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    if g.user is None:
        return {'success': False, 'error': 'login_required'}, 401

    data = request.get_json(silent=True) or {}
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    product = ShopProduct.query.get(product_id)
    if not product:
        return {'success': False, 'error': 'not_found'}, 404

    try:
        quantity = max(1, int(quantity))
    except (TypeError, ValueError):
        quantity = 1

    existing = CartItem.query.filter_by(user_id=g.user.id, product_id=product.id).first()
    if existing:
        existing.quantity += quantity
    else:
        db.session.add(CartItem(user_id=g.user.id, product_id=product.id, quantity=quantity))
    db.session.commit()

    return {'success': True}


@bp.route('/cart/update', methods=['POST'])
def update_cart_item():
    if g.user is None:
        return {'success': False, 'error': 'login_required'}, 401

    data = request.get_json(silent=True) or {}
    item = CartItem.query.filter_by(id=data.get('cart_item_id'), user_id=g.user.id).first()
    if not item:
        return {'success': False, 'error': 'not_found'}, 404

    try:
        quantity = int(data.get('quantity'))
    except (TypeError, ValueError):
        return {'success': False, 'error': 'invalid_quantity'}, 400

    if quantity < 1:
        db.session.delete(item)
    else:
        item.quantity = quantity
    db.session.commit()

    return {'success': True}


@bp.route('/cart/remove', methods=['POST'])
def remove_cart_item():
    if g.user is None:
        return {'success': False, 'error': 'login_required'}, 401

    data = request.get_json(silent=True) or {}
    item = CartItem.query.filter_by(id=data.get('cart_item_id'), user_id=g.user.id).first()
    if item:
        db.session.delete(item)
        db.session.commit()

    return {'success': True}
