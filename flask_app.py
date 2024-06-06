
# A very simple Flask Hello World app for you to get started with...
import math
from flask import Flask, render_template,request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from socket import gethostname
from flask_login import (LoginManager, UserMixin,
    login_user, logout_user, login_required, current_user)
from datetime import datetime
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
    )


# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"
# initialize the app with the extension
# create the extension
db = SQLAlchemy(app)

#Setup the flask login manager
login_manager = LoginManager()
login_manager.init_app(app)
#Model
class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(4096))
    posters_id = db.Column(db.Integer, db.ForeignKey("poster.id"))
    author = db.relationship("Poster", back_populates = "posts")

class Poster(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
    posts = db.relationship("Post", back_populates = "author")

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(4096))
    #date= datetime.datetime.now()
    #print(date.strftime("%Y-%m-%d"))
    DueDate= db.Column(db.DateTime)
    Status= db.Column(db.String(4096))



#class Review(db.Model):
#    __tablenme__ = "reviews"
#    id= db.Column(db.Integer, primary_key=True)
 #   text = db.Column(db.String(4096))
  #  reviewers_id = db.Column(db.Integer,db.ForeignKey("reviewer.id"))
   # author = db.relationship("Reviewer", back_populates="reviews")

#class Reviewer(UserMixin,db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  username = db.Column(db.String(250), unique=True,
   #                      nullable=False)
    #password = db.Column(db.String(250),
     #                    nullable=False)
  #  reviews = db.relationship("Review", back_populates = "author")


class Movie(db.Model):
    __tablename__="movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    link = db.Column(db.String(250))


@login_manager.user_loader
def loader_user(user_id):
    return Poster.query.get(user_id)


#@login_manager.user_loader
#def loader_review(reviewer_id):
 #   return Reviewer.query.get(reviewer_id)







numPageLoads = 0

#Controllers
@app.route('/')
def hello_world():
    global numPageLoads
    numPageLoads+=1
    return 'Hello from Flask!'

###
# The /triangle URL is associated with the triangle function
####
@app.route('/circumfrence', methods=['POST','GET'])
def circumfrence():
    if request.method == 'GET':
        return render_template('circumfrence_input.html')
    if request.method == 'POST':
        radius = int(request.form['radius'])
        c = (2*3.14*radius)

        return render_template('circumfrence_result.html', radius = radius, c=c)


@app.route('/triangle', methods=['POST', 'GET'])
def triangle():
    if request.method == 'GET':
        return render_template('pythagorean_input.html') # <- View
        if request.method == 'POST':
            a = int(request.form['a'])
            b = int(request.form['b'])

            c = math.sqrt(a*a + b*b)

        return render_template('pythagorean_result.html', a=a, b=b, c=c)

#user login


# create task
@app.route('/new_task', methods = ['POST', 'GET'])
#@login_required
def new_task():
    if request.method == 'GET':
        return render_template('new_task.html')
        return redirect("/todolist")
    if request.method == 'POST':
        textFromForm = request.form['text']
        TaskFilter = request.form['complete']
        DueDate = datetime.strptime(request.form["due_date"], "%Y-%m-%d")
        new_task = Task(text=textFromForm, DueDate=DueDate, Status= TaskFilter)
        db.session.add(new_task)
        db.session.commit()
        #return render_template('todolist.html', new_task = Task)
        return redirect("/todolist")

@app.route('/Complete')
def task():
    ToFilter = Task.query.filter_by(Status = 'complete').all()
    return render_template('complete.html', task=ToFilter)


#retrieve all tasks
@app.route('/todolist')
def tasks():
    tasks = Task.query.all()
    #ToFilter = Task.query.filter_by(Status='complete').all()
    return render_template('todolist.html', tasks =tasks)

#update an due date from list
@app.route('/edit_task/<id>', methods = ['POST', 'GET'])
def edit_task(id):
    if request.method == 'GET':
        toEdit = Task.query.get(id)
        return render_template('edit_task.html', task= toEdit)
    if request.method =='POST':
        toEdit.DueDate = datetime.strptime(request.form['due_date'], "%Y-%m-%d")
        toEdit.text = request.form['text']
    #request.form['text']
        db.session.commit()
        return redirect("/todolist")

#delete task from list
@app.route('/delete_task/<id>')
def delete_task(id):
    toDelete= Task.query.get(id)
    db.session.delete(toDelete)
    db.session.commit()
    return redirect("/todolist")

