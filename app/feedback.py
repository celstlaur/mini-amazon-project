from flask import render_template, redirect, url_for, request
from flask_login import current_user
from flask import jsonify
import datetime

from .models.feedbackitem import FeedbackItem
from .models.product import Product

from flask import Blueprint
bp = Blueprint('recent_feedback', __name__)

@bp.route('/recent_feedback')

def recentFeedback():
    if current_user.is_authenticated:
        feedbacks = FeedbackItem.get_all(current_user.id)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)
    
    else:
        return jsonify({}), 404
    
@bp.route('/recent_feedback/add/<int:product_id>')
def submit_feedback(product_id):
    if current_user.is_authenticated:

        user_id = current_user.id

        product = Product.get(product_id)

        return render_template('submitfeedback.html', product=product)

        #FeedbackItem.add_product_feedback(user_id, product_id)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)
    
    else:
        return jsonify({}), 404
    
@bp.route('/recent_feedback/add_review/<int:product_id>', methods=['GET', 'POST'])
def add_feedback(product_id):
    if current_user.is_authenticated:

        user_id = current_user.id
        review_text = request.form["review"]

        #return render_template('submitfeedback.html')

        test = FeedbackItem.add_product_feedback(user_id, product_id, review_text)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)

        if test is True:
            return redirect(url_for('recent_feedback.recentFeedback'))
    
    else:
        return jsonify({}), 404