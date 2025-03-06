from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, 
                           error_message="Page Not Found", 
                           error_description="Oops! The page you are looking for does not exist."), 404

@errors.app_errorhandler(403)
def forbidden_error(error):
    return render_template('error.html', error_code=403, 
                           error_message="Access Forbidden", 
                           error_description="You do not have permission to access this page."), 403

@errors.app_errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500, 
                           error_message="Internal Server Error", 
                           error_description="Something went wrong. Please try again later."), 500