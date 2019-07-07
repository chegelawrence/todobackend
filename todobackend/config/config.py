import os

class Config:
    '''Contains the app configuratioon variables'''
    SECRET_KEY = '4d82decffec68c1bb5a96f5e36ffd0ff184fb684b72b661366a30563832cd533'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + '/home/lawz/Desktop/todobackend/todos.sqlite'