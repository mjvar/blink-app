from .extensions import db

class Eye_Data(db.Model):
    __tablename__ = 'eye_data_entries'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(80))
    score = db.Column(db.Float())

    def __init__(self, timestamp, score):
        self.timestamp = timestamp
        self.score = score

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'timestamp': self.timestamp,
            'score': self.score
        }

class Face_Data(db.Model):
    __tablename__ = 'face_data_entries'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(80))

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id, 
            'timestamp': self.timestamp
        }