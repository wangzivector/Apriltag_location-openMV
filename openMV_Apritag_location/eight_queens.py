aim=[]
now=[]
def permutations_now(arr, position, end):

    if position == end:
        now.append([])
        for aa in range(1,len(arr)+1):
            now[len(now)-1].append(arr[aa-1])

    else:
        for index in range(position, end):
            arr[index], arr[position] = arr[position], arr[index]
            permutations_now(arr, position+1, end)
            arr[index], arr[position] = arr[position], arr[index]
def permutations_aim(arr, position, end):

    if position == end:
        aim.append([])
        for aa in range(1,len(arr)+1):
            aim[len(aim)-1].append(arr[aa-1])

    else:
        for index in range(position, end):
            arr[index], arr[position] = arr[position], arr[index]
            permutations_aim(arr, position+1, end)
            arr[index], arr[position] = arr[position], arr[index]

solution = [
    [ 1,13,24,30,35,47,50,60 ],
    [ 1,14,24,27,39,44,50,61 ],
    [ 1,15,20,30,40,42,53,59 ],
    [ 1,15,21,32,34,44,54,59 ],
    [ 2,12,22,32,35,41,55,61 ],
    [ 2,13,23,25,35,48,54,60 ],
    [ 2,13,23,28,33,48,54,59 ],
    [ 2,14,17,31,36,48,51,61 ],
    [ 2,14,24,27,33,44,55,61 ],
    [ 2,15,19,30,40,45,49,60 ],
    [ 2,15,21,32,33,44,54,59 ],
    [ 2,16,22,25,35,45,55,60 ],
    [ 3,9,23,29,40,42,52,62 ],
    [ 3,13,18,32,33,47,52,62 ],
    [ 3,13,18,32,38,44,55,57 ],
    [ 3,13,23,25,36,42,56,62 ],
    [ 3,13,24,28,33,47,50,62 ],
    [ 3,14,18,29,40,41,55,60 ],
    [ 3,14,18,31,33,44,56,61 ],
    [ 3,14,18,31,37,41,56,60 ],
    [ 3,14,20,25,40,45,55,58 ],
    [ 3,14,20,26,40,45,55,57 ],
    [ 3,14,24,25,36,47,53,58 ],
    [ 3,14,24,25,37,47,50,60 ],
    [ 3,14,24,26,36,41,55,61 ],
    [ 3,15,18,32,37,41,52,62 ],
    [ 3,15,18,32,38,44,49,61 ],
    [ 3,16,20,31,33,46,50,61 ],
    [ 4,9,21,32,34,47,51,62 ],
    [ 4,9,21,32,38,43,55,58 ],
    [ 4,10,21,32,38,41,51,63 ],
    [ 4,10,23,27,38,48,49,61 ],
    [ 4,10,23,27,38,48,53,57 ],
    [ 4,10,23,29,33,48,54,59 ],
    [ 4,10,24,29,39,41,51,62 ],
    [ 4,10,24,30,33,43,53,63 ],
    [ 4,14,17,29,34,48,51,63 ],
    [ 4,14,24,26,39,41,51,61 ],
    [ 4,14,24,27,33,47,53,58 ],
    [ 4,15,17,32,37,42,54,59 ],
    [ 4,15,19,32,34,45,49,62 ],
    [ 4,15,21,26,38,41,51,64 ],
    [ 4,15,21,27,33,46,56,58 ],
    [ 4,16,17,27,38,42,55,61 ],
    [ 4,16,17,29,39,42,54,59 ],
    [ 4,16,21,27,33,47,50,62 ],
    [ 5,9,20,30,40,42,55,59 ],
    [ 5,9,24,28,34,47,51,62 ],
    [ 5,9,24,30,35,47,50,60 ],
    [ 5,10,20,30,40,43,49,63 ],
    [ 5,10,20,31,35,48,54,57 ],
    [ 5,10,22,25,39,44,56,59 ],
    [ 5,10,24,25,36,47,51,62 ],
    [ 5,11,17,30,40,42,52,63 ],
    [ 5,11,17,31,34,48,54,60 ],
    [ 5,11,24,28,39,41,54,58 ],
    [ 5,15,17,27,40,46,52,58 ],
    [ 5,15,17,28,34,48,54,59 ],
    [ 5,15,18,28,40,41,51,62 ],
    [ 5,15,18,30,35,41,52,64 ],
    [ 5,15,18,30,35,41,56,60 ],
    [ 5,15,20,25,35,48,54,58 ],
    [ 5,16,20,25,35,46,50,63 ],
    [ 5,16,20,25,39,42,54,59 ],
    [ 6,9,21,26,40,43,55,60 ],
    [ 6,10,23,25,35,45,56,60 ],
    [ 6,10,23,25,36,48,53,59 ],
    [ 6,11,17,31,37,48,50,60 ],
    [ 6,11,17,32,36,42,55,61 ],
    [ 6,11,17,32,37,42,52,63 ],
    [ 6,11,21,31,33,44,50,64 ],
    [ 6,11,21,32,33,44,50,63 ],
    [ 6,11,23,26,36,48,49,61 ],
    [ 6,11,23,26,40,45,49,60 ],
    [ 6,11,23,28,33,48,50,61 ],
    [ 6,12,17,29,40,42,55,59 ],
    [ 6,12,18,32,37,47,49,59 ],
    [ 6,12,23,25,35,45,50,64 ],
    [ 6,12,23,25,40,42,53,59 ],
    [ 6,16,18,28,33,47,53,59 ],
    [ 7,9,19,32,38,44,50,61 ],
    [ 7,10,20,25,40,45,51,62 ],
    [ 7,10,22,27,33,44,56,61 ],
    [ 7,11,17,30,40,45,50,60 ],
    [ 7,11,24,26,37,41,54,60 ],
    [ 7,12,18,29,40,41,51,62 ],
    [ 7,12,18,32,38,41,51,61 ],
    [ 7,13,19,25,38,48,50,60 ],
    [ 8,10,20,25,39,45,51,62 ],
    [ 8,10,21,27,33,47,52,62 ],
    [ 8,11,17,30,34,45,55,60 ],
    [ 8,12,17,27,38,42,55,61 ]
]
in_position = [ 0,1,2,3,4,5,6,7 ]
max_notmove=0
max_notmove_times=1
'''for count_1 in range(1,9):
    in_position[count_1-1]=input("input the number")'''
