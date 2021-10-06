# 宝石与石头
## 题目
> 给定字符串`J` 代表石头中宝石的类型,和字符串 `S`代表你拥有的石头。 `S` 中每个字符代表了一种你拥有的石头的类型,你想知道你拥有的石头中有多少是宝石。
> `J` 中的字母不重复,`J` 和 `S`中的所有字符都是字母。字母区分大小写,因此`"a"`和`"A"`是不同类型的石头。
> 
>> 示例
>> **输入:**  `J`= `"aA"`, `S` = `"aAAbbbb"`
>> **输出:** `3`

## 可以在这里确认
->[LeetCode 771 宝石与石头](https://leetcode-cn.com/problems/jewels-and-stones/)

## 思考
这里我一上来就最直接的想到了暴力的双循环,但是考虑到效率问题,肯定不可能这么简单,但后看题目下的提示哈希表。就想到了还是建立哈希表,然后在哈希表里查找,时间复杂度O(1)。还是用空间换取时间。

## 解题思路
关键在第一步,建立哈希表。然后遍历哈希表,然后得出结果。

## Python实现
使用Python自带的**字典**。
```python
class Solution:
    def numJewelsInStones(self, J, S):
        """
        :type J: str
        :type S: str
        :rtype: int
        """

        # create a dictionary
        dict = {}

        # create a hash table

        for c in J:
            dict[c] = 0
        # search
        for c in S:
            if c in dict:
                dict[c] += 1

        sum = 0
        for value in dict.values():
            sum += value

        return sum
```
**在LeetCode上跑了48ms**

## C++实现
```cpp
class Solution 
{
public:
    int numJewelsInStones(string J, string S) 
    {
        // create a dictionary
        std::unordered_map<char, int> dict;

        // create a hash table
        for(int i = 0; i < J.size(); ++i)
        {
            dict.insert(std::pair(J[i], 0));
        }

        // search
        for(int i = 0; i < S.size(); ++i)
        {
            auto it = dict.find(S[i]);
            if(it != dict.end())
            {
                ++((*it).second);
            }
        }

        int sum = 0;
        for(auto& item : dict)
        {
            sum += item.second;
        }

        return sum;
    }
};
```
**在LeetCode上跑了4ms**