# 문자열 포멧팅
print("I eat %d apples." %3) # 숫자 포멧팅
print("I eat %s apples." %"five") # 문자 포멧팅
print("I eat %d apples and %d banana" %(5, 3)) # 다중 포멧팅

# 문자열 연습문제
pin = "881120-1068234" #Q1
yyyymmdd = pin[:6]
num = pin[7:]
print(yyyymmdd)
print(num)

print(pin[-7]) #Q2

# 리스트 연습문제
a = [1, 3, 5, 4, 2] # Q1
a.sort()
a.reverse()
print(a)

a = ['Life', 'is', 'too', "short"] #Q2
print(" ".join(a))

# 튜플 연습문제
a = (1, 2, 3)
a = a + (4,)
print(a)

# 딕셔너리 연습문제
a = {'A':90, 'B':80, 'C':70}
result = a.pop('B')
print(result, a)

# 집합 연습문제
a = [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5]
aSet = set(a)
b = list(aSet)
print(b)
