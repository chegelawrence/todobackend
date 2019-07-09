from todobackend import create_app
from flask import jsonify, request
from todobackend import db
from todobackend.models.models import Todos,TodoSchema

app = create_app()



todo_schema = TodoSchema(strict=True)
todos_schema = TodoSchema(many=True,strict=True)
#return all todos
@app.route('/')
def index():
    todos = Todos.query.all()
    response = todos_schema.dump(todos)

    return jsonify(response.data)

#add new todo
@app.route('/',methods=['POST'])
def addTodo():
    todo_title = str(request.get_json()['title']).title()
    newTodo = Todos(title=todo_title)
    try:
        db.session.add(newTodo)
        db.session.commit()

        response = todo_schema.jsonify(newTodo)
        response.status_code = 201
        return response
    except Exception as e:
        response,status_code = jsonify({'msg':'Internal server error'}),500
        response.status_code = status_code
        return response

#get a single todo
@app.route('/<int:id>')
def singleTodo(id):
    todo = Todos.query.get(int(id))
    if not todo:
       return jsonify({
           'msg':'Resource not found'
       }), 404
    response = todo_schema.jsonify(todo)
    response.status_code = 200
    return response
#update todo completed status
@app.route('/<int:id>',methods=['PUT'])
def updateTodo(id):
    todo = Todos.query.get(id)
    if not todo:
        return jsonify({
            'msg':'Resource not found'
        }), 404
    if todo.completed == 0:
        todo.completed = 1
    else:
        todo.completed = 0
    db.session.commit()
    return todo_schema.jsonify(todo)

#delete todo
@app.route('/<int:id>',methods=['DELETE'])
def deleteTodo(id):
    todo = Todos.query.get(int(id))
    if not todo:
        return jsonify({
            'msg':'Resource not found'
        }), 404
    try:
        db.session.delete(todo)
        db.session.commit()
        return todo_schema.jsonify(todo)
    except Exception as e:
        response = jsonify({'msg':'Internal server error'})
        response.status_code = 500
        return response

if __name__ == '__main__':
    app.run(debug=True,port=9000)