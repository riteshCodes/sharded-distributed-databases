from flask import Flask, render_template, redirect, url_for
from flask_wtf import Form, FlaskForm
from wtforms import IntegerField, SubmitField, TextAreaField, StringField
import redis, json
from wtforms.validators import DataRequired

# config system
app = Flask(__name__)
# Flask-WTF requires an encryption key - the string can be anything
app.config.update(dict(SECRET_KEY='mysecretkey'))
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# set auto-generated key
if not r.exists('id'):
    r.set('id', '0')



class CreateTask(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
"""

class CreateTask(Form):
    title = TextAreaField('Task Title')
    short_desc = TextAreaField('Short Description')
    priority = IntegerField('Priority')
    create = SubmitField('Create')


class DeleteTask(Form):
    key = TextAreaField('Task Key')
    title = TextAreaField('Task Title')
    delete = SubmitField('Delete')


class UpdateTask(Form):
    key = TextAreaField('Task Key')
    title = TextAreaField('Task Title')
    short_desc = TextAreaField('Short Description')
    priority = IntegerField('Priority')
    update = SubmitField('Update')


class ResetTask(Form):
    reset = SubmitField('Reset')


def create_task(form):
    title = form.title.data
    priority = form.priority.data
    short_desc = form
    task = {'title': title, 'short_desc': short_desc, 'priority': priority}

    # set auto-generated key
    r.hset('T' + str(r.get('id')), task)
    r.incr('id')
    return redirect('/')


def deleteTask(form):
    key = form.key.data
    title = form.title.data
    if (key):
        r.delete(key)
    else:
        for i in r.keys():
            if i != 'id' and r.hget(i, 'title') == title:
                print(i)
                r.delete(i)
    return redirect('/')


def updateTask(form):
    title = form.title.data
    priority = form.priority.data
    key = form.key.data
    short_desc = form.shortdesc.data
    task = {'title': title, 'shortdesc': short_desc, 'priority': priority}

    # update by "reset"
    if (r.exists(key)):
        r.hset(key, task)
    return redirect('/')


def resetTask(form):
    r.flushall()
    r.set('id', '0')
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def main():
    # create form
    cform = CreateTask(prefix='cform')
    dform = DeleteTask(prefix='dform')
    uform = UpdateTask(prefix='uform')
    reset = ResetTask(prefix='reset')

    # response
   if cform.create.data:
       return createTask(cform)
   # if dform.validate_on_submit() and dform.delete.data:
       # return deleteTask(dform)
    #if uform.validate_on_submit() and uform.update.data:
      #  return updateTask(uform)
    #if reset.validate_on_submit() and reset.reset.data:
     #   return resetTask(reset)

    # get all data
    keys = r.keys()
    val = {}
    for i in keys:
        if i != 'id':
            val[i] = r.hgetall(i)

    return render_template('home.html', cform=cform, dform=dform, uform=uform, keys=keys, val=val, reset=reset)


if __name__ == '__main__':
    app.run(debug=True)


    """

