"""给出2*n + 1 个的数字，除其中一个数字之外其他每个数字均出现两次，找到这个数字。
您在真实的面试中是否遇到过这个题？
样例给出 [1,2,2,1,3,4,3]，返回 4"""
class Solution(object):
    def singleNum(self,nums):
        EOR = 0
        #异或的特性
        # n^n = 0
        #n^0 = n   n^n-1^n = n-1  不管多长 只要有一样的就为0

        for i in nums :
            EOR ^= i
        return EOR

if __name__=="__main__":
    list = [1,2,3,4,4,2,1]
    s = Solution()
    print(s.singleNum(list))