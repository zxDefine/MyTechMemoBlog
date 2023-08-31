# 最长公共前缀
## 题目
> 编写一个函数来查找字符串数组中的最长公共前缀。
> 如果不存在公共前缀,返回空字符串 ""。
> 
>> 示例 1:
>> 输入: strs = \["flower","flow","flight\]
>> 输出: "fl"
>>
>> 示例 2:
>> 输入:strs = \["dog","racecar","car"\]
>> 输出: ""
>> 解释: 输入不存在公共前缀。
>>
>>> 提示:
>>>* 0 \<= strs.length \<= 200
>>>* 0 \<= strs\[i\].length \<= 200
>>>* strs\[i\] 仅由小写英文字母组成

## 可以在这里确认
->[LeetCode 14 最长公共前缀](https://leetcode-cn.com/problems/longest-common-prefix/)


## 解题思路

1. 把第一个字符串取出来,然后按照前1个字符,前2个字符,前3个字符,以此类推遍历一遍字符串,例如"flower"->\["f","fl","flo","flow","flowe","flower"\]
2. 然后就是简单的把上面得到的字符串,跟得到的需要比较的字符串全部遍历一遍
3. 如果找到了,那个字符串就是答案,没找到就返回空字符串

## Python

```python
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if 0 == len(strs):
            return ""
        checkStrList = list()
        for i in range(len(strs[0])):
            checkStrList.append(strs[0][0:(i + 1)])  
        targetStrs = strs[1:]
        resStr = ""
        for checkStr in checkStrList:
            bForceEnd = False
            for targetStr in targetStrs:
                if not targetStr.startswith(checkStr):
                    bForceEnd = True
                    break
            if bForceEnd:
                break
            resStr = checkStr
        return resStr
```

执行用时:44 ms, 在所有 Python3 提交中击败了50.73%的用户
内存消耗:14.9 MB, 在所有 Python3 提交中击败了83.84%的用户

## C++

```cpp
class Solution {
public:
    string longestCommonPrefix(vector<string>& strs) {
        if(0 == strs.size())    return "";
        
        vector<string> checkStrs;
        for(auto i = 0; strs[0][i] != '\0'; ++i){
            checkStrs.push_back(strs[0].substr(0, i + 1));
        }
        
        string resStr = "";
        for(auto i = 0; i < checkStrs.size(); ++i){
            bool bForceEnd = false;
            for(auto j = 1; j < strs.size(); ++j){
                std::size_t found = strs[j].find(checkStrs[i]);
                if(found == std::string::npos || found != 0){
                    bForceEnd = true;
                    break;
                }
            }
            if(bForceEnd) break;
            resStr = checkStrs[i];
        }
        
        return resStr;
    }
};
```

执行用时:4 ms, 在所有 C++ 提交中击败了89.31%的用户
内存消耗:9.2 MB, 在所有 C++ 提交中击败了21.68%的用户

## Kotlin

```kotlin
class Solution {
    fun longestCommonPrefix(strs: Array<String>): String {
        if(0 == strs.size) return ""

        val checkStrs = MutableList<String>(strs[0].length){""}
        for(i in 0 until strs[0].length step 1){
            checkStrs[i] = strs[0].slice(0..i)
        }

        var res = ""
        loop_1@for(i in checkStrs){
            var bForceEnd = false
            loop_2@for(j in strs){
                if(j.startsWith(i) == false){
                    bForceEnd = true
                    break@loop_2
                }
            }
            if(bForceEnd) break@loop_1
            res = i
        }
        return res
    }
}
```
执行用时:212 ms, 在所有 Kotlin 提交中击败了61.06%的用户
内存消耗:35.4 MB, 在所有 Kotlin 提交中击败了19.47%的用户
