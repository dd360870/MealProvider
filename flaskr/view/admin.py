from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.view.auth import admin_required, login_required

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route("/")
@admin_required
def index():
    return render_template('admin/index.html')