# 搜索插入位置
## 题目
>给定一个排序数组和一个目标值,在数组中找到目标值,并返回其索引。如果目标值不存在于数组>中,返回它将会被按顺序插入的位置。
>你可以假设数组中无重复元素。
>>示例 1
>>输入: [1,3,5,6], 5
>>输出: 2
>>
>>示例 2:
>>输入: [1,3,5,6], 2
>>输出: 1
>>
>>示例 3:
>>输入: [1,3,5,6], 7
>>输出: 4
>>
>>示例 4:
>>输入: [1,3,5,6], 0
>>输出: 0

## 可以在这里确认
->[LeetCode 35 搜索插入位置](https://leetcode-cn.com/problems/search-insert-position/)

## 思考
题目中有两个重要的信息,一个是**排序数组**,一个是**无重复元素**,所以这道题本意应该是要考二分查找。这里就是用二分查找解答。虽然这里可以简单的从头遍历到尾,但是这么做的话,时间复杂度应该是O(n),而使用二分算法的话复杂度就是O(logn),这里是二分法,所以底数是2。

## 解题思路
这里写几个二分查找的关键点
1. 循环的结束是 **left <= right**, 注意等号。
2. 求解中数的时候小心数字溢出。比如,mid=(left+right)/2。应该使用mid=left+(right - left) / 2。
3. list[mid] > target时,处理右值,right = mid - 1。
4. list[mid] < target时,处理左值, left = mid + 1。

## Python实现
```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        if nums[0] > target : return 0
        
        left = 0; right = len(nums) - 1
        while left <= right:
            mid = left + (right - left) // 2
            if nums[mid] < target : left = mid + 1
            elif nums[mid] > target : right = mid - 1
            elif nums[mid] == target : return mid
            
        return left
```

执行用时 :72 ms, 在所有 Python3 提交中击败了68.36%的用户
内存消耗 :14.2 MB, 在所有 Python3 提交中击败了5.47%的用户

## C++实现
```cpp
class Solution 
{
public:
    int searchInsert(vector<int>& nums, int target) 
    {
        if(nums[0] > target) return 0;
        
        int left = 0;
        int right = nums.size() - 1;
        while(left <= right)
        {
            int mid = left + (right - left) / 2;
            if(nums[mid] > target)      right = mid - 1;
            else if(nums[mid] < target) left = mid + 1;
            else if(nums[mid] == target) return mid;
        }
        
        return left;
    }
};
```

执行用时 :8 ms, 在所有 C++ 提交中击败了83.23%的用户
内存消耗 :9 MB, 在所有 C++ 提交中击败了73.88%的用户