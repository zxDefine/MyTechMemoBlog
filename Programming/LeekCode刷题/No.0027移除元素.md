# 移除元素
## 题目
>给定一个数组 nums 和一个值 val,你需要原地移除所有数值等于 val 的元素,返回移除后数组的新长度。不要使用额外的数组空间,你必须在原地修改输入数组并在使用 O(1) 额外空间的条件下完成。元素的顺序可以改变。你不需要考虑数组中超出新长度后面的元素。
>>示例 1:
>>给定 nums = [3,2,2,3], val = 3,
>>函数应该返回新的长度 2, 并且 nums 中的前两个元素均为 2。
>>你不需要考虑数组中超出新长度后面的元素。
>>
>>示例 2:
>>给定 nums = [0,1,2,2,3,0,4,2], val = 2,
>>函数应该返回新的长度 5, 并且 nums 中的前五个元素为 0, 1, 3, 0, 4。
>>注意这五个元素可为任意顺序。
>>你不需要考虑数组中超出新长度后面的元素。

## 可以在这里确认
->[LeetCode 27 移除元素](https://leetcode-cn.com/problems/remove-element/)

## 思考
使用双指针,一个代表新数组的当前结尾位置,一个代表原素组当前检查位置。

## 解题思路
1.创建2个位置索引idxCurr,idxCheck
2.遍历数组,当当前元素不等于目标值的时候,把idxCheck的元素赋值给idxCurr的位置,同时idxCurr加1
3.当前元素等于目标值的时候,idxCheck加1

## Python
```python
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        idxCurr = 0
        idxCheck = 0
        for i in range(len(nums)):
            if nums[i] != val:
                nums[idxCurr] = nums[idxCheck]
                idxCurr += 1
            idxCheck += 1
        return idxCurr
```

执行用时:52 ms, 在所有 Python3 提交中击败了5.98%的用户
内存消耗:14.7 MB, 在所有 Python3 提交中击败了90.27%的用户

## C++实现
```cpp
class Solution {
public:
    int removeElement(vector<int>& nums, int val) {
        int idxCurr = 0;
        int idxCheck = 0;
        for(int i = 0; i < nums.size(); ++i){
            if(nums[i] != val){
                nums[idxCurr] = nums[idxCheck];
                idxCurr++;
            }
            idxCheck++;
        }
        return idxCurr;
    }
};
```

执行用时:4 ms, 在所有 C++ 提交中击败了51.07%的用户
内存消耗:8.6 MB, 在所有 C++ 提交中击败了40.55%的用户