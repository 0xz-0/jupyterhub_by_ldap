import ldap
import os
# from typing import Tuple


class SelfLdap(object):

    _connection = None
    _connection_bound = False

    def __init__(self) -> None:
        self.AUTH_LDAP_SERVER_URI = os.environ.get('AUTH_LDAP_SERVER_URI').strip("'").strip('"')
        self.AUTH_LDAP_BASE_DN = os.environ.get('AUTH_LDAP_BASE_DN').strip("'").strip('"')
        self.AUTH_LDAP_BIND_DN = os.environ.get('AUTH_LDAP_BIND_DN').strip("'").strip('"')
        self.AUTH_LDAP_BIND_PASSWORD = os.environ.get('AUTH_LDAP_BIND_PASSWORD').strip("'").strip('"')

    @property
    def connection(self):
        if not self._connection_bound:
            self._bind()
        return self._get_connection()

    def _bind(self):
        if not self.AUTH_LDAP_SERVER_URI:
            raise ValueError("Lack Env Var AUTH_LDAP_SERVER_URI")
        if not self.AUTH_LDAP_BIND_PASSWORD:
            raise ValueError("Lack Env Var AUTH_LDAP_BIND_PASSWORD")
        self._bind_as(self.AUTH_LDAP_BIND_DN,self.AUTH_LDAP_BIND_PASSWORD, True)

    def _bind_as(self, bind_dn, bind_password, sticky=False):
        _1, _2, _3, _4 = self._get_connection().simple_bind_s(bind_dn, bind_password)
        # if success,return (97,[],1,[]);else raise error INVALID_CREDENTIALS
        # but when pwd is None | "" , it isn't truth yet
        self._connection_bound = sticky

    def _get_connection(self):
        if not self._connection:
            self._connection = ldap.initialize(self.AUTH_LDAP_SERVER_URI)
            # self._connection.protocol_version = ldap.VERSION3
        return self._connection

    def _authenticate_user_dn(self, username: str, password: str) -> bool:
        bind_dn = 'cn=%s,%s' % (username, self.AUTH_LDAP_BASE_DN)
        try:
            self._bind_as(bind_dn, password, False)
            return True
        except ldap.INVALID_CREDENTIALS:
            return False

    def authenticate(self, username: str, password: str) -> dict:
        username = username.strip()
        password = password.strip()
        if not username:
            raise ValueError("UserName Is Lacked!")
        if not password:
            raise ValueError("PassWord Is Lacked!")

        # result_type == ldap.RES_SEARCH_ENTRY
        _, result_data = self.connection.result(
            self.connection.search(
                self.AUTH_LDAP_BASE_DN,
                ldap.SCOPE_SUBTREE,
                f"sAMAccountName={username}"
            )
        )
        if len(result_data) == 0:
            raise ValueError(f"UserName=[{username}] isn`t existed!")
        else:
            judge = self._authenticate_user_dn(username, password)
            if not judge:
                raise ValueError(f"Password isn't correct!")

            # todo ; when return more than 1
            # result_data[0] is tuple which length is equal 2
            data = result_data[0][1]
            ret = dict(
                username=username,
                password=password,
                uid=data['uidNumber'][0].decode(),
            )
        return ret
