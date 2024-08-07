from faker import Faker

fake = Faker()
#  ko_kr로 세팅
fake = Faker('ko_KR')

def get_name():
    return fake.name()
    