from flask_cors import CORS
from typing import Optional
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, send_from_directory, Response
from marshmallow import Schema, fields
from werkzeug.exceptions import HTTPException
import json

app = Flask(__name__)

# Import the json object from the db.json
import json
db = json.load(open('db.json'))
print(db[0])


spec = APISpec(
    title="Conference Voting",
    version="1.0.0",
    openapi_version="3.0.0",
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

@app.route('/')
def show_talks():
    """Fetch all talks
    ---
    get:
            tags:
                -   details
            summary: fetches talks list
            description: Get details of all the beautiful talks submitted by the speakers. 
            parameters: 
              - name: talkLimit
                in: query
                description: Number of talks fetched in a single request
                schema: 
                    type: integer
                    minimum: 20
                    maximum: 50
                    example: 35
            responses:  
                '200':
                    description: It works!
                    content: 
                        application/json: 
                            schema: 
                                type: array
                                items: 
                                    properties:
                                        talk_id: 
                                            type: string
                                            example: pycascades2022-talk01
                                        talk_name: 
                                            type: string 
                                            example: 'Building Elegant API Contracts: From Zero to Hero' 
                                        talk_speaker:
                                            type: string 
                                            example: Neeraj Pandey
                                        talk_pitch: 
                                            type: string
                                            example: Learn how one can write efficient APIs with high-quality API specifications using Open API and RAML specs to create API contracts and achieve a better experience using the API with more reliable unit tests and increased response consistency.

                '404':
                    description: No talk found on this url!
    """
    return jsonify(db)


@app.route("/talk/<id>", methods=['GET'])
def get_talk(id: str):
    """Get talk by talk id
    ---
    get:
        description: Get talk by talk id
        responses:
            200:
                description: Talk found
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                talk_id:
                                    type: string
                                    example: pycascades2022-talk01
                                talk_name: 
                                    type: string 
                                    example: 'Building Elegant API Contracts: From Zero to Hero' 
                                talk_speaker:
                                    type: string 
                                    example: Neeraj Pandey
                                talk_pitch: 
                                    type: string
                                    example: Learn how one can write efficient APIs with high-quality API specifications using Open API and RAML specs to create API contracts and achieve a better experience using the API with more reliable unit tests and increased response consistency.
            '4XX': 
                    description: Talk not found!
                    content:    
                        application/http-problems: {}

    
    """
    try:
        for talk in db:
            print('talk: ', talk)
            if talk['talk_id'] == id:
                return Response(
                    response=json.dumps(talk), 
                    status=201, 
                    mimetype='application/json'
                )
        return Response("Talk not found!", status=404, mimetype='application/json')
    except:
        return Response("Talk not found!", status=404, mimetype='application/json')


@app.route('/api/openapi.json')
def create_openapi_json():
    return jsonify(spec.to_dict())

with app.test_request_context():
    spec.path(view=show_talks)
    spec.path(view=get_talk)
    spec.path(view=create_openapi_json)

if __name__ == "__main__":
    CORS(app)
    app.run(debug=True)

