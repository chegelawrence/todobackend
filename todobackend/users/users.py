from flask import request,jsonify,Blueprint
from todobackend import db,blacklist
from todobackend.models.models import Users
from flask_jwt_extended import create_access_token,jwt_required,get_raw_jwt
from werkzeug.security import generate_password_hash,check_password_hash
import datetime

users_blueprint = Blueprint('users_blueprint',__name__)


@users_blueprint.route('/',methods=['POST'])
def login():
	'''users login endpoint'''
	if not request.is_json:
		return jsonify({
			'error':{'msg':'Bad request'}
			}), 400
	username = request.json.get('username',None)
	password = request.json.get('password',None)
	if not username:
		return jsonify({'error':{'msg':'No username in request'}}),400
	if not password:
		return jsonify({'error':{'msg':'No password in request'}}),400

	user = Users.query.filter_by(email=username.lower()).first()
	if not user:
		return jsonify({'error':{'msg':'Not authorized'}}),401
	if check_password_hash(user.password,password):
		#correct password, create access token and return
		access_token = create_access_token(identity={'id':user.id,'username':user.username,'email':user.email},expires_delta=datetime.timedelta(days=2))
		return jsonify({'access_token':access_token,'logged_in':True})
	else:
		return jsonify({'error':{'msg':'Wrong password'}}),401


@users_blueprint.route('/register',methods=['POST'])
def register():
	'''create user account endpoint'''
	if not request.is_json:
		return jsonify({'error':{'msg':'Bad request'}}),400
	username = request.json.get('username',None)
	email = request.json.get('email',None)
	password = request.json.get('password',None)
	confirm_password = request.json.get('confirm_password',None)
	if not username:
		return jsonify({'error':{'msg':'No username in request'}}),400
	if not email:
		return jsonify({'error':{'msg':'No email in request'}}),400
	if not password:
		return jsonify({'error':{'msg':'No password in request'}}),400
	if not confirm_password:
		return jsonify({'error':{'msg':'No confirm_password field in request'}}),400

	if password == confirm_password:
		password_hash = generate_password_hash(password)
		user = Users(username=username.capitalize(),email=email.lower(),password=password_hash)
		#add user to db
		db.session.add(user)
		#commit changes to the database
		db.session.commit()
		return jsonify({'success':{'msg':'Account creation successful'}}), 201
	else:
		return jsonify({'error':{'msg':'Passwords do not match'}}),401

@users_blueprint.route('/logout')
@jwt_required
def logout():
	jti = get_raw_jwt()['jti']
	blacklist.add(jti)
	return jsonify({'success':{'msg':'Successfully logged out'}})

