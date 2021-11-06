from flask import render_template, redirect, url_for, abort, flash, request
from . import main
from flask_login import login_required, current_user
from ..models import User,  Post, Category
from .. import db, photos
from .forms import  CategoryForm

@main.route('/')
def index():

    # pitches = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template('index.html')

    
        

@main.route('/category', methods=['GET', 'POST'])
# @login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully.')
        return redirect(url_for('.index'))
    return render_template('category.html', form=form)



