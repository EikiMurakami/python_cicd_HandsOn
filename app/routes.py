from flask import Blueprint, render_template, redirect, url_for, request
from .models import db, Task
from .forms import TaskForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@bp.route('/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, description=form.description.data, done=form.done.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add_task.html', form=form)

@bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.done = form.done.data
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('edit_task.html', form=form, task=task)

@bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.index'))
