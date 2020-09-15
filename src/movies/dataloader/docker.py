import os

from movies.db_config import IMAGE, CONTAINER_NAME, PWD


def create_container():

    os.system(
        "docker run -d --name {} -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD={}' -p 1433:1433 {}".format(
            CONTAINER_NAME, PWD, IMAGE
        )
    )
    os.system("docker start {}".format("CONTAINER_NAME"))


def stop_container():

    os.system("docker stop {}".format(CONTAINER_NAME))


def run_container():

    os.system(
        "docker start {}".format(
            CONTAINER_NAME
        )
    )