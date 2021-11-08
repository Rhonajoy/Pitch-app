from flask import render_template,request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import User,  Category,Pitches,Comment
from .. import db, photos
from .forms import UpdateProfile,FormPitch,CommentForm

@main.route('/')
def index():
    pitches = Pitches.query.order_by(Pitches.date_created).all()
    
    return render_template('index.html',pitches=pitches)
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


    return render_template('profile/update.html',form =form)


@main.route('/createpitch', methods=['GET', 'POST'])
@login_required
def new_pitch():
    pitch_form = FormPitch()
    if pitch_form.validate_on_submit():
        title = pitch_form.title.data
        category = pitch_form.category.data
        content = pitch_form.content.data
        new_pitch = Pitches(title=title, category=category, content=content)
        new_pitch.save_pitches()
        
        return redirect(url_for('main.index'))

   
        

    return render_template('pitch.html', pitch_form = pitch_form)
@main.route('/category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CommentForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully.')
        return redirect(url_for('.index'))
    return render_template('category.html', form=form)
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
@main.route('/comment/new/<int:pitch_id>', methods = ['GET', 'POST'])
@login_required
def new_comment(pitch_id):
  form = CommentForm()
  pitch = Pitches.query.get(pitch_id)
  if form.validate_on_submit():
    content = form.content.data
    new_comment = Comment(content=content, pitch_id = pitch_id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('.new_comment', pitch_id = pitch_id))

  
  return render_template('comments.html', form = form, pitch = pitch)





