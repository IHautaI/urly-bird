from faker import Faker
from urlyapp.models import Bookmark, Profile, Tag
import random



def fake():
    tags = ['terrible', 'great', 'smelly', 'sad', 'bright', 'too bright', 'gnarly'\
            'awesome', 'happy', 'tremendous']
    faker = Faker()

    for item in tags:
        Tag.objects.create(name=item)

    tags = list(Tag.objects.all())
    for _ in range(1000):
        bm = Bookmark.objects.create(title=faker.name(), description=faker.address(), \
                                     url=faker.url())
        for _ in range(3):
            bm.tag_set.add(random.choice(tags))

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
    Tag.objects.all().delete()
