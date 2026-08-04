from flask import g, render_template, flash, Blueprint
from par3.views.auth_views import login_required
from par3.forms import RecommendForm
from par3.models import ShaftRecommend
from par3 import db
from par3.utils import *

bp=Blueprint('recommend', __name__, url_prefix='/recommend')

@bp.route("/shaft/", methods=["GET", "POST"])
@login_required
def shaft():

    form = RecommendForm()

    if form.validate_on_submit():

        # 아무것도 선택 안 함
        if not any([
            form.driver_selected.data,
            form.wood5_selected.data,
            form.utility4_selected.data,
            form.iron7_selected.data
        ]):
            flash("추천받을 클럽을 하나 이상 선택해주세요.")
            return render_template("recommend.html", form=form)

        result = {}

        # 드라이버
        if form.driver_selected.data:

            if not form.driver_distance.data:
                flash("드라이버 목표 비거리를 입력해주세요.")
                return render_template("recommend.html", form=form)

            distance = convert_distance(
                form.driver_distance.data,
                form.distance_unit.data
            )

            result["driver"] = recommend_shaft_weight(
                form.gender.data,
                form.user_height.data,
                form.user_weight.data,
                distance,
                SHAFT_MULTIPLIER["driver"]
            )

        # 우드
        if form.wood5_selected.data:

            if not form.wood5_distance.data:
                flash("5번 우드 목표 비거리를 입력해주세요.")
                return render_template("recommend.html", form=form)

            distance = convert_distance(
                form.wood5_distance.data,
                form.distance_unit.data
            )

            result["wood5"] = recommend_shaft_weight(
                form.gender.data,
                form.user_height.data,
                form.user_weight.data,
                distance,
                SHAFT_MULTIPLIER["wood5"]
            )

        # 유틸
        if form.utility4_selected.data:

            if not form.utility4_distance.data:
                flash("4번 유틸 목표 비거리를 입력해주세요.")
                return render_template("recommend.html", form=form)

            distance = convert_distance(
                form.utility4_distance.data,
                form.distance_unit.data
            )

            result["utility4"] = recommend_shaft_weight(
                form.gender.data,
                form.user_height.data,
                form.user_weight.data,
                distance,
                SHAFT_MULTIPLIER["utility4"]
            )

        # 아이언
        if form.iron7_selected.data:

            if not form.iron7_distance.data:
                flash("7번 아이언 목표 비거리를 입력해주세요.")
                return render_template("recommend.html", form=form)

            distance = convert_distance(
                form.iron7_distance.data,
                form.distance_unit.data
            )

            result["iron7"] = recommend_shaft_weight(
                form.gender.data,
                form.user_height.data,
                form.user_weight.data,
                distance,
                SHAFT_MULTIPLIER["iron7"]
            )

        # 플렉스
        if form.swing_speed.data:

            speed = convert_speed(
                form.swing_speed.data,
                form.speed_unit.data
            )

            flex = recommend_flex(speed)

        elif form.driver_selected.data:

            flex = recommend_flex_by_distance(
                convert_distance(
                    form.driver_distance.data,
                    form.distance_unit.data
                )
            )

        else:
            flex = "-"

        # 기존 결과 수정 또는 새로 생성
        recommend = ShaftRecommend.query.filter_by(
            user_id=g.user.id
        ).first()

        if recommend is None:
            recommend = ShaftRecommend(user_id=g.user.id)
            db.session.add(recommend)

        recommend.driver_weight = result.get("driver")
        recommend.wood5_weight = result.get("wood5")
        recommend.utility4_weight = result.get("utility4")
        recommend.iron7_weight = result.get("iron7")
        recommend.driver_flex = flex

        db.session.commit()

        return render_template(
            "recommend.html",
            form=form,
            result=result,
            flex=flex
        )

    return render_template(
        "recommend.html",
        form=form
    )