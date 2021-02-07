from django.conf import settings
import requests

access_token = 'EAAIbhKF1vxYBAKDqE3qdHJ9oDZCrZBJfEXe62xI4hEgvR4TzE2FI6KUHRXmiSlNn4lVh6ZBZBA1eKA7xXKAkZA0I8wQWZCrClJfAUhTjhYlkklQOxzqiytEZAXkfMQGIDgYuDOMZB0ggLO0oCW3J5yqRy5l5gBN4V2ZBqQfazvZBDK9QZDZD'

#x = requests.get("https://graph.facebook.com/{0}/feed".format(105099951582064), params,timeout=2.5)
#y = requests.post(url, params,timeout=2.5)
#print(x.status_code)

class PublishInFacebook:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.access_token = settings.FB_ACCESS_TOKEN
        self.page_id = 105099951582064
        self.url = "https://graph.facebook.com/{0}/feed".format(self.page_id)

    def publish_facebook(self,post):
        if post.img or post.pdf:
            pass
        else:
            message = post.get_text()
            print(message)
            data = {'message':message, 'access_token':self.access_token}
            requests.post(self.url, data)
        return True
