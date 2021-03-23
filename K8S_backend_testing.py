import requests


def geturl():
    url = ''
    try:
        with open('k8s_url.txt', 'r', encoding='utf-8') as file:
            url = file.read()
            print(url)
    except IOError as e:
        print("Could not read the file:", e)
    finally:
        file.close()
        return url


# test rest app is running from k8s
def test_k8s():
    try:
        # receive the k8s url from k8s_url.txt
        url = geturl()
        if url is None or url == '':
            url = 'http://host.docker.internal:5000'
        res = requests.get(url + '/users/1')
        print('get user: ', res.json())
    except requests.exceptions.ConnectionError as e:
        print("Connection refused to rest_app service from docker", e)
    finally:
        assert res.ok


if __name__ == "__main__":
    test_k8s()
