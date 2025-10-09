from flask import Blueprint, render_template

destbp = Blueprint('destination', __name__, url_prefix='/destinations')

@destbp.route ('/<id>')
def show (id):
    return render_template (destination/show.html)

