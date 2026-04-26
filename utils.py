import json

def serialize_data(data):
    return json.dumps(data).encode('utf-8')

def deserialize_data(data):
    return json.loads(data.decode('utf-8'))

def format_date(timestamp):
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')
