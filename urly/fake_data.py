from faker import Faker
from urlyapp.models import Bookmark, Profile
import random


def fake():
    faker = Faker()
    for _ in range(1000):
        bm = Bookmark.objects.create(title=faker.name(), description=faker.address(), \
                                     url=faker.url())
    bms = list(Bookmark.objects.all())

    for idx in range(100):
        bm = [bms.pop(random.randint(0, 1000 - idx*10 - idx2 - 1)) for idx2 in range(10)]
        pf = Profile.objects.create(username=faker.name(), description=faker.text())
        for item in bm:
            item.profile = pf
            item.save()

def deletem():
    Bookmark.objects.all().delete()
    Profile.objects.all().delete()
