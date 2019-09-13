"""给定一个数组，
返回3数相加为0的所有可能
不能重复
思路： 两个指针
j，k j向左  k向右
滑动相加法
两数相加也可采用此法

"""


class Sulution(object):
    def threeNum(self,nums):
        if len(nums) < 3 :
            return None
        nums.sort()
        i  = 0
        list = []
        while i < len(nums)-2:
            j = i +1
            k = len(nums)-1
            while j < k :
                print(i,j,k)
                l = [nums[i] , nums[j] ,nums[k]]
                print(l)
                if sum(l) == 0 :
                    list.append(l)
                    j+=1
                    k-=1
                    #忽略 j ， k 相等
                    while nums[k] == nums[k-1]:
                        k = k -1
                    while nums[j] == nums[j+1]:
                        j = j + 1
                elif sum(l) > 0:
                    k = k -1
                else:
                    j = j +1
            i =i +1
            #忽略 i相等
            while i < len(nums)-2 and nums[i] ==nums[i-1]:
                i+=1
        return list

if __name__ == "__main__":
    s = Sulution()
    print(s.threeNum([-1,0,1,2,-1,-4]))

