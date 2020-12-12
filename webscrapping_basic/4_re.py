import re

p = re.compile("ca.e")
# . (ca.e) : 하나의 문자   > care, cafe, case (o)| caffe(x)
# ^ (^de) : 문자열의 시작 > desk, destination (o)| fade(x)
# $ (se$) : 문자열의 끝 > case, base (o) | face(x)


def print_match(m):
    if m:
        print('m.group() : ', m.group())
        print('m.string:', m.string)
        print('m.start(): ', m.start())
        print('m.end():', m.end())
        print('m.span():', m.span())
    else:
        print("메칭되지 않음")


# m = p.match('careless')
# print_match(m)

m = p.search("good care")
# search : 주어진 문자열 중에 일치하는 게 있는지 확인
print_match(m)
