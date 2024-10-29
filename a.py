num_of_dec_vars = int(input("How many dec. vars are there?"))
answer = [-1] * num_of_dec_vars

#construct objective function
obj_function = []
for i in range(num_of_dec_vars):
    obj_function += [-int(input("Coefficient of X" + str(i + 1) +" in obj function:"))]




#construct inequalities
inequalities = []
num_of_constraints = int(input("How many constraints are there?"))
obj_function += [0 for i in range(num_of_constraints + 1)] # slacks and one more for optimal value
for i in range(num_of_constraints):
    current_inequality = []
    for j in range(num_of_dec_vars):
        current_inequality += [int(input("Coefficient of X" + str(j + 1) +" in inequality number "+ str(i + 1) + ":"))]
    
    slack_part = []
    for j in range(num_of_constraints):
        if j == i:
            slack_part += [1]
        else:
            slack_part += [0]
    current_inequality += slack_part

    

    inequality_type = input("gteq / steq:")
    while inequality_type not in ["gteq", "steq"]:
        inequality_type = input("gteq / steq:")

    current_inequality += [int(input("rhs of the inequality:"))]

    if inequality_type == "gteq":
        for j in range(len(current_inequality)):
            current_inequality[j] = -current_inequality[j]
    
    inequalities += [current_inequality]

def check_further_optimize(obj_function, inequalities):
    check_negative = 0
    index_of_smallest_element = 0
    for i in range(len(obj_function) - 1): #what if a slack variable becomes negative?
        if obj_function[i] <= check_negative:
            check_negative = obj_function[i]
            index_of_smallest_element = i
    if check_negative == 0: # no negative elements remained
        return
    solve(obj_function, inequalities, index_of_smallest_element)

def solve(obj_function, inequalities, index_of_smallest_element):
    pivot_element_position = determine_pivot_element(inequalities, index_of_smallest_element)
    pivot_element = inequalities[pivot_element_position[0]][pivot_element_position[1]]

    answer[pivot_element_position[1]] = pivot_element_position[0]

    #make pivot element's row adjustments
    for i in range(len(inequalities[pivot_element_position[0]])):
        inequalities[pivot_element_position[0]][i] /= pivot_element
    pivot_element = inequalities[pivot_element_position[0]][pivot_element_position[1]] #now pivot element is 1


    #other rows' adjustments
    for i in range(num_of_constraints):
        if i != pivot_element_position[0]:
            coefficient = - inequalities[i][pivot_element_position[1]] / pivot_element
            for j in range(len(inequalities[i])):
                inequalities[i][j] += coefficient * inequalities[pivot_element_position[0]][j]

    #obj. function adjustment
    coefficient = - obj_function[pivot_element_position[1]] / pivot_element
    for i in range(len(obj_function)):
        obj_function[i] += coefficient * inequalities[pivot_element_position[0]][i]
    check_further_optimize(obj_function, inequalities)


def determine_pivot_element(inequalities, index_of_smallest_element):
    pivot_row = 0
    minimum_ratio = float("INF")
    for i in range(len(inequalities)):
        if inequalities[i][index_of_smallest_element] == 0:
            continue
        row_ratio = inequalities[i][-1] / inequalities[i][index_of_smallest_element]
        if row_ratio < minimum_ratio: # what if there are two rows with minimum ratio?
            minimum_ratio = row_ratio
            pivot_row = i
    return [pivot_row, index_of_smallest_element] #row, column of pivot in inequalities (excluding obj function as a row)
    




check_further_optimize(obj_function, inequalities)

#print(obj_function,"--")
#for i in inequalities:
#    print(i)

for i in range(num_of_dec_vars):
    print("Value of X" + str(i + 1)+" is ",end="" )
    if answer[i] == -1:
        print(0)
        continue
    print(inequalities[answer[i]][-1])
print("Optimum value is "+ str(obj_function[-1]))


