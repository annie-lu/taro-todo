# app/home/views.py

from flask import render_template
from flask_login import login_required, current_user
from .. import login_manager
from datetime import datetime as dt
from datetime import date, timedelta

from flask import current_app as app, request, make_response, render_template, redirect

from .. import db
from ..database.models.account import Account
from ..database.models.pet import Pet
from ..database.models.task import Task
from collections import OrderedDict

from . import home


from . import home


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return redirect('/list')


@app.route('/list')
@login_required
def list():
    tasks = Task.query.filter(db.and_(Task.account_id==current_user.id,Task.deleted_at==dt.min)).all()
    print(tasks)
    tasks = sorted(tasks, key=lambda x: x.id)
    pet = Pet.query.filter_by(account_id=current_user.id)[0]

    return render_template('home/list.html', tasks=tasks, pet=pet)

@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'Error'

    task = Task(content,current_user.id)
    db.session.add(task)
    db.session.commit()
    return redirect('/list')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/list')
    task.deleted_at = dt.now()
    db.session.commit()
    return redirect('/list')


@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)
    pet = Pet.query.filter_by(account_id=current_user.id)[0]

    if not task:
        return redirect('/list')
    if task.done:
        task.done = False
        pet.points -=1
        task.completed_at = dt.min
    else:
        task.done = True
        task.completed_at=dt.now()
        pet.points += 1
    filter_day = dt.today() - timedelta(days = 3)
    pet.health = min(5,len(Task.query.filter(db.and_(Task.account_id==current_user.id,Task.completed_at>=filter_day)).all()))/5

    db.session.commit()
    return redirect('/list')
