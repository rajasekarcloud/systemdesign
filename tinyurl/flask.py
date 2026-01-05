from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import time
import botocore.session
from amazondax.AmazonDaxClient import AmazonDaxClient

app = Flask(__name__)
CORS(app)

dax_endpoint = 'daxs://urlmappingscache.vojjn0.dax-clusters.us-east-1.amazonaws.com'
dax_client= AmazonDaxClient.resource(endpoint_url=dax_endpoint, region_name='us-east-1') 
dax = dax_client.Table('URLMappings')

dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb_resource.Table('URLMappings')

def generate_short_key():
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route('/')
def home():
    return jsonify({"message": "URL Shortener API is running!"})

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "healthy"}), 200

# Create short URL with TTL
@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get('long_url')
    ttl_seconds = data.get('ttl_seconds', 86400)  # Default: 1 day (86400s)

    if not long_url:
        return jsonify({'error': 'URL is required'}), 400

    shortKey = generate_short_key()
    expire_at = int(time.time()) + ttl_seconds  # Compute TTL timestamp

    table.put_item(TableName='URLMappings', Item={
        'shortKey': shortKey,
        'long_url': long_url,
        'expireAt': str(expire_at)  # TTL field
    })

    short_url = f"http://short.url/{shortKey}"
    return jsonify({'short_url': short_url})

# Fetch long URL by short key
@app.route('/fetch_url/<shortKey>', methods=['GET'])
def fetch_url(shortKey):
    response = dax.get_item(TableName='URLMappings', Key={'shortKey': shortKey})
    item = response.get('Item')

    return jsonify({'long_url': item['long_url']})

# Delete a short URL
@app.route('/delete_url/<shortKey>', methods=['DELETE'])
def delete_url(shortKey):
    response = table.get_item(TableName='URLMappings', Key={'shortKey': shortKey})
    if 'Item' not in response:
        return jsonify({'error': 'Short URL not found'}), 404

    table.delete_item(TableName='URLMappings', Key={'shortKey': shortKey})

    return jsonify({'message': 'Short URL deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

