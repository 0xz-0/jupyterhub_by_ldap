from copy import deepcopy

class UserAuth(object):
    def __init__(self) -> None:
        pass

    def _get_users(self) -> list:
        """
            * user list. avoid use root!!!
            * todo: get from file like user.conf
        """
        return [
            dict(username='admin', password='123456', uid='65530')
        ]

    @property
    def user_dict(self) -> dict:
        user_list = self._get_users()
        ret = dict()
        for v in user_list:
            if ret.get(v['username']) is None:
                ret[v['username']] = deepcopy(v)
            else:
                raise ValueError(f"UserList is duplicated! Name={v['username']}")
        return ret

    def authenticate(self, username: str, password: str) -> dict:
        user = self.user_dict.get(username, dict())
        if user:
            if user.get('password') == password:
                return user
            else:
                pass
                # raise ValueError(f"Password isn't correct!")
        else:
            pass
            # raise ValueError(f"UserName=[{username}] isn`t existed!")
        return dict()