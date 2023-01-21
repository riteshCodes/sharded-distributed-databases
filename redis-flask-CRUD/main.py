from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
import redis
from wtforms.validators import DataRequired

# config system
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='my_secret_key'))
db = redis.StrictRedis(host='localhost', port=6379, db=0)
# @param: Redis by default consists of 16 logical databases. Starting from 0 index and ending with 15.
# redis_cli = redis.Redis(host="localhost", port=16379, decode_responses=True, encoding="utf-8")

# set auto-generated key (Initialization)
if not db.exists('id'):
    db.set('id', '0')


class CreateTask(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired()])
    short_description = StringField('Short Description', validators=[DataRequired()])
    priority = IntegerField('Priority', validators=[DataRequired()])
    create = SubmitField('Create')


class DeleteTask(FlaskForm):
    key = StringField('Task Key')
    title = StringField('Task Title')
    delete = SubmitField('Delete')


class UpdateTask(FlaskForm):
    key = StringField('Task Key', validators=[DataRequired()])
    title = StringField('Task Title', validators=[DataRequired()])
    short_description = StringField('Short Description', validators=[DataRequired()])
    priority = IntegerField('Priority', validators=[DataRequired()])
    update = SubmitField('Update')


class ResetTask(FlaskForm):
    reset = SubmitField('Reset')


class CreateMultipleTasks(FlaskForm):
    title_first = StringField('First Task Title', validators=[DataRequired()])
    short_description_first = StringField('Short Description', validators=[DataRequired()])
    priority_first = IntegerField('Priority', validators=[DataRequired()])

    title_second = StringField('Second Task Title', validators=[DataRequired()])
    short_description_second = StringField('Short Description', validators=[DataRequired()])
    priority_second = IntegerField('Priority', validators=[DataRequired()])

    create = SubmitField('Create two tasks')


def create_task(form):
    title = form.title.data
    priority = form.priority.data
    short_description = form.short_description.data
    task = {'title': title, 'short_description': short_description, 'priority': priority}

    # set auto-generated key
    task_id = "Task_" + db.get('id').decode('UTF-8')
    db.hset(task_id, mapping=task)
    db.incr('id')  # Increment the index after adding the task

    return redirect('/')


def delete_task(form):
    key = form.key.data
    title = form.title.data

    if key:
        db.delete(key)
    else:
        for i in db.keys():
            if i.decode('UTF-8') != 'id' and db.hget(i, 'title').decode('UTF-8') == title:
                print(i)
                db.delete(i)

    return redirect('/')


def update_task(form):
    title = form.title.data
    priority = form.priority.data
    key = form.key.data
    short_description = form.short_description.data
    task = {'title': title, 'short_description': short_description, 'priority': priority}

    # update by "reset"
    print("This key")
    print(key)
    if db.exists(key):
        db.hset(key, mapping=task)
    print(db.hgetall(key))
    return redirect('/')


def reset_task(form):
    db.flushall()
    db.set('id', '0')
    return redirect('/')


def create_m_task(form):
    title_first = form.title_first.data
    priority_first = form.priority_first.data
    short_description_first = form.short_description_first.data
    task_first = {'title': title_first, 'short_description': short_description_first, 'priority': priority_first}

    title_second = form.title_second.data
    priority_second = form.priority_second.data
    short_description_second = form.short_description_second.data
    task_second = {'title': title_second, 'short_description': short_description_second, 'priority': priority_second}

    # set auto-generated key
    first_task_id = "Task_" + db.get('id').decode('UTF-8')
    db.incr('id')    # Increment the index after adding the task
    second_task_id = "Task_" + db.get('id').decode('UTF-8')

    pipe = db.pipeline()
    pipe.hset(first_task_id, mapping=task_first)
    pipe.hset(second_task_id, mapping=task_second)

    pipe.execute()

    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def main():
    # create form
    cform = CreateTask(prefix='cform')
    dform = DeleteTask(prefix='dform')
    uform = UpdateTask(prefix='uform')
    reset = ResetTask(prefix='reset')

    m_form = CreateMultipleTasks(prefix="m_form")

    # response
    if cform.validate_on_submit() and cform.create.data:
        return create_task(cform)
    if dform.validate_on_submit() and dform.delete.data:
        return delete_task(dform)
    if uform.validate_on_submit() and uform.update.data:
        return update_task(uform)
    if reset.validate_on_submit() and reset.reset.data:
        return reset_task(reset)

    if m_form.validate_on_submit() and m_form.create.data:
        return create_m_task(m_form)

    # get all data
    keys = db.keys()
    val = {}
    for i in keys:
        print(i.decode('UTF-8'))
        if i.decode('UTF-8') != 'id':
            val[i.decode('UTF-8')] = {k.decode("utf-8"): v.decode("utf-8") for k, v in
                                      db.hgetall(i.decode('UTF-8')).items()}
            print(val[i.decode('UTF-8')])

    return render_template('home.html', cform=cform, dform=dform, uform=uform, m_form=m_form,
                           keys=keys, val=val, reset=reset)


if __name__ == '__main__':
    app.run(debug=True)
