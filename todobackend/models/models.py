from todobackend import db

class Todos(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer,nullable=False,primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    completed = db.Column(db.Integer,nullable=False,default=0)

    def __repr__(self):
        return f"Todo('{self.id},'{self.title}','{self.completed}')"