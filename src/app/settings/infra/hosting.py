from environ import Env

env = Env()

HOST = env("HOST", default="localhost")
