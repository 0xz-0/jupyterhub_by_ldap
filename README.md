# jupyterhub_by_ldap
[中文](./README_CN.md)|EN

 * Add Login Auth by LDAP and UserList
 * Base Image from [docker.io/jupyterhub/jupyterhub:2.1.1](https://hub.docker.com/r/jupyterhub/jupyterhub)

## Start

1. Alter .env ; Add User to [user_list(in code)](./auth/user.py) ; Alter [config](./jupyterhub_config.py).
   
2. [optional] Check ldap and user_list
   1. env install:`poetry install`
   2. auth unit:`python -m unittest auth/test_auth.py`

3. Build Image
    ```shell
        docker build -t jupyterhub:v1 -f ./build/Dockerfile .
    ```

4. Run Container
    ```shell
        docker run -d \
        --name jupyterhub \
        --env-file .env \
        -v $PWD/volume/file:/home \
        -p 8000:8000 \
        jupyterhub:v1
    ```
    * notice: If volume is existed. Maybe it cause a error with permissions.
  
5. [optional] Check Container Service Runner
    ```
    docker exec -it jupyterhub bash -c "sh /srv/jupyterhub/health.sh"
    ```

6. Open http://localhost:8000 And Login to Start!