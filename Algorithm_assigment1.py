# Assignment for Algorhitm
num = int(input())
initiallist = list(map(int,input().split()))
num_list1 = []
num_list2 = []
count = 0

for i in range(num):
    if i%2 != 0: 
        num_list1.append(initiallist[i]) #짝수자리에 오는 숫자는 num_list1
    else:
        num_list2.append(initiallist[i]) #홀수자리에 오는 숫자는 num_list2

num_list1.sort(reverse=True)  #짝수자리에 오는 수는 내림차순 정렬
num_list2.sort() #홀수자리에 오는 수는 오름차순 정렬

while True:
    if num%2 != 0: # 입력받은 수가 홀수일 때
        print(num_list2[count], end=' ')
        if count == len(num_list2) - 1:
            break
        print(num_list1[count], end=' ')
        count += 1
    else: # 입력받은 수가 짝수일 때
        print(num_list2[count], end=' ')
        print(num_list1[count], end=' ')
        count += 1
        if count == len(num_list1):
            break

    
