from datetime import datetime
import hashlib


class Auth():
    def __init__(self):
        pass

    def generate_hash(self, input):
        hash = hashlib.sha256()
        hash.update(input.encode("utf-8"))
        return hash.hexdigest()

    def generate_token(self, username):
        current_date = int(datetime.now().timestamp())
        return self.generate_hash(str(current_date) + username)

    def verify_token(self, token, expiration_date):
        return datetime.now() <= expiration_date


if __name__ == "__main__":
    auth = Auth()
    print(auth.generate_token("synnek"))
