s = '1, 2, 3, 4'
l = [x.strip() for x in s.split(',')]
print(l)
print(type(l[0]))
print(l[0]+l[1])
# ['1', '2', '3', '4']
# <class 'str'>

s = '1, 2, 3, 4'
l = [float(x.strip()) for x in s.split(',')]
print(l)
print(type(l[0]))
print(l[0]+l[1])
# [1, 2, 3, 4]
# <class 'int'>
