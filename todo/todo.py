from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo', __name__)

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    db, c = get_db()
    c.execute(
        'select t.id, t.description, u.username, t.completed, t.created_at '
        'from todo t JOIN user u on t.created_by = u.id where t.created_by = %s order by created_at desc',
        (g.user['id'],)
    )
    todos = c.fetchall()

    #Crear todo:
    if request.method == 'POST':
        description = request.form['description']
        error = None

        if not description:
            error = 'Descripción es requerida.'
        
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'insert into todo (description, completed, created_by)'
                ' values (%s, %s, %s)',(description, False, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/index.html', todos=todos)

def get_todo(id):
    db, c = get_db()
    c.execute(
        'select t.id, t.description, t.completed, t.created_by, t.created_at, u.username '
        'from todo t join user u on t.created_by = u.id where t.id = %s', (id, )
    )

    todo = c.fetchone()

    if todo is None:
        abort(404, "El todo de id {0} no existe",format(id))

    return todo

@bp.route('/<int:id>/updatetest', methods=['GET', 'POST'])
@login_required
def updatetest(id):
    todo = get_todo(id)

    if request.method == 'POST':
        description = request.form['description']
        error = None

        if not description:
            return redirect(url_for('todo.index'))

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'update todo set description = %s'
                ' where id = %s and created_by = %s',
                (description, id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return redirect(url_for('todo.index'))

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    todo = get_todo(id)

    if request.method == 'POST':
        description = request.form['description']
        error = None

        if not description:
            error = "La descripción es requerida."

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'update todo set description = %s'
                ' where id = %s and created_by = %s',
                (description, id, g.user['id'])
            )
            db.commit()
            return redirect(url_for('todo.index'))

    return render_template('todo/update.html', todo=todo)

@bp.route('/<int:id>/delete', methods=['GET'])  
@login_required
def delete(id):
    db, c = get_db()
    c.execute(
        'delete from todo where id = %s and created_by = %s',(id,g.user['id'])
    )
    db.commit()
    return redirect(url_for('todo.index'))

@bp.route('/<int:id>/<int:completed>/check', methods=['GET']) 
@login_required
def check(id, completed):
    print(id, completed)
    db, c = get_db()
    if completed == 1:
        completed = False
    else:
        completed = True
    c.execute(
        'update todo set completed = %s where id = %s and created_by = %s',(completed, id, g.user['id'])
    )
    db.commit()
    return redirect(url_for('todo.index'))
    