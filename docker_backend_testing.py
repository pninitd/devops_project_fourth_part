import requests

def test_docker():
    # test rest app is running from docker
    try:
        res = requests.get('http://localhost:5000/users/1')
        print('get user: ', res.json())
    except requests.exceptions.ConnectionError as e:
        print("Connection refused to rest_app service from docker", e)
    finally:
        assert res.ok


if __name__ == "__main__":
    test_docker()
