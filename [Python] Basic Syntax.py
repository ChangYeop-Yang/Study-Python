# ⓐ 중첩리스트 만들기
t = ["begin", "end"]
q = [1, 2, 3]
t.insert(1, q)
print("Values : %s" %t)

# ⓑ 리스트를 Stack으로 사용하기
s = [10, 20, 30, 40 , 50]
s.append(60) # Push
while s : # Pop
    print("Stack : %d" %s.pop())

# ⓒ 리스트를 Queue으로 사용하기
a = [10, 20, 30, 40, 50]
a.append(60) #Insert
while a : #Delete
    print("Queue : %d" %a.pop(0))

# ⓓ 리스트로 2차원 배열 표현하기
mat = [ [1, 2, 3], [4, 5, 6], [7, 8, 9] ]
print("mat[1][2] : %d" %mat[1][2]) # [4, 5, 6] => [6]
