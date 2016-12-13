import os
import logging
import numpy as np
from app import app #, db
from flask import request, abort, jsonify, make_response
from flask import render_template, send_from_directory
#from flask_sqlalchemy import SQLAlchemy, DeclarativeMeta
from flask.ext.sqlalchemy import SQLAlchemy, DeclarativeMeta
from json import JSONEncoder

log = logging.getLogger(__name__)

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

import socket
import pickle


#from .models import Metadata #???

class ProductJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            return obj.to_dict()
        return super(ProductJSONEncoder, self).default(obj)


app.json_encoder = ProductJSONEncoder

user = 'postgres'
password = 'cs207mima'
host = 'localhost'
port = '5432'
dbname = 'timeseries'
url = 'postgresql://{}:{}@{}:{}/{}'
# Posgres url
postgres_url = url.format(user, password, host, port, dbname)
# SQlite uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/metadata.db'#postgres_url#???
db = SQLAlchemy(app)


class Metadata(db.Model):
    __tablename__='metadata'

    id = db.Column(db.Integer, primary_key=True)
    mean = db.Column(db.Float)
    std = db.Column(db.Float)#nullable=Flase
    blarg = db.Column(db.Float)
    level = db.Column(db.String(1))
    #fpath = db.Column(db.String(80), nullable=False)???

    def __repr__(self):
        return '<id %r>' % (self.id)

    def to_dict(self):
        return dict(id=self.id, 
                    blarg=self.blarg, 
                    level=self.level, 
                    mean=self.mean, 
                    std=self.std)#, 
                    #fpath=self.fpath)



#socket???
def connectRBTree():
    port = 12341
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, port))
    return s

def connectSM():
    port = 12340 
    s = socket.socket()
    host = socket.gethostname() 
    s.connect((host, port))
    return s

@app.route('/')
@app.route('/index')
def index():
    #return "Hello, World!"
    log.info('Getting Home html')
    return send_from_directory('static', os.path.join('html', 'home.html'))
    #user = {'nickname': 'Miguel'}  # fake user
    #posts = [  # fake array of posts
    #    { 
    #        'author': {'nickname': 'Mary'}, 
    #        'body': 'Beautiful day in Portland!' 
    #    },
    #    { 
    #        'author': {'nickname': 'Susan'}, 
    #        'body': 'The Avengers movie was so cool!' 
    #    }
    #]
    #return render_template('index.html',
    #                       title='Home',
    #                       user=user,
    #                       posts=posts)


@app.route('/timeseries', methods=['GET'])
def get_metadata_range():

    if 'mean_in' in request.args:
        mean_in = request.args.get('mean_in')
        mean_range = mean_in.split('-')
        m_min = float(mean_range[0])
        m_max = float(mean_range[1])
        query = Metadata.query.filter(Metadata.mean>=m_min & Metadata.mean<=m_max).all()
        log.info('Get timeseries whose mean is in the range')
        return jsonify(dict(metadata=query))

    if 'level_in' in request.args:
        level_in = request.args.get('level_in')
        level_range = level_in.split(',')
        query = Metadata.query.filter(Metadata.level.in_(level_in)).all()
        log.info('Get timeseries whose level is in the range')
        return jsonify(dict(metadata=query))

    if 'level' in request.args:
        level = request.args.get('level')
        query = Metadata.query.filter_by(level=level).all()
        log.info('Get timeseries whose level is queried')
        return jsonify(dict(metadata=query))

    log.info('Getting all metadata')
    return jsonify(dict(metadata=Metadata.query.all())) #tasks???



@app.route('/timeseries', methods=['POST'])
def create_ts():
    if not request.json:
        abort(400)
    log.info('Creating timeseries entries in metadata')

    
    data = request.get_json(force=True)
    data['cmd'] = "ADDTS"
    s = connectSM()
    try:
        # Send POST request to server
        s.send(pickle.dumps(data))
        response = pickle.loads(s.recv(1024))

        # Add metadata to db
        ts = db.session.query(Metadata).filter_by(id=data['id']).first()
        print("timeseries=",ts)
        #if the timeseries id is in the Medadata base
        if ts:
            print("timeseries exists, updating...")
            ts.mean = np.mean(data['value'])
            ts.std = np.std(data['value'])
        else:
            print("timeseries does not exist, updating...")
            ts = Metadata(id=data['id'],
                          blarg=np.random.choice([0,1]),
                          level=np.random.choice(['A','B','C','D','E','F']),
                          mean=np.mean(data['value']),
                          std=np.std(data['value']))

        db.session.add(ts)
        db.session.commit()

    finally:
        s.close()
        return json.dumps(response)

    db.session.add(prod)
    db.session.commit()
    return jsonify({'op': 'OK', 'task': prod}), 201




@app.route('/timeseries/<ts_id>', methods=['GET'])
def get_timeseries_by_id(id):
    #send back metdata
    query = Metadata.query.filter_by(id=ts_id).first()
    if query is None:
        log.info('Failed to get metadata with ID=%s', ts_id)
        abort(404)
    log.info('Get metadata with ID=%s', ts_id)

    #send back timeseries in a JSON payload
    #socket part??? 
    s = connectSM()
    try:
        toSend = {"cmd":"BYID","id":id} # A = get timeseries by id, B = get all timeseries etc
        s.send(pickle.dumps(toSend))
        rec = s.recv(8192)
        rec = pickle.loads(rec)
        return jsonify({'metadata':query, 'timeseries': rec})

    finally:
        s.close()



#should take a id=the_id querystring and use that as an id into the database to 
#find the timeseries that are similar, sending back the ids of (say) the top 5.
@app.route('/simquery', methods=['GET'])
def get_simts_by_id():
    return 'hello worlds'
    if 'id' in request.args:
        ts_id = request.args.get('id')
        #default n is 5
        n = 5
        #socket???
        s = connectRBTree()
        try:
            while True: #???
                toSend = {"cmd":"SIMID", "id":sim_id, "n":n}
                s.send(pickle.dumps(toSend))
                rec = s.recv(1024)
                # TODO data MORE THAN 1024, protocol?
                rec = pickle.loads(rec)
                return jsonify({"similar_points": rec}) 

        finally:
            s.close()

#take a timeseries as an input in a JSON, carry out the query, 
#and return the appropriate ids as well. This is an unusual use of POST.
@app.route('/simquery', methods=['POST'])
def simquery_post():
    return 'hello'
    data = request.get_json(force=True)
    data['cmd'] = "SIMTS"
    s = connectRBTree()
    try:
        s.send(pickle.dumps(data))
        response = pickle.loads(s.recv(1024))
        return jsonify({"response": response})

    finally:
        s.close()
        #return 
    
    
db.create_all()

