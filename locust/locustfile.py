from locust import HttpUser, task, between
from random import randint
from datetime import date

class TrackerUser(HttpUser):
    wait_time= between(1, 3)
    @task(5)
    def cheapest(self):
        product_id= randint(1, 5)
        today = date.today()
        date_string = today.strftime("%Y-%m-%d")
        print(f"Requesting cheapest product for product_id: {product_id}, {date_string}")
        print(f"URL: /tracker/cheapest_product/{product_id}/{date_string}/{date_string}")
        self.client.get(f"/tracker/cheapest_product/{product_id}/{date_string}/{date_string}")

    @task(3)
    def history(self):
        product_id= randint(1, 5)
        today = date.today()
        date_string = today.strftime("%Y-%m-%d")
        print(f"Requesting price history for product_id: {product_id}, {date_string}")
        print(f"URL: /tracker/price_history/{product_id}/{date_string}/{date_string}")
        self.client.get(f"/tracker/price_history/{product_id}/{date_string}/{date_string}")

    @task(2)
    def vendor(self):
        product_id= randint(1, 5)
        vendor_id= randint(1, 5)
        today = date.today()
        date_string = today.strftime("%Y-%m-%d")
        print(f"Requesting product vendor history for product_id: {product_id}, vendor_id: {vendor_id}, {date_string}")
        print(f"URL: /tracker/product_vendor_history/{product_id}/{vendor_id}/{date_string}/{date_string}")
        self.client.get(f"/tracker/product_vendor_history/{product_id}/{vendor_id}/{date_string}/{date_string}")