from flask import render_template, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import User,  Category,Pitches
from .. import db, photos
from .forms import FormCategory,UpdateProfile,FormPitch

@main.route('/')
def index():

    # pitches = Post.query.order_by(Post.timestamp.desc()).all()

    return render_template('index.html')
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))


    return render_template('profile/update_profile.html',form =form)


@main.route('/category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = FormCategory()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully.')
        return redirect(url_for('.index'))
    return render_template('category.html', form=form)

# @main.route('/pitch',methods=['GET','POST'])
# @login_required
# def add_pitch():
#     form=FormPitch()
#     if form.validate_on_submit():
#         pitch = Pitches(name=form.name.data)
#         db.session.add(pitch)
#         db.session.commit()
#         flash('Pitch added successfully.')
#         return redirect(url_for('.index'))
#     return render_template('pitch.html', form=form)

@main.route('/pitches/new/', methods = ['GET', 'POST'])
@login_required
def new_pitch():
  form = FormPitch()
  
  if form.validate_on_submit():
    description = form.description.data
    title = form.title.data
    user_id = current_user
    category = form.category.data
    new_pitch = Pitches(owner_id=current_user._get_current_object().id, title=title, description=description, category=category)
    db.session.add(new_pitch)
    db.session.commit()

    return redirect(url_for('main.index'))

  return render_template('pitches.html', form=form)



