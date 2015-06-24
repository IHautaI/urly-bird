from faker import Faker
import random
from django.contrib.auth.models import User
import datetime
from hashids import Hashids

from urlyapp.models import Bookmark, Profile, Tag


def fake():
    bmnum = 100
    pfnum = 10

    tags = ['terrible', 'great', 'smelly', 'sad', 'bright', 'too bright', 'gnarly',\
            'awesome', 'happy', 'tremendous']
    faker = Faker()

    for item in tags:
        Tag.objects.create(name=item)

    tags = list(Tag.objects.all())
    for _ in range(bmnum):
        bm = Bookmark.objects.create(title=faker.name(), description=faker.address(), \
                                     _url=faker.url())
        for _ in range(3):
            bm.tag_set.add(random.choice(tags))

    bms = list(Bookmark.objects.all())
    hashid = Hashids(salt='Moddey Dhoo')
    for idx in range(pfnum):
        bm = [bms.pop(random.randint(0, bmnum - idx*10 - idx2 - 1)) for idx2 in range(10)]
        pf = Profile.objects.create(username=faker.name(), description=faker.text())
        for item in bm:
            item.profile = pf
            item.save()
            item.short = hashid.encode(item.id, pf.id)
            item.timestamp = datetime.datetime.utcnow() + datetime.timedelta(weeks=-52)
            item.timestamp = item.timestamp.replace(tzinfo=datetime.timezone(offset=datetime.timedelta()))
            item.save()

    pfs = list(Profile.objects.all())

    bms = list(Bookmark.objects.all())

    for item in bms:
        num = random.randint(1,10)
        for idx in range(num):
            pf = random.choice(pfs)
            timestamp = faker.date_time_this_year().replace(tzinfo=datetime.timezone(offset=datetime.timedelta()))
            item.click_set.create(profile=pf, timestamp=timestamp)

            item.save()

def users():
    profs = list(Profile.objects.all().order_by('pk'))

    for idx, prof in enumerate(profs):
        user = User.objects.create(username=prof.username, password=idx+1)
        prof.user = user
        prof.save()


def deletem():
    Bookmark.objects.all().delete()
    Profile.objects.all().delete()
    Tag.objects.all().delete()
    User.objects.all().delete()
