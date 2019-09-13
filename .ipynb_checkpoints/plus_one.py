"""给一个数组 [1,2,3,4,5]
加一
输出 [1,2,3,4,6]
"""

class Solution(object):
    def plusone(self,nums):
        flag = 1
        for i in range(len(nums)-1 ,-1,-1):
            if nums[i] + flag == 10:
                nums[i] = 0
                flag =1
            else:
                nums[i] = nums[i] + flag
                flag = 0
        if flag == 1 :
            nums.insert(0,1)
        return  nums

