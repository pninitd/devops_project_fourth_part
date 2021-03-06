import requests


def clean_test_user():
    # Delete test user from the automation
    try:
        requests.delete('http://localhost:5000/users/666')
        print("cleaned automation user")
    except requests.exceptions.ConnectionError as e:
        print("Connection refused to rest_app service", e)


def clean_specific_user(id):
    # Delete specific user from the automation
    try:
        requests.delete('http://localhost:5000/users/%s' % id)
        print("cleaned user %s" % id)
    except requests.exceptions.ConnectionError as e:
        print("Connection refused to rest_app service", e)


def stop_rest_app():
    # Stop rest app service
    try:
        requests.get('http://localhost:5000/stop_server')
    except requests.exceptions.ConnectionError as e:
        print("Connection refused to rest_app service", e)


if __name__ == "__main__":
    clean_test_user()
    stop_rest_app()
