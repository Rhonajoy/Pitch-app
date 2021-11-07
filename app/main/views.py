from flask import render_template,request, redirect, url_for, abort, flash
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
    form = UpdateProfile()
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

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

# @main.route('/pitches/new/', methods = ['GET', 'POST'])
# @login_required
# def new_pitch():
#   form = FormPitch()
  
#   if form.validate_on_submit():
#     name = form.name.data
#     content= form.content.data
#     user_id = current_user.id
#     category = form.category.data
#     new_pitch = Pitches(user_id=user_id, name=name, content=content, category=category)
#     db.session.add(new_pitch)
#     db.session.commit()

#     return redirect(url_for('main.index'))

#   return render_template('pitches.html', form=form)
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))




