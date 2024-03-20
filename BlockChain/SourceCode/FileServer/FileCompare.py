import hashlib


def print_file():
    li = [b"hello", b" world"]

    print(hashlib.blake2b(b"hello world").hexdigest())
    h = hashlib.blake2b()
    for i in li:
        h.update(i)
    print(h.hexdigest())


def file_compare(url1, url2):
    try:
        if file_trans(url1) == file_trans(url2):
            print("These two files are the same !")
            return True
        else:
            print("The two files are different !")
            return False
    except FileNotFoundError:
        print('No find your file !')
    except FileExistsError:
        print('file have exception !')
    finally:
        print('Conversion success !')


def file_trans(url):
    try:
        f = open(url, 'rb')
        stb = f.read()
        h = hashlib.blake2b()
        for st in stb:
            h.update(bytes(st))
        print(url.split('/')[-1] + " hash value is :" + h.hexdigest())
        return h.hexdigest()
    except FileNotFoundError:
        print("No find your file !")
    except FileExistsError:
        print("file have exception")


if __name__ == '__main__':
    # test
    url1 = "D:/MyPhone/1.jpg"
    url2 = "D:/MyPhone/2.jpg"
    file_compare(url1, url2)
