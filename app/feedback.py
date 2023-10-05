from flask import render_template, redirect, url_for
from flask_login import current_user
from flask import jsonify
import datetime

from .models.feedbackitem import FeedbackItem

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