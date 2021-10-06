# 两数之和
## 题目
> 给定一个**整数数组**nums 和一个**整数目标值**target,请你在该数组中找出**和为目标值**的那**两个**整数,并返回它们的数组下标。
> 你可以假设每种输入只会对应一个答案。但是,数组中同一个元素在答案里不能重复出现。
>> 示例1
>>  输入:nums = \[2,7,11,15\], target = 9
>>  输出:\[0,1\]
>>  解释:因为 nums\[0\] + nums\[1\] == 9 ,返回 \[0, 1\] 。
>> 示例2
>>  输入:nums = \[3,2,4\], target = 6
>>  输出:\[1,2\]
>> 示例3 
>>  输入:nums = \[3,3\], target = 6
>>  输出:\[0,1\]
>>>提示
>>>* 2 \<= nums.length \<= $10^3$
>>>* $-10^9$ \<= nums\[i\] \<= $10^9$
>>>* $-10^9$ \<= target \<= $10^9$
>>>* 只会存在一个有效答案

## 可以在这里确认
->[LeetCode 1 两数之和](https://leetcode-cn.com/problems/two-sum/)


## 解题思路
关键点在于 nums\[i\] + nums\[j\] = target,即等于 **nums\[i\] = target - nums\[j\]**。可以做个哈希表,表里面存储以**target - nums\[j\](目标元素)**  为键,当前**索引**为值。在迭代并将元素插入到表中的同时,进行检查表中是否已经存在当前元素所对应的目标元素。如果存在,即找到对应解,立即返回。

## Python
Python里面的**字典**就是利用哈希表存储的,可以拿来直接使用。
```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        d = dict()
        for i in range(len(nums)):
            if nums[i] in d:
                return [d[nums[i]], i]
            else:
                d[target - nums[i]] = i
```
执行用时:44 ms, 在所有 Python3 提交中击败了40.28%的用户
内存消耗:14.9 MB, 在所有 Python3 提交中击败了48.49%的用户

## C++
C++ 的话,可以用unordered_map实现。
```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        std::unordered_map<int, int> dict;
        std::vector<int> result;
        for(int i = 0; i < nums.size(); ++i){
            auto it = dict.find(nums[i]);
            if(it != dict.end()){
                result.push_back(dict[nums[i]]);
                result.push_back(i);
                return result;
            }
            else{
                dict.insert(std::pair<int, int>(target - nums[i], i));
            }
        }
        return result;
    }
};
```
执行用时:4 ms, 在所有 C++ 提交中击败了93.32%的用户
内存消耗:8.6 MB, 在所有 C++ 提交中击败了80.96%的用户

## Kotlin
```kotlin
class Solution {
    fun twoSum(nums: IntArray, target: Int): IntArray {
        val dict: MutableMap<Int, Int> = mutableMapOf<Int, Int>()
        var idnex1 = 0
        var idnex2 = 1
        loop@for(i in 0 until nums.size step 1){
            if(dict.get(nums[i]) != null){
                idnex1 = dict[nums[i]]!!
                idnex2 = i
                break@loop
            }
            else{
                dict[target - nums[i]] = i
            }
        }
        return intArrayOf(idnex1, idnex2)
    }
}
```
执行用时:216 ms, 在所有 Kotlin 提交中击败了81.47%的用户
内存消耗:35.4 MB, 在所有 Kotlin 提交中击败了88.25%的用户