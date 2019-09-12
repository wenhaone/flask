#递归算法
def binary_search(nums,key):
    nums.sort()
    mid = len(nums)//2
    print(mid,end = '\n')
    print(nums[mid] , end="mid \n")
    if mid > 0 :
        if key >nums[mid] :
            return binary_search(nums[mid+1:],key)
        elif key < nums[mid]:
            return  binary_search(nums[:mid],key)
        else:
            return  True
    return False
#非递归算法
def binary_search2(nums,key):
    left = 0
    right = len(nums)-1
    while left <= right :
        mid = (left+right)//2
        if key > nums[mid]:
            left = mid+1
        elif key < nums[mid]:
            right = mid
        else:
            return True
    return False




if __name__ == "__main__":
    list = [1,2,3,4,5,6,7,8]
    num = 11
    print(binary_search2(list,num))
    # print(1//2)