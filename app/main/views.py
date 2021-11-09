from flask import render_template,request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import Likes, User,Pitches,Comment,Dislikes
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
@main.route('/comments/<pitch_id>', methods=['GET', 'POST'])
@login_required
def comments(pitch_id):
    
    # get all comments of the pitch
    comments = Comment.query.filter_by(pitch_id=pitch_id).all()
    pitch = Pitches.query.get(pitch_id)
    form = CommentForm()
    if pitch is None:
        abort(404)
    
    if form.validate_on_submit():
            comment = Comment(
            content=form.content.data,
            pitch_id=pitch_id,
            user_id=current_user.id

        )
            db.session.add(comment)
            db.session.commit()
            form.content.data = ''
            flash('Your comment has been posted successfully!')
    return render_template('comments.html',pitches= pitch, comment=comments, form = form)
@main.route('/like/<pitch_id>', methods=['GET', 'POST'])
@login_required
def like(pitch_id):
    pitch = Pitches.query.get(pitch_id)
    if pitch is None:
        abort(404)
    # check if the user has already liked the pitch
    like = Likes.query.filter_by(user_id=current_user.id, pitch_id=pitch_id).first()
    if like is not None:
        # if the user has already liked the pitch, delete the like
        db.session.delete(like)
        db.session.commit()
        flash('You have successfully unlike the pitch!')
        return redirect(url_for('.index'))
    # if the user has not liked the pitch, add a like
    new_like = Likes(
        user_id=current_user.id,
        pitch_id=pitch_id
    )
    db.session.add(new_like)
    db.session.commit()
    
    return redirect(url_for('.index'))
@main.route('/dislike/<pitch_id>', methods=['GET', 'POST'])
@login_required
def dislike(pitch_id):
    pitch = Pitches.query.get(pitch_id)
    if pitch is None:
        abort(404)
    # check if the user has already liked the pitch
    dislike =  Dislikes.query.filter_by(user_id=current_user.id, pitch_id=pitch_id).first()
    if dislike is not None:
        # if the user has already liked the pitch, delete the like
        db.session.delete(dislike)
        db.session.commit()
        
        return redirect(url_for('.index'))
    # if the user has not liked the pitch, add a like
    new_dislike = Dislikes(
        user_id=current_user.id,
        pitch_id=pitch_id
    )
    db.session.add(new_dislike)
    db.session.commit()
    
    return redirect(url_for('.index'))




