# jupyterhub_by_ldap
中文|[EN](./README.md)

 * 增加通过LDAP和用户列表的方式登录
 * 基于基础镜像，[docker.io/jupyterhub/jupyterhub:2.1.1](https://hub.docker.com/r/jupyterhub/jupyterhub)

## 开始

1. 修改环境变量文件;在[用户列表代码里](./auth/user.py) 增加可登录的用户列表; 修改[配置文件](./jupyterhub_config.py).
   
2. [可选]校验和检查LDAP以及用户列表
   1. 安装环境依赖:`poetry install`
   2. 执行单元检测:`python -m unittest auth/test_auth.py`

3. 构建镜像`docker build -t jupyterhub:v1 -f ./build/Dockerfile .`

4. 启动容器
```shell
docker run -d \
--name jupyterhub \
--env-file .env \
-v $PWD/volume/file:/home \
-p 8000:8000 \
jupyterhub:v1
```
    * 注意: 如果挂载的文件已经存在，则可能会产生一个由权限不足导致的问题
  
5. [可选]检查服务是否在运行
    ```
    docker exec -it jupyterhub bash -c "sh /srv/jupyterhub/health.sh"
    ```

6. 打开[网址](http://localhost:8000) 然后登录即可。
   
## 一些注意事项

1. 登录的用户，先判断用户列表，再判断ldap。可能出现用户名冲突，暂需自行处理。