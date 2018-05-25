from app import app,db,oid,lm,mail
from flask import render_template,flash,redirect,session,url_for,request,g
from .forms import LoginForm,EditForm,PostForm,AnswerForm
from flask_login import login_user,logout_user,current_user,login_required
from .models import User,Hipe,Answer,random_hipe
from datetime import datetime
from flask_mail import Message
from config import POSTS_PER_PAGE
from email import follower_notification
from oauth import OAuthSignIn,sign_in_images


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/static')
@app.route('/', methods =['GET','POST'])
@app.route('/index', methods =['GET','POST'])
@app.route('/index/<int:page>', methods =['GET','POST'])
@login_required
def index(page=1):
    user = g.user 
       
    return render_template('index.html',
            title = 'Home',
            user = user,
            current_page = 'index')

@app.route('/login',methods = ['GET','POST'])
@oid.loginhandler
def login():
 
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        session['remember me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['username','email'])
    return render_template('login.html',
            title = 'Sign In',
            form = form,
            providers =  ['facebook','google']
            )
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == '':
        flash('Invalid login. Please try agin')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        username = resp.username
        if username is None or username == '':
            username = resp.email.split('@')[0]
        username = User.make_unique_username(username)
        flash('Adding a user with name {}'.format(username))
        user = User(username = username, email = resp.email)
        db.session.add(user)
        db.session.commit()
        db.session.add(user.follow(user))
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me',None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    flash('you were successfully logged out, please log in again to play HIPE')
    logout_user()
    return redirect(url_for('login'))

@app.route('/user/<username>')
@app.route('/user/<username>/<int:page>')
@login_required
def user(username,page=1):
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash('User %s not found.' %username)
        return redirect(url_for('index'))
    hipes = user.solved.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html',
            user = user,
            hipes = hipes,
            current_page = 'user')

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash('User %s not found.' %username)
        return redirect(url_for('index'))
    if user == g.user:
        flash('Stop following yourself!')
        return redirect(url_for('user',username = username))

    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow %s right now. Are you already following them?' %username)
        return redirect(url_for('user',username = username))
    db.session.add(u)
    db.session.commit()
    follower_notification(user, g.user)
    flash('You are now following %s!' %username)
    return redirect(url_for('user',username = username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        flash('User %s not found.' %username)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You cannot unfollow yourself.')
        return redirect(url_for('user',username = username))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow %s right now. Are you sure you are following them?' %username)
        return redirect(url_for('user',username = g.user.username))
    db.session.add(u)
    db.session.commit()
    flash('You are no longer following %s!' %username)
    return redirect(url_for('user',username = username))




@app.route('/edit', methods=['GET','POST'])
@login_required
def edit():
    form = EditForm(g.user.display_name)
    if form.validate_on_submit():
        g.user.display_name = form.display_name.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Thanks %s your changes were saved' %form.display_name.data)
        return redirect(url_for('user',username = g.user.username))
    else:
        form.display_name.data = g.user.display_name
        form.about_me.data = g.user.about_me
    return render_template('edit.html',form=form)

@app.route('/hipe/<letters>', methods = ['GET','POST'])
@login_required
def hipe(letters): 
    hipe = Hipe.query.filter_by(letters = letters.lower()).first()
    if hipe == None:
        flash('We do not have %s as a HIPE at the moment. Should we?' %letters)
        return redirect(url_for('index'))
    form = AnswerForm(hipe)
    if form.validate_on_submit():
        flash('Well done!')
        if not hipe in g.user.solved: 
            db.session.add(g.user.solve(hipe))
            db.session.commit()
        return redirect(url_for('answer',letters=letters))
    return render_template('hipe.html',
            form = form,
            hipe = hipe)

@app.route('/answer/<letters>', methods = ['GET','POST'])
@login_required
def answer(letters): 
    hipe = Hipe.query.filter_by(letters = letters.lower()).first()
    if hipe == None:
        flash('We do not have %s as a HIPE at the moment. Should we?' %letters)
        return redirect(url_for('index'))
    if not g.user.has_solved(hipe):
        flash('You have not solved that HIPE yet. No peeking!')
        return redirect(url_for('hipe',letters = letters))
    answers = Answer.query.filter_by(hipe_id = hipe.id)
    return render_template('answer.html',
            hipe = hipe,
            answers = answers)

@app.route('/random')
@login_required
def random():
    hipe = random_hipe() 
    if g.user.solved.count() == len(Hipe.query.all()):
        flash('You have solved all our HIPEs, well done!')
        return redirect(url_for('user',username = g.user.username))
    while g.user.has_solved(hipe):
        hipe = random_hipe()
    return redirect(url_for('hipe',letters = hipe.letters))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    username, email,display_name = oauth.callback()
    if email is None:
        flash('Authentication failed')
        return redirect(url_for('index'))
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username = username, email = email,display_name = display_name)
        db.session.add(user)
        db.session.commit()
    login_user(user,True)
    return redirect(url_for('index'))





@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

