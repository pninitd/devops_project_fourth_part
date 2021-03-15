import requests


def test_docker():
    # test rest app is running from docker
    try:
        res = requests.get('http://0.0.0.0:5000/users/1')
        print('get user: ', res.json())
        assert res.ok
    except requests.exceptions.ConnectionError as e:
        print("Connection refused to rest_app service from docker", e)


if __name__ == "__main__":
    test_docker()
