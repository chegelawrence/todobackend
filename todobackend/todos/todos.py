from flask import jsonify,request,Blueprint
from todobackend import db,blacklist,jwt
from todobackend.models.models import Todos,TodoSchema,Users
from time import ctime
from flask_jwt_extended import jwt_required,get_jwt_identity

todos_blueprint = Blueprint('todos_blueprint',__name__)

todo_schema = TodoSchema(strict=True)
todos_schema = TodoSchema(many=True,strict=True)

#Returns true if access token has 
#been blacklisted otherwise false
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

#return all todos
@todos_blueprint.route('/todos')
@jwt_required
def todos():
    todos = Todos.query.all()
    response = todos_schema.dump(todos)

    return jsonify(response.data)

#add new todo
@todos_blueprint.route('/todos',methods=['POST'])
@jwt_required
def addTodo():
    todo_title = request.json.get('title',None)
    if not todo_title:
        return jsonify({'error':{'msg':'missing title in request'}}),400

    newTodo = Todos(title=todo_title.title())
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
@todos_blueprint.route('/todos/<int:id>')
@jwt_required
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
@todos_blueprint.route('/todos/<int:id>',methods=['PUT'])
@jwt_required
def updateTodo(id):
    todo = Todos.query.get(int(id))
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
@todos_blueprint.route('/todos/<int:id>',methods=['DELETE'])
@jwt_required
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
        response = jsonify({'msg':'Internal server error','status_code':500})
        return response