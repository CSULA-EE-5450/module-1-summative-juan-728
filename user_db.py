from typing import Tuple, Dict
import secrets
import nacl.pwhash


class UserDB(object):
    def __init__(self):
        self._accounts: Dict[str, bytes] = {}

    def create_user(self, username: str) -> Tuple[str, str]:
        """
        Creates a user and returns a automatically-generated token (password)
        for the user.  You can generate this token using secrets.token_urlsafe()

        :raises: ValueError if the username already exists
        :param username: desired username
        :return: (username, password_token)
        """

        if username == self._accounts:
            raise ValueError("Username already exist")

        passtoken = (secrets.token_urlsafe())
        passtoken_byte = str.encode(passtoken)
        self._accounts[username] = nacl.pwhash.str(passtoken_byte)

        return username, passtoken
        pass

    def is_valid(self, username: str, password) -> bool:
        """
        Check whether the given username and password match a user
        present in the UserDB.  The hash of the input password is
        compared to the stored hash.

        See what you can call in nacl.pwhash to verify an input password.

        :param username:
        :param password:
        :return: True if the credentials are valid, False if not.
        """
        password_bytes = str.encode(password)

        try:
            if username in self._accounts.keys() and nacl.pwhash.verify(self._accounts[username], password_bytes):
                return True
        except:
            return False
        pass