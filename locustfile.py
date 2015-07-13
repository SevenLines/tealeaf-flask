from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
    @task(2)
    def index(l):
        l.client.get("/")

    @task(2)
    def group2211(l):
        l.client.get("/g/52/")

    @task(2)
    def group2221(l):
        l.client.get("/g/53/")

    @task(2)
    def group2222(l):
        l.client.get("/g/54/")

    @task(2)
    def group2241(l):
        l.client.get("/g/55/")

    @task(2)
    def group2251(l):
        l.client.get("/g/56/")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