solution_list=[]
for count_2 in range(1,93):

    i=0
    j=0
    chess_count=0
    while True:

        if int(in_position[i])<solution[count_2 - 1][j]:
            i+=1

        elif int(in_position[i])>solution[count_2 - 1][j]:
            j+=1

        else:
            i+=1
            j+=1
            chess_count+=1

        if (i>7)or(j>7):
            if max_notmove<chess_count:
                max_notmove=chess_count
                max_notmove_times=1
                solution_list.clear()
                solution_list.insert(92,count_2)
            elif max_notmove==chess_count:
                 max_notmove_times=1+max_notmove_times
                 solution_list.insert(92,count_2)
            break
print(solution_list)
cpy=[]
def min_num(num1,num2):
    num1hang=int(num1%8)
    num1lie=int(num1/8)
    num2hang=int(num2%8)
    num2lie=int(num2/8)
    return (abs(num1hang-num2hang)+abs(num1lie-num2lie))
def min_road(arraim,arrnow):
    sum_road=0
    for kk in range(len(arraim)-1):
        sum_road+=min_num(arraim[kk],arrnow[kk])
        sum_road+=min_num(arraim[kk],arrnow[kk+1])
    sum_road+=min_num(arraim[len(arraim)-1],arrnow[len(arraim)-1])
    return sum_road
count_road=10000
aim_s=[]
now_s=[]
for count_3 in solution_list:
    print(count_3)
    i=0
    j=0
    chess_count=0
    cpy.clear()
    aim.clear()
    now.clear()
    for cc in range(1,9):
        cpy.insert(92,in_position[cc-1])
    while True:

        if int(cpy[i])<solution[count_3 - 1][j]:
            i+=1

        elif int(cpy[i])>solution[count_3 - 1][j]:
            j+=1

        else:
            cpy[i]=100
            solution[count_3 - 1][j]=100
            i+=1
            j+=1
        if (i>7)or(j>7):
            for k in range(1,max_notmove+1):
                cpy.remove(100)
                solution[count_3 - 1].remove(100)
            permutations_aim(solution[count_3 - 1],0,len(solution[count_3 - 1]))
            permutations_now(cpy,0,len(cpy))
            for ccc in range(len(now)):
                g=min_road(aim[ccc],now[ccc])
                if g<count_road:
                    count_road=g
                    aim_s.clear()
                    now_s.clear()
                    for cccc in range(len(aim[ccc])):
                        aim_s.insert(92,aim[ccc][cccc])
                        now_s.insert(92,now[ccc][cccc])
            break

print(now_s)
print(aim_s)

