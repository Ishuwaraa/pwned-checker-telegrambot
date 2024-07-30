import requests
import hashlib
# import sys


def request_api_data(hashed_pass):
    try:
        url = 'https://api.pwnedpasswords.com/range/' + hashed_pass
        res = requests.get(url)
        if res.status_code != 200:
            raise RuntimeError(f'Error fetching: {res.status_code}')
        return res.text
    except requests.RequestException as err:
        return err
    except Exception as err:
        return err


def pwned_check(pw):
    # encoding is necessary. hashlib will return an object. hexdigest() will convert it to a readable hexadecimal
    hashed = hashlib.sha1(pw.encode('utf-8')).hexdigest().upper()   # .upper cuz the api takes capitals
    # api takes only the first 5 chars due to k-anonymity
    # then returns the suffixes that match the prefix hashed we sent
    res = request_api_data(hashed[:5])
    # split lines without the line break. default is false
    hashed_list = res.splitlines()
    not_secure_count = 0
    for item in hashed_list:
        hashed_suffix, pwned_count = item.split(':')[0], item.split(':')[1]
        if hashed_suffix == hashed[5:]:
            not_secure_count += 1
            return f'Change your password. Your password, "{pw}" has been pwned {pwned_count} times.'

    if not not_secure_count:
        return f'All good to go. Your password, "{pw}" is secure.'


# def main(passwords):
#     for item in passwords:
#         pwned_check(item)
#     return 'Done!'


# making sure file doesn't run if imported elsewhere
# if __name__ == '__main__':
#     sys.exit(main(sys.argv[1:]))    # .exit() used in case the process doesn't end
