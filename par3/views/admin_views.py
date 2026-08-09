from flask import Blueprint, render_template
from sqlalchemy import extract, func

from par3 import db
from par3.models import PageVisit, User
from par3.views.auth_views import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@admin_required
def dashboard():
    rows = (
        db.session.query(
            extract('hour', PageVisit.created_at).label('hour'),
            func.count(PageVisit.id),
        )
        .group_by('hour')
        .all()
    )

    hourly_counts = [0] * 24
    for hour, count in rows:
        if hour is not None:
            hourly_counts[int(hour)] = count

    return render_template('admin/dashboard.html', hourly_counts=hourly_counts)


@bp.route('/members')
@admin_required
def members():
    users = User.query.order_by(User.id.asc()).all()
    return render_template('admin/members.html', users=users)
