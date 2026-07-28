from locust import HttpUser, task, between

class TrackerUser(HttpUser):
    wait_time= between(1, 3)
    @task(5)
    def cheapest(self):
        self.client.get("/tracker/cheapest_product/1")

    @task(3)
    def history(self):
        self.client.get("/tracker/history/1")

    @task(2)
    def vendor(self):
        self.client.get("/tracker/product_vendor_history/1")