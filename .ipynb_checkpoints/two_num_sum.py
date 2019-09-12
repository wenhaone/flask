"""求和问题，给定一个数组，数组中的元素唯一，数组元素数量 N >2，若数组中的
两个数相加和为 m，则认为该数对满足要求，请思考如何返回所有满足要求的数对（要
求去重），并给出该算法的计算复杂度和空间复杂度(2018-4-23-lyf)"""

#时间复杂度是O（n**2）
#空间复杂度是O（n）
def two_num_sum_list(list,sum):
    hash = set()
    for i in range(len(list)):
        for j in range(i+1,len(list)):
            if (list[i] + list[j] )== sum:
                hash.add((list[i],list[j]))

    return hash

if __name__=="__main__":
    list=[1,2,3,4,5,6,7,8]
    num = 9
    print(two_num_sum_list(list,num))
