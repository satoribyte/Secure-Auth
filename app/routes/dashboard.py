from flask import Blueprint, render_template
from flask_login import login_required, current_user

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard.route('/', endpoint='dashboard_page')
@login_required
def dashboard_page():
    return render_template('dashboard.html', user=current_user)