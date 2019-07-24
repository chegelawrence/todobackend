from todobackend import db
from todobackend import ma
from time import ctime

class Todos(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer,nullable=False,primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    date_added = db.Column(db.String(20),nullable=False,default=ctime())
    completed = db.Column(db.Integer,nullable=False,default=0)

    def __repr__(self):
        return f"Todo('{self.id},'{self.title}','{self.completed}','{seld.date_added}')"

class Users(db.Model):
	"""docstring for Users"""
	__tablename__ = 'users'
	id = db.Column(db.Integer,nullable=False,primary_key=True)
	username = db.Column(db.String(50),nullable=False)
	email = db.Column(db.String(100),nullable=False,default='test@test.com')
	password = db.Column(db.String(100),nullable=False)

	def __repr__(self):
		return f"User('{self.id}','{self.username}','{self.email}','{self.password}')"

		

class TodoSchema(ma.Schema):
    class Meta:
        fields = ('id','title','completed','date_added')