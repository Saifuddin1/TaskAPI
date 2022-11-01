
from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask_login import login_required,current_user
from . import db
from .models import Task,User

show = Blueprint('show',__name__)

@show.route("/")
@login_required
def index():
    tasks = Task.query.all()
    task_list = []
    for ele in tasks:
        d = {"empact" : ele.empact,"ease" : ele.ease,"confidence" : ele.confidence,"average" : ele.average,"user":ele.user.username,"author" : ele.author,"id":ele.id}
        task_list.append(d)
    task_list = sorted(task_list,key = lambda i:i['average'],reverse = True)
    return render_template('index.html', user = current_user, tasks = task_list)



@show.route("/create-post",methods = ["GET","POST"])
@login_required
def create_task():
    if request.method =="POST":
        empact = request.form.get('empact')
        ease = request.form.get('ease')
        confidence = request.form.get('confidence')
        average = round((int(empact) + int(ease) + int(confidence))/3,2)
        if not empact or not ease or not confidence:
            flash('task cannot be empty',category = 'error')
        else:
            task = Task(empact = empact,ease = ease,confidence = confidence,average = average, author=current_user.id)
            db.session.add(task)
            db.session.commit()
            flash('Task created!', category='success')
            return redirect(url_for('show.index'))
    return render_template('create-task.html',user = current_user)



@show.route("/delete-task/<id>")
@login_required
def delete_task(id):
    print("in to delete")
    task = Task.query.filter_by(id = id).first()
    if not task:
        flash("Task does not exist", category = "error")
    elif current_user.id != task.author:
        flash("You do not have permission to delete this task", category = 'error')
    else:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted",category= 'success')
    return redirect(url_for('show.index'))



@show.route("/tasks/<username>")
@login_required
def tasks(username):
    user = User.query.filter_by(username= username).first()
    if not user:
        flash('No user exist with this name', category='error')
        return redirect(url_for('show.index'))
    tasks = user.tasks
    task_list = []
    for ele in tasks:
        d = {"empact" : ele.empact,"ease" : ele.ease,"confidence" : ele.confidence,"average" : ele.average,"user":ele.user.username,"author" : ele.author,"id" : ele.id}
        task_list.append(d)
    task_list = sorted(task_list,key = lambda i:i['average'],reverse = True)
    
    return render_template("task.html",user = current_user, tasks = task_list,username = username)



@show.route("/update-task/<task_id>",methods = ["GET","POST"])
@login_required
def update_task(task_id):
    print("into update")
    t = Task.query.filter_by(id=task_id).first()
    data = request.form
    if request.method == 'POST':
        t.empact= data.get("empact")
        t.ease= data.get("ease")
        t.confidence = data.get("confidence")
        t.average = round((int(data.get("empact")) + int(data.get("ease")) + int(data.get("confidence")))/3,2)
        db.session.commit()
        return redirect(url_for('show.index'))
    return render_template('updatetask.html',task = t,user = current_user)



@show.route("/user-profile")
@login_required
def user_profile():
    return render_template('userprofile.html',user = current_user)



@show.route("/update-profile",methods = ["GET","POST"])
@login_required
def update_profile():
    my_data = User.query.filter_by(id=current_user.id).first()
    data = request.form
    if request.method == 'POST':
        my_data.username= data.get("username")
        my_data.contact= data.get("contact")
        db.session.commit()
        return redirect(url_for('show.user_profile'))
    return render_template('updateprofile.html',user = current_user)


