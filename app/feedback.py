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
        
        if feedbacks is None:
            return jsonify({}), 404
         
        return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)
    
    else:
        return jsonify({}), 404
    
@bp.route('/feedback_error')
def error():
    if current_user.is_authenticated:
                
        return render_template('reviewerror.html')
    
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
    
@bp.route('/recent_feedback/edit/<int:product_id>')
def submit_edits(product_id):
    if current_user.is_authenticated:

        user_id = current_user.id

        product = Product.get(product_id)

        return render_template('submitedits.html', product=product)

        #FeedbackItem.add_product_feedback(user_id, product_id)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)
    
    else:
        return jsonify({}), 404
    
@bp.route('/recent_feedback/add_review/<int:product_id>', methods=['GET', 'POST'])
def add_feedback(product_id):
    if current_user.is_authenticated:
        
        # RETURN ERROR IF REVIEW HAS ALREADY BEEN MADE
        current_reviews = FeedbackItem.get_product_reviews(current_user.id)
        if current_reviews is not None:
            return redirect(url_for('recent_feedback.error'))
    

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

@bp.route('/recent_feedback/edit_review/<int:product_id>', methods=['GET', 'POST'])
def edit_feedback(product_id):
    if current_user.is_authenticated:
        user_id = current_user.id
        review_text = request.form["edit"]

        #return render_template('submitfeedback.html')

        test = FeedbackItem.edit_product_feedback(user_id, product_id, review_text)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)

        if test is True:
            return redirect(url_for('recent_feedback.recentFeedback'))
    
    else:
        return jsonify({}), 404

@bp.route('/recent_feedback/delete_review/<int:product_id>/<review>/<type>', methods=['POST'])
def delete_feedback(product_id, review, type):
    if current_user.is_authenticated:

        user_id = current_user.id
        

        #return render_template('submitfeedback.html')

        if type == "Product":
            test = FeedbackItem.delete_product_feedback(user_id, product_id, review)
        else:
            test = FeedbackItem.delete_seller_feedback(user_id, product_id, review)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)

        if test is True:
            return redirect(url_for('recent_feedback.recentFeedback'))
    
    else:
        return jsonify({}), 404