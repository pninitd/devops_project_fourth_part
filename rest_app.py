import json

from flask import Flask, request
from werkzeug.exceptions import HTTPException, InternalServerError

from db_connector import get_user_name_by_id, is_id_exist, create_user, update_user_by_id, \
    delete_user_by_id
import os
import signal

app = Flask(__name__)


# http://127.0.0.1:5000/users/<user_id>
@app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def user(user_id):
    if request.method == 'GET':
        try:
            # check if id exist in db
            if is_id_exist(user_id):
                # id exist
                user_name = get_user_name_by_id(user_id)
                if user_name != '':
                    # check no error returned from backend
                    return {'status': 'ok', 'user_name': user_name}, 200
                else:
                    # return {'status': 'error',
                    #         'reason': 'failed to get user' + user_id + ', general error'}, 500
                    return handle_500(user_id)
            else:
                return {'status': 'error', 'reason': 'no such id'}, 500
        except Exception as e:
            # return {'status': 'error',
            #         'reason': 'failed to get user' + user_id + ', general error'}, 500
            return handle_500(user_id)

    elif request.method == 'POST':
        try:
            # getting the json data payload from request
            request_data = request.json
            # treating request_data as a dictionary to get a user_name value from key
            user_name = request_data.get('user_name')
            # check if id already exist in db
            if is_id_exist(user_id):
                return {'status': 'error', 'reason': 'id ' + user_id + ' already exists'}, 500
            else:
                success = create_user(user_id, user_name)
                if success:
                    return {'status': 'ok', 'user_added': user_name}, 201
                else:
                    # return {'status': 'error',
                    #         'reason': 'failed to save' + user_id + ', general error'}, 500
                    return handle_500(user_id)
        except Exception as e:
            # return {'status': 'error',
            #         'reason': 'failed to save' + user_id + ', general error'}, 500
            return handle_500(user_id)

    elif request.method == 'PUT':
        try:
            # getting the json data payload from request
            request_data = request.json
            # treating request_data as a dictionary to get a user_name value from key
            user_name = request_data.get('user_name')
            # check if id exist in db
            if is_id_exist(user_id):
                # id exist
                success = update_user_by_id(user_id, user_name)
                if success:
                    return {'status': 'ok', 'user_updated': user_name}, 200
                else:
                    # return {'status': 'error',
                    #         'reason': 'failed to update user ' + user_id + ', general error'}, 500
                    return handle_500(user_id)
            else:
                return {'status': 'error', 'reason': 'no such id'}, 500
        except Exception as e:
            # return {'status': 'error',
            #         'reason': 'failed to update user ' + user_id + ', general error'}, 500
            return handle_500(user_id)

    elif request.method == 'DELETE':
        try:
            # check if id exist in db
            if is_id_exist(user_id):
                # id exist
                success = delete_user_by_id(user_id)
                if success:
                    return {'status': 'ok', 'user_deleted': user_id}, 200
                else:
                    # return {'status': 'error',
                    #         'reason': 'failed to delete user ' + user_id + ', general error'}, 500
                    return handle_500(user_id)
            else:
                return {'status': 'error', 'reason': 'no such id'}, 500
        except Exception as e:
            # return {'status': 'error',
            #         'reason': 'failed to delete user ' + user_id + ', general error'}, 500
            return handle_500(user_id)


@app.errorhandler(InternalServerError)
def handle_500(e):
    return {'status': 'error', 'reason': 'Internal Server Error '}, 500


# Extra: route error handler for non-existing routes
@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.route('/stop_server')
def stop_server():
    print('Stopping rest app Server')
    try:
        os.kill(os.getpid(), signal.CTRL_C_EVENT)
    except Exception as e:
        os.kill(os.getpid(), signal.SIGKILL)
    finally:
        return 'Rest app Server stopped'


app.run(host='127.0.0.1', debug=True, port=5000)
