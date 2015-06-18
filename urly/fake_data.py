from faker import Faker
from urlyapp.models import Bookmark

def fake():
    faker = Faker()
    for _ in range(1000):
        bm = Bookmark.objects.create(title=faker.name(), description=faker.address(), \
                                     url=faker.url())
