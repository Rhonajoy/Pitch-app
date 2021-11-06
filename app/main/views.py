from flask import render_template, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import User,  Post, Category
from .. import db, photos
from .forms import  CategoryForm

@main.route('/')
def index():

    # pitches = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template('index.html')
@main.route('/user/<username>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


    
        

@main.route('/category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully.')
        return redirect(url_for('.index'))
    return render_template('category.html', form=form)



