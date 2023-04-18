import unittest

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv('.env'))

from auth.self_ldap import SelfLdap
from auth.user import UserAuth


class TestLdap(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.ldap_cls = SelfLdap()

    def test_conn(self):
        # ldap.ldapobject.SimpleLDAPObject object
        print(self.ldap_cls.connection)

    def test_user(self):
        """
            * ldap user test
        """
        username = ""
        password = ""
        uid = ""

        result = self.ldap_cls.authenticate(username, password)
        self.assertEqual(result['uid'], uid)
        pass

class TestUserAuth(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.user_cls = UserAuth()

    def test_auth(self):
        """
            * user list test
        """

        username = "admin"
        password = "123456"

        result = self.user_cls.authenticate(username, password)
        self.assertEqual(result.get('uid'), "65534")


if __name__ == '__main__':
    unittest.main()
