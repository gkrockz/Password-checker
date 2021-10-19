import requests
import hashlib
import sys

def fetch_data(head):
  url = 'https://api.pwnedpasswords.com/range/' + head
  response = requests.get(url)
  if response.status_code != 200:
    raise RuntimeError(f'Error fetching: {response.status_code}, check the api and try again')
  return response

def decode_response(hashes, hash_to_check):
  hashes = (line.split(':') for line in hashes.text.splitlines())
  for hash, count in hashes:
    if hash == hash_to_check:
      return count
  return 0

def is_pwned(password):
  sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
  first5_chars, tail = sha1password[:5], sha1password[5:]
  response = fetch_data(first5_chars)
  return decode_response(response, tail)
  

def main(args):
  for password in args:
    count = is_pwned(password)
    if count:
      print(f'{password} was found {count} times... you should probably change your password!')
    else:
      print(f"{password} was NOT found. Good to go !" )
  return 'Process Completed !'

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))