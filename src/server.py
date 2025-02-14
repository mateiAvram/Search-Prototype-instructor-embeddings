import json

# flask
from flask import Flask, request
from flask_cors import CORS
# from flask_restx import Api, Resource, swagger

# local packages
from models.searchResultItem import SearchResultItem
from business.lanceClient import lanceClient

app = Flask(__name__)
CORS(app)
# api = Api(app, version='1.0', title='Search Assistant API', description='API documentation using Swagger')

def to_json(O: any):
    json_str = json.dumps(O.__dict__)
    json_obj = json.loads(json_str)
    return json_obj

# @app.route('/swagger-ui/')
# def swagger_ui():
#     return swagger.ui(api)

# @app.route('/')
# class HelloWorld(Resource):
#     def get(self):
#         # item1 = to_json(SearchResultItem(1, "hello"))
#         # item2 = to_json(SearchResultItem(2, "world"))
#         # list = [item1, item2]
#         # return list
#         return {'message': 'Hello, World!'}

@app.route('/', methods = ['GET'])
def hello_world():
    item1 = to_json(SearchResultItem(1, "hello"))
    item2 = to_json(SearchResultItem(2, "world"))
    list = [item1, item2]
    return list

@app.route('/search', methods = ['GET'])
def search():
    query = request.args.get('query')

    client = lanceClient()
    results = client.search(query)

    print(results[0])

    return_list = []

    count = 0
    for result in results:
        return_list.append(to_json(SearchResultItem(str(count), result.metadata['url'])))
        count += 1

    return return_list
    # return []

if __name__ == '__main__':
    app.run()
