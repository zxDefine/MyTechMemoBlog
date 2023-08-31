# 删除排序数组中的重复项
## 题目
> 给定一个**排序数组**,你需要在**原地**删除重复出现的元素,使得每个元素只出现一次,返回移除后数组的新长度。
> **不适用额外的数组空间,你必须在原地修改输入数组并在使用O(1)额外空间的条件下完成**
>> 示例 1:
>> 给定数组 nums = [1,1,2], 函数应该返回新的长度 2, 并且原数组 nums 的前两个元素被修改为 1, 2。 
>> 你不需要考虑数组中超出新长度后面的元素。
>>
>> 示例 2:
>> 给定 nums = [0,0,1,1,1,2,2,3,3,4],函数应该返回新的长度 5, 并且原数组 nums 的前五个元素被修改为 0, 1, 2, 3, 4。
>>
>> 你不需要考虑数组中超出新长度后面的元素。

## 可以在这里确认
->[LeetCode 26 删除排序数组中的重复项](https://leetcode-cn.com/problems/remove-duplicates-from-sorted-array/)

## 思考
一眼看到这个题目,发现有两个非常重要的限制条件,一个是已经排序了的**排序数组**,另一个是必须在原数组的**内存地址**上操作的**原地**修改。简单说就是不能在新建一个数组来做临时存储或者最后结果。这第二个条件限制了我的解题思路,思来想去我自己好像只有一种方法比较好,就是使用两个**“指针”**或者说**“index”**,遍历数组,然后把不重复的数字全部集中到数组前面,也就是交换,把重复的删除也好,直接放到数组后面也行,因为最后检查应该就是用返回的新长度去遍历交换过后的数组,然后跟答案比对。(最后一句纯属个人推测)

看了一眼官解,跟我自己的想法基本相似,看来官解也没有其他更好的方法了吧。

## 解题思路
首先,需要两个指针或是索引,一个我们叫快指针,一个叫慢指针,起始都指向位置0。
其次,用快指针遍历数组,用快指针跟慢指针所指向的地方判断相等,如果相等,说明是重复项,那快指针就后移一位,跳过重复项,如果不相等,就说明不是重复项,这个时候把慢指针后移一位。然后,把快指针所指的数字赋值到移动后的慢指针的地方,然后快指针后移一位。然后以此类推,直到快指针遍历完数组。
最后,返回慢指针加1,就是新长度

注意**需要判断数组不能为空**。

## Python实现
```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        if 0 == len(nums):
            return 0
        
        fastIndex = 0
        slowIndex = 0
        while fastIndex < len(nums):
            if nums[slowIndex] != nums[fastIndex]:
                slowIndex += 1
                nums[slowIndex] = nums[fastIndex]
            fastIndex += 1
                
        return slowIndex + 1
```
执行用时:44 ms, 在所有 Python3 提交中击败了79.81%的用户
内存消耗:15.7 MB, 在所有 Python3 提交中击败了73.24%的用户

## C++实现
```cpp
class Solution 
{
public:
    int removeDuplicates(vector<int>& nums) 
    {
        if(0 == nums.size())
        {
            return 0;            
        }
        
        int fastIndex = 0;
        int slowIndex = 0;
        
        for(; fastIndex < nums.size(); ++fastIndex)
        {
            if(nums[slowIndex] != nums[fastIndex])
            {
                nums[++slowIndex] = nums[fastIndex];                
            }
        }
        
        return slowIndex + 1;
    }
};
```
执行用时: 32ms,在所有C++提交中击败 76.06%的用户
内存消耗: 10MB,在所有C++提交中击败76.56%的用户

壮大我C++