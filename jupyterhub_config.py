from tornado import gen
from jupyterhub.auth import Authenticator
import pwd
import traceback

import os
import sys
sys.path.append('/srv/jupyterhub') # must be the same as "add auth {path}" in dockerfile
from auth.user import UserAuth
from auth.self_ldap import SelfLdap

class MyAuthenticator(Authenticator):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ldap = SelfLdap()
        self.user = UserAuth()

    def system_user_exists(self, username: str):
        """Check if the user exists on the system"""
        try:
            pwd.getpwnam(username)
            self.log.info('Judge user=%s exists!' % username)
        except Exception as e:
            self.log.error('Ensure User exist! %s' % (repr(e)))
            return False
        else:
            return True

    def add_system_user(self, uid, username, password):
        """
            Create a new local UNIX user on the system.
            Tested to work on FreeBSD and Linux, at least.
        """
        res = os.system('useradd -u %s -p %s -m %s ' %(uid, password, username))
        if res != 0:
            self.log.warning('User %s create failure: %s' % (username, res))
            return False
        
        ## create password
        # res = os.system('echo %(pass)s |passwd --stdin %(name1)s' % {'name1': username, 'pass': password})
        # res = os.system('echo %s:%s | chpasswd' % (username, password))
        # if res != 0:
        #     self.log.warning('User %s password create failure: %s' % (username, res))
        #     return False
        
        ## chown home path
        # res = os.system('chown -R %s:%s /home/%s' %(username, username, username))
        # if res != 0:
        #     self.log.warning('User %s home dir Chown failure: %s' % (username, res))
        #     return False

        self.log.info(f'Create user={username}; uid={uid} Success!')
        return True

    @gen.coroutine
    def authenticate(self, handler, data):
        '''
        :param handler:
        :param data:
        '''
        # self.log.info(data)
        # ldap对大小写不敏感，但是Liunx的账户对大小写敏感,此处全部取小写
        username = data["username"].lower().strip()
        password = data["password"].strip()
        # self.log.info("username:%s;password:%s" % (username,password))

        if password is None or password.strip() == "":
            self.log.warning(
                "Username:%s Login denied for blank password", username)
            return None

        # auth by user list
        user_dict = self.user.authenticate(username=username, password=password)
        if user_dict.get('uid'):
            pass
        else:
            try:
                user_dict = self.ldap.authenticate(
                    username=username, password=password)
            except Exception as e:
                traceback.print_exc()
                self.log.warning(e)
                return

        self.log.info('Current user name: %s' % username)
        # self.log.debug('Current user %s' % repr(user_dict))
        if not self.system_user_exists(username):
            if self.add_system_user(**user_dict):
                return username
            else:
                return None
        return username


# 要生成带有设置和描述的默认配置文件：
#jupyterhub --generate-config
# 用户自定义认证 - 不直接用ldap插件的原因在于，需要改源码来实现新增操作系统用户的步骤(因为官方不建议在ldap被注销后,仍然保留其文件内容)
c.JupyterHub.authenticator_class = MyAuthenticator

# 指定cookie secret的文件，内容必须是64位哈希字符串，如6dd65ff19de7b8cb6d53031b0ad940e7379e15cf7ab612094d19e8b5141cc52c
# c.JupyterHub.cookie_secret_file = '/srv/jupyterhub/jupyterhub_cookie_secret'

# shutdown the server after no activity for 2 hours
c.ServerApp.shutdown_no_activity_timeout = 2 * 60 * 60
# shutdown kernels after no activity for 1 hour
c.MappingKernelManager.cull_idle_timeout = 1 * 60 * 60
# check for idle kernels every 1 hour
c.MappingKernelManager.cull_interval = 1 * 60 * 60

# 仪表板中访问的最高级别目录。
c.Spawner.notebook_dir = '/home/{username}'

# 是否有向系统添加用户的权限
# c.LocalAuthenticator.create_system_users = True
# c.DummyAuthenticator.password = "admin"

# 初始管理员用户
c.JupyterHub.admin_access = True
c.JupyterHub.admin_users = {"admin"}

# 白名单
# c.Authenticator.whitelist = {}

# Jupyterhub service setting
# c.JupyterHub.spawner_class = 'sudospawner.SudoSpawner'
c.JupyterHub.base_url = '/'
c.JupyterHub.cookie_max_age_days = 14  # cookie有效期为1天，默认值14为2周

# customer templstes path, default is []
c.JupyterHub.template_paths = []
