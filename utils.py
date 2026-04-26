import pickle

def serialize_data(data):
    return pickle.dumps(data)

def deserialize_data(data):
    return pickle.loads(data)

def format_date(timestamp):
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')
