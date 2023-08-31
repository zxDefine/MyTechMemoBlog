# 实现strStr()
## 题目
>实现 strStr() 函数。
>给定一个 haystack 字符串和一个 needle 字符串,在 haystack 字符串中找出 needle 字符串出现的>第一个位置 (从0开始)。如果不存在,则返回  -1。
>>示例 1:
>>输入: haystack = "hello", needle = "ll"
>>输出: 2
>>
>>示例 2:
>>输入: haystack = "aaaaa", needle = "bba"
>>输出: -1

## 可以在这里确认
->[LeetCode 28 实现strStr()](https://leetcode-cn.com/problems/implement-strstr/)

## 思考
这个题第一个想到的就是使用已经写好了的轮子,使用轮子是工作中非常重要的常用的方式。当然这里既然是算法练习,那当然不能只是调用轮子这么简单。首先能想到的最直接最好理解的方法,就是遍历haystack字符串,一个字符一个字符的查找下去,看看从这个字符开始有不有跟needle一样的字符串就可以了。Python里面有切片语法,会简单很多,C++稍微复杂一点。

## 解题思路
遍历haystack字符串,获取每个字符并且这个字符开始的needle长度的字符串跟needle比较。**需要注意的是当needle是空字符的时候,需要则呢处理,C语言的strStr()是返回0,即开头。**

## Python实现
```python
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        #前人的车轮,如果不是为了练习,其实应该多用车轮的,避免重复创造
        #return haystack.find(needle)
        
        if not needle: return 0
        needleLength = len(needle)
        maxLoop = len(haystack) - needleLength + 1
        for i in range(maxLoop):
            if haystack[i:i + needleLength] == needle:
                return i
        return -1
```

执行用时 :48 ms, 在所有 Python3 提交中击败了79.03%的用户
内存消耗 :14 MB, 在所有 Python3 提交中击败了5.73%的用户

## C++实现
```cpp
class Solution 
{
public:
    int strStr(string haystack, string needle) 
    {
        if(needle.empty())  return 0;
        
        int needleLength = needle.size();
        int maxLoop = haystack.size() - needleLength + 1;
        
        for(int i = 0; i <= maxLoop; ++i)
        {
            string tmpStr = haystack.substr(i, needleLength);
            if(tmpStr == needle)    return i;
        }
        
        return -1;
    }
};
```

执行用时 :8 ms, 在所有 C++ 提交中击败了69.08%的用户
内存消耗 :9.1 MB, 在所有 C++ 提交中击败了79.13%的用户