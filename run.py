from todobackend import create_app
from flask import jsonify, request
from todobackend import db
from todobackend.models.models import Todos
app = create_app()

#return all todos
@app.route('/')
def index():
    todos = Todos.query.all()
    all_todos = [
        {'id':todo.id,'title':todo.title,'completed':False if todo.completed is 0 else True}\
             for _,todo in enumerate(todos)
    ]
    print(all_todos)
    return jsonify(all_todos)

#add new todo
@app.route('/add/',methods=['POST'])
def addTodo():
    todo_title = str(request.get_json()['title']).title()
    newTodo = Todos(title=todo_title)
    try:
        db.session.add(newTodo)
        db.session.commit()
        todo = Todos.query.filter_by(title=todo_title).first()
        response,status_code = {
            'id':todo.id,
            'title':todo.title,
            'completed':False if todo.completed is 0 else True
        }, 201
        return jsonify(response),status_code
    except Exception as e:
        response,status_code = {'msg':e},500
        return jsonify(response),status_code

#get a single todo
@app.route('/<int:id>')
def singleTodo(id):
    todo = Todos.query.get_or_404(id)
    return jsonify({
        'id':todo.id,'title':todo.title,'completed':False if todo.completed is 0 else True
    }),200

#delete todo
@app.route('/<int:id>',methods=['DELETE'])
def deleteTodo(id):
    todo = Todos.query.get_or_404(id)
    try:
        db.session.delete(todo)
        db.session.commit()
        return jsonify({
            'msg':'Todo deleted'
        }), 200
    except Exception as e:
        return jsonify({'msg':e}),500

if __name__ == '__main__':
    app.run(debug=True,port=9000)