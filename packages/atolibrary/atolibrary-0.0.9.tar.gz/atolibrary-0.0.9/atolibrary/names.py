from faker import Faker
import random 

fake = Faker()
#  ko_kr로 세팅
fake = Faker('ko_KR') 

schools = [
    '강동초등학교', '강명초등학교', '강솔초등학교', '고덕초등학교', '길동초등학교', 
    '둔촌초등학교', '명일초등학교', '상일초등학교', '성내초등학교', '암사초등학교'
]

countries = [
    '대한민국', '미국', '일본', '중국', '러시아', '독일', '프랑스', '영국', '이탈리아', '스페인',
    '캐나다', '멕시코', '브라질', '아르헨티나', '칠레', '콜롬비아', '페루', '베네수엘라', '호주', '뉴질랜드',
    '인도', '파키스탄', '방글라데시', '네팔', '스리랑카', '미얀마', '태국', '베트남', '말레이시아', '싱가포르',
    '인도네시아', '필리핀', '사우디아라비아', '이란', '이라크', '이스라엘', '터키', '이집트', '남아프리카공화국', '나이지리아',
    '케냐', '에티오피아', '탄자니아', '우간다', '가나', '코트디부아르', '모로코', '알제리', '튀니지', '리비아',
    '그리스', '포르투갈', '네덜란드', '벨기에', '스웨덴', '노르웨이', '덴마크', '핀란드', '폴란드', '체코',
    '헝가리', '오스트리아', '스위스', '루마니아', '불가리아', '크로아티아', '세르비아', '슬로바키아', '슬로베니아', '우크라이나'
]

robots = ['EV3', 'Spike Prime', 'Atobot', '로봇태권V', '마징가', 'R2D2', 'C3PO', 'Data', 'Bender', 'Hal', 'Optimus Prime', 'Wall-E', 'Eve', 'Johnny 5', 'K-9', 'T-800', 'BB-8', 'Robby', 'Gort', 'Maria']
vehicles = ['현대', '기아', '토요타', '벤츠', 'BMW', '아우디', '폭스바겐', '포드', '쉐보레', '닛산', '혼다', '마쯔다', '스바루', '테슬라', '볼보', '푸조', '시트로엥', '르노', '피아트', '람보르기니']
colors = [
    '빨강', '주황', '노랑', '초록', '파랑', '남색', '보라', '분홍', '갈색', '회색', 
    '검정', '흰색', '연두색', '하늘색', '자주색', '연분홍색', '연노랑색', '연파랑색', '연보라색', '연갈색', 
    '연회색', '진빨강', '진주황', '진노랑', '진초록', '진파랑', '진남색', '진보라', '진분홍', '진갈색', 
    '진회색', '진검정'
]

def get_human_name():
    return fake.name()

def get_social_security_number():
    return fake.ssn()

def get_school_name():
    return fake.random_element(schools)

def get_country_name():
    return fake.random_element(countries)

def get_robot_name():
    return fake.random_element(robots)

def get_vehicle_company():
    return fake.random_element(vehicles)

def get_color_name():
    return fake.random_element(colors)

def get_colors():
    return fake.random_elements(elements=colors, length=5, unique=True)
    
