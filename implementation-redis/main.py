from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
import redis
from wtforms.validators import DataRequired

# config system
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='mysecretkey'))
db = redis.StrictRedis(host='localhost', port=6379, db=0)

# set auto-generated key
if not db.exists('id'):
    db.set('id', '0')


class CreateTask(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired()])
    shortdesc = StringField('Short Description', validators=[DataRequired()])
    priority = IntegerField('Priority', validators=[DataRequired()])
    create = SubmitField('Create')


class DeleteTask(FlaskForm):
    key = StringField('Task Key')
    title = StringField('Task Title')
    delete = SubmitField('Delete')


class UpdateTask(FlaskForm):
    key = StringField('Task Key', validators=[DataRequired()])
    title = StringField('Task Title', validators=[DataRequired()])
    shortdesc = StringField('Short Description', validators=[DataRequired()])
    priority = IntegerField('Priority', validators=[DataRequired()])
    update = SubmitField('Update')


class ResetTask(FlaskForm):
    reset = SubmitField('Reset')


def createTask(form):
    title = form.title.data
    priority = form.priority.data
    shortdesc = form.shortdesc.data
    task = {'title': title, 'shortdesc': shortdesc, 'priority': priority}

    # set auto-generated key
    task_id = "Task_" + db.get('id').decode('UTF-8')
    db.hset(task_id, mapping=task)
    db.incr('id')  # Increment the index

    return redirect('/')


def deleteTask(form):
    key = form.key.data
    title = form.title.data

    if key:
        db.delete(key)
    else:
        for i in db.keys():
            if i != 'id' and db.hget(i, 'title') == title:
                print(i)
                db.delete(i)

    return redirect('/')


def updateTask(form):
    title = form.title.data
    priority = form.priority.data
    key = form.key.data
    shortdesc = form.shortdesc.data
    task = {'title': title, 'shortdesc': shortdesc, 'priority': priority}

    # update by "reset"
    if db.exists(key):
        db.hset(key, task)

    return redirect('/')


def resetTask(form):
    db.flushall()
    db.set('id', '0')
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def main():
    # create form
    cform = CreateTask(prefix='cform')
    dform = DeleteTask(prefix='dform')
    uform = UpdateTask(prefix='uform')
    reset = ResetTask(prefix='reset')

    # response
    if cform.validate_on_submit() and cform.create.data:
        return createTask(cform)
    if dform.validate_on_submit() and dform.delete.data:
        return deleteTask(dform)
    if uform.validate_on_submit() and uform.update.data:
        return updateTask(uform)
    if reset.validate_on_submit() and reset.reset.data:
        return resetTask(reset)

    # get all data
    keys = db.keys()
    val = {}
    for i in keys:
        if i != 'id':
            val[i] = 'TEST'
    return render_template('home.html', cform=cform, dform=dform, uform=uform,
                           keys=keys, val=val, reset=reset)


if __name__ == '__main__':
    app.run(debug=True)
