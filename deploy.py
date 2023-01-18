import sys
import time

from python_on_whales.docker_client import DockerClient

envs = {
    "qa": {"compose_files": ["docker-compose.qa.yml"], "compose_env_file": ".env.qa"},
    "prod": {"compose_files": ["docker-compose.prod.yml"], "compose_env_file": ".env.prod"},
    "dev": {"compose_files": ["docker-compose.yml"], "compose_env_file": ".env.dev"},
}
services_to_deploy = ["app", "celery-scheduler", "celery-worker"]


def _env_from_interactive_input():
    print("No env argument provided, must define the env")
    while True:
        env = input(f"Which env to deploy? {' | '.join(envs.keys())}: ")
        if env not in envs:
            print("Invalid input")
            continue
        break
    return envs[env]


def _env_from_args(args):
    if len(args) > 1:
        print("Only one argument should be provided!")
        exit(1)
    env = args[0]
    if env not in envs:
        print(f"Invalid env choice, choose one of: {' | '.join(envs.keys())}")
    return envs[env]


def get_env_from_args_or_input():
    init_args = sys.argv[1:]
    if not init_args:
        return _env_from_interactive_input()
    return _env_from_args(init_args)


def get_running_containers(cli: DockerClient):
    return [c for c in cli.compose.ps() if c.state.running]


def main():
    """This script allows deploying a new app instance without any downtime, this plays together with the traefik
    health-check that will only dispatch requests to the new container when available"""
    env = get_env_from_args_or_input()

    dkr = DockerClient(**env)
    running_containers = get_running_containers(dkr)
    if not running_containers:
        print("No containers running, starting all containers")
        dkr.compose.up(build=True, detach=True, scales={"app": 1})
        return

    print(f"There are running containers, scaling the app")
    dkr.compose.up(
        services=services_to_deploy,
        detach=True,
        scales={"app": 2},
        recreate=False,
        build=True,
    )
    print("Waiting some seconds (60) while the new app service get up")
    time.sleep(60)
    print("Rescaling to one app service")
    dkr.compose.up(
        services=services_to_deploy,
        detach=True,
        scales={"app": 1},
        recreate=False,
    )


main()
