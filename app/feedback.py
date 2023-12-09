from flask import render_template, redirect, url_for, request
from flask_login import current_user
from flask import jsonify
import datetime

from .models.feedbackitem import FeedbackItem
from .models.product import Product
from .models.seller import Seller
from .models.transaction import Transaction

from flask import Blueprint
bp = Blueprint('recent_feedback', __name__)

@bp.route('/recent_feedback')
def recentFeedback():
    if current_user.is_authenticated:
        feedbacks = FeedbackItem.get_all(current_user.id)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        if feedbacks is None:
            return render_template('no_reviews.html')
         
        return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)
    
    else:
        return jsonify({}), 404
    
@bp.route('/feedback_error')
def error():
    if current_user.is_authenticated:
                
        return render_template('reviewerror.html')
    
    else:
        return jsonify({}), 404

@bp.route('/feedback_errorSELLER')
def errorSELLER():
    if current_user.is_authenticated:
                
        return render_template('reviewerrorSELLER.html')
    
    else:
        return jsonify({}), 404

@bp.route('/order_error')
def ordererror():
    if current_user.is_authenticated:
                
        return render_template('ordererror.html')
    
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

@bp.route('/recent_feedback/addSELLER/<int:seller_id>')
def submit_SELLERfeedback(seller_id):
    if current_user.is_authenticated:

        user_id = current_user.id

        seller = Seller.seller_details(seller_id)[0]

        #return jsonify({seller})

        return render_template('submitSELLERfeedback.html', seller=seller)
    
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
    
@bp.route('/recent_feedback/editSTARS/<int:product_id>')
def submit_editsSTARS(product_id):
    if current_user.is_authenticated:

        user_id = current_user.id

        product = Product.get(product_id)

        return render_template('submiteditsSTARS.html', product=product)

        #FeedbackItem.add_product_feedback(user_id, product_id)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)
    
    else:
        return jsonify({}), 404
    
@bp.route('/recent_feedback/editSELLER/<int:seller_id>')
def submit_SELLERedits(seller_id):
    if current_user.is_authenticated:

        user_id = current_user.id

        seller = Seller.seller_details(seller_id)[0]

        return render_template('submitSELLERedits.html', seller=seller)

        #FeedbackItem.add_product_feedback(user_id, product_id)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)
    
    else:
        return jsonify({}), 404

@bp.route('/recent_feedback/editSELLERSTARS/<int:seller_id>')
def submit_SELLEReditsSTARS(seller_id):
    if current_user.is_authenticated:

        user_id = current_user.id

        seller = Seller.seller_details(seller_id)[0]

        return render_template('submitSELLEReditsSTARS.html', seller=seller)

        #FeedbackItem.add_product_feedback(user_id, product_id)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)
    
    else:
        return jsonify({}), 404
    
@bp.route('/recent_feedback/add_review/<int:product_id>', methods=['GET', 'POST'])
def add_feedback(product_id):
    if current_user.is_authenticated:
        
        # RETURN ERROR IF REVIEW HAS ALREADY BEEN MADE
        current_reviews = FeedbackItem.get_product_reviews(current_user.id, product_id)
        if current_reviews is not None:
            return redirect(url_for('recent_feedback.error'))
    
        user_id = current_user.id

        review_text = request.form['review']
        star_rating = int(request.form['rating'])

        #return render_template('submitfeedback.html')

        test = FeedbackItem.add_product_feedback(user_id, product_id, review_text, star_rating)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)

        if test is True:
            return redirect(url_for('recent_feedback.recentFeedback'))
    
    else:
        return jsonify({}), 404
    
@bp.route('/recent_feedback/add_SELLERreview/<int:seller_id>', methods=['GET', 'POST'])
def add_SELLERfeedback(seller_id):
    if current_user.is_authenticated:
        
        # RETURN ERROR IF REVIEW HAS ALREADY BEEN MADE
        current_reviews = FeedbackItem.get_seller_reviews(current_user.id, seller_id)
        if current_reviews is not None:
            return redirect(url_for('recent_feedback.errorSELLER'))
        
        # RETURN ERROR IF CURRENT USER HAS NOT ORDERED FROM SELLER
        orders = Transaction.transactions(current_user.id)
        if orders is None:
            return redirect(url_for('recent_feedback.ordererror'))

        user_id = current_user.id

        review_text = request.form['seller_review']
        star_rating = int(request.form['seller_rating'])

        test = FeedbackItem.add_seller_feedback(user_id, seller_id, review_text, star_rating)

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

@bp.route('/recent_feedback/edit_reviewSTARS/<int:product_id>', methods=['GET', 'POST'])
def edit_feedbackSTARS(product_id):
    if current_user.is_authenticated:
        user_id = current_user.id
        star_rating = int(request.form['editSTARS'])

        #return render_template('submitfeedback.html')

        test = FeedbackItem.edit_product_STARS(user_id, product_id, star_rating)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)

        if test is True:
            return redirect(url_for('recent_feedback.recentFeedback'))
    
    else:
        return jsonify({}), 404
    
@bp.route('/recent_feedback/edit_SELLERreview/<int:seller_id>', methods=['GET', 'POST'])
def edit_SELLERfeedback(seller_id):
    if current_user.is_authenticated:
        user_id = current_user.id
        review_text = request.form["editSELLER"]

        #return render_template('submitfeedback.html')

        test = FeedbackItem.edit_seller_feedback(user_id, seller_id, review_text)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)

        if test is True:
            return redirect(url_for('recent_feedback.recentFeedback'))
    
    else:
        return jsonify({}), 404
    
@bp.route('/recent_feedback/edit_SELLERreviewSTARS/<int:seller_id>', methods=['GET', 'POST'])
def edit_SELLERfeedbackSTARS(seller_id):
    if current_user.is_authenticated:
        user_id = current_user.id
        star_rating = request.form["editSELLERSTARS"]

        #return render_template('submitfeedback.html')

        test = FeedbackItem.edit_seller_STARS(user_id, seller_id, star_rating)

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
    
@bp.route('/recent_feedback/sellerfeedpage/<int:seller_id>',  methods=['GET', 'POST'])
def get_seller_feedback_page(seller_id):
    if current_user.is_authenticated:

        user_id = current_user.id

        seller = Seller.seller_details(seller_id)[0]

        seller_reviews = (Product.get_seller_reviews(seller.user_id))
        avg_star_ratingSELLER = (Product.get_seller_avgstars(seller.user_id))
        num_ratingsSELLER = (Product.get_num_seller_ratings(seller.user_id))

        return render_template('seller_reviews_sorted.html', seller=seller, seller_reviews = seller_reviews, avg_star_ratingSELLER = avg_star_ratingSELLER, num_ratingsSELLER = num_ratingsSELLER )

        #FeedbackItem.add_product_feedback(user_id, product_id)

        #return jsonify([feedback.__dict__ for feedback in feedbacks])
        
        #return render_template('recent_feedbacks.html', recent_feedbacks = feedbacks)
    
    else:
        return jsonify({}), 404