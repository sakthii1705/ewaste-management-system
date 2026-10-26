@'
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from app.models import Device, Component, ComponentRequest

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@main_bp.route("/dashboard")
@login_required
def dashboard():
    device_count = Device.query.count()
    component_count = Component.query.count()
    available_count = Component.query.filter_by(status="available").count()
    pending_requests = ComponentRequest.query.filter_by(status="pending").count()

    recent_devices = Device.query.order_by(
        Device.created_at.desc()
    ).limit(5).all()

    return render_template(
        "dashboard/index.html",
        user=current_user,
        device_count=device_count,
        component_count=component_count,
        available_count=available_count,
        pending_requests=pending_requests,
        recent_devices=recent_devices
    )
'@ | Set-Content -Encoding utf8 "app\blueprints\main.py"