########
# USER CRUD Controllers
########


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("add_user.html")
    if request.method == "POST":
        password=request.form.get("password")

        #note the password hashing here!
        user = Poster(username=request.form.get("username"),
                     password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login_user.html")
    # If a post request was made, find the user by
    # filtering for the username
    if request.method == "POST":
        user = Poster.query.filter_by(
            username=request.form.get("username")).first()
        # Check if the password entered is the
        # same as the user's password
        password =  request.form.get("password")
        if user and check_password_hash(user.password, password):
            # Use the login_user method to log in the user
            login_user(user)
            flash('You were successfully logged in')
            return redirect("/homepage")
            # Redirect the user back to the home
        else:
            flash('Your username or password were incorrect')
            return redirect("/login")


@app.route("/logout")
def logout():
    logout_user()
    flash('You were successfully logged out')
    return redirect("/homepage")

'''@app.route("/main")
def main():
    main = Review.query.all()
    return render_template('main.html', main = main)
    '''
'''
@app.route("/add_review", methods=['POST','GET'])
#@login_required
def add_review():
    if request.method == 'GET':
        return render_template('add_review.html')
    if request.method == 'POST':
        Formtext= request.form['text']
        newReview= Review(text=Formtext,author=current_user)
        db.session.add(newReview)
        db.session.commit()
        return redirect("/main")


@app.route('/edit_review/<id>', methods=['POST', 'GET'])
#@login_required
def edit_review(id):
    if request.method == 'GET':
        to_Edit = Review.query.get(id)
        #we can check to see if the author of the existing post
        #is the same as the current_user
        if(to_Edit.author != current_user):
            flash("You are not the author of this comment, so you can't edit it!")
            return redirect("/main")
        return render_template('edit_review.html',review=to_Edit)
    if request.method == 'POST':
        to_Edit = Review.query.get(id)
        to_Edit.text = request.form['text']
        db.session.commit()
        return redirect("/main")

@app.route('/delete_review/<id>')
#@login_required
def delete_review(id):
    Delete = Review.query.get(id)
    if(Delete.author != current_user):
        flash("You are not the author of this comment, so you can't delete it!")
        return redirect("/main")
    db.session.delete(Delete)
    db.session.commit()
    return redirect("/main")

@app.route("/add_movie", methods= ['POST','GET'])
def add_movie():
    if request.method == 'GET':
        add_movie = Movie.query.all()
        return render_template('add_movie.html', add_movie = add_movie)
    if request.method == 'POST':
        form_title= request.form['title']
        form_link = request.form['link']
        newMovie= Movie(title=form_title, link = form_link)
        db.session.add(newMovie)
        db.session.commit()
        return redirect("/add_movie")

@app.route('/delete_movie/<id>')

def delete_movie(id):
    delete = Movie.query.get(id)
    db.session.delete(delete)
    db.session.commit()
    return redirect("/main")
'''

###
# Important code that was meant for this project
###
@app.route("/homepage")
#@login_required
def homepage():
    # the first line gathers up all the posts on the homepage.
    homepage = Post.query.all()
    return render_template('homepage.html', homepage = homepage)

@app.route("/add_post", methods= ['POST','GET'])
@login_required
def post():
    if request.method == 'GET':
        return render_template('add_post.html')
    if request.method == 'POST':
        Posting = request.form['text']
        newPost= Post(text=Posting,author=current_user)
        db.session.add(newPost)
        db.session.commit()
        return redirect("homepage")
        return render_template('homepage.html')


@app.route("/edit_post/<id>", methods= ['POST','GET'])
@login_required
def edit_post(id):
    if request.method == 'GET':
        Post_Edit = Post.query.get(id)
        #we can check to see if the author of the existing post
        #is the same as the current_user
        if(Post_Edit.author != current_user):
            flash("You are not the author of this comment, so you can't edit it!")
            return redirect("/homepage")
        return render_template('edit_post.html',post=Post_Edit)
    if request.method == 'POST':
        Post_Edit = Post.query.get(id)
        Post_Edit.text = request.form['text']
        db.session.commit()
        return redirect("/homepage")

@app.route('/delete_post/<id>')
@login_required
def delete_post(id):
    Delete = Post.query.get(id)
    if(Delete.author != current_user):
        flash("You are not the author of this comment, so you can't delete it!")
        return redirect("/homepage")
    db.session.delete(Delete)
    db.session.commit()
    return redirect("/homepage")




if __name__ == '__main__':
    print("you clicked the blue button!")
    with app.app_context():
        db.drop_all()
        db.create_all()
        me = Poster(username='admin',password=generate_password_hash("admin"))
        myPost = Post(text='''This is a sample review''',author=me)

        #manually add a comment

        db.session.add(myPost)
        db.session.commit()

    if 'liveconsole' not in gethostname():
        app.run()
