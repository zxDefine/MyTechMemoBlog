# 有效的括号
## 题目
>给定一个只包括 '\(','\)','\{','\}','\[','\]' 的字符串s,判断字符串是否有效。
>有效字符串需满足:
> 1. 左括号必须用相同类型的右括号闭合。
> 2. 左括号必须以正确的顺序闭合。
>
>>示例 1:
>>	输入: s = "\(\)"
>>	输出: true
>>
>>示例 2:
>>	输入: s = "\(\)\[\]\{\}"
>>	输出: true
>>
>>示例 3:
>>	输入: s = "\(\]"
>>	输出: false
>>
>>示例 4:
>>	输入: s = "\(\[\)\]"
>>	输出: false
>>
>>示例 5:
>>	输入: s = "\{\[\]\}"
>>	输出: true
>>
>>>提示:
>>>* 1 \<= s.length \<= 104
>>>* s 仅由括号 '\(\)\[\]\{\}' 组成

## 可以在这里确认
->[LeetCode 20 有效的括号](https://leetcode-cn.com/problems/valid-parentheses/)

## 思考
看到这题的第一反应就是,正常来说,正确的括号的话,那么必须是一一对应的,那如果左括号为1,右括号为-1的话,那么和为0。从这个想法出发,我的解法如下。

## 解题思路
1. 先建立括号的对应值的字典,左为正,右为负。
2. 将获得的括号字符串转换成数字数组
3. 先求sum,不为零就说明不是有效括号,返回
4. 遍历数字数组,如果得到是正数,就push到新数字数组的最后
5. 如果是负数就判断,这个负数跟新数字数组的最后一位相加是否为零,是的话pop新数组最后一位
6. 遍历完新数组后，如果新数组里面还有数字存在，则说明没有一一对应，返回False

## Python

```python
class Solution:
    def isValid(self, s: str) -> bool:
        d = {'(' : 1, ')' : -1, '[' : 2, ']' : -2, '{' : 3, '}' : -3}
        changeNumList = [d[c] for c in s]
        if 0 != sum(changeNumList): return False
        tempList = list()
        for i in changeNumList:
            if i > 0:
                tempList.append(i)
            else:
                if len(tempList) > 0:
                    if (tempList[-1] + i) != 0:
                        return False
                    else:
                        tempList.pop()     
        if len(tempList) > 0:
            return False
        return True
```

执行用时:36 ms, 在所有 Python3 提交中击败了86.47%的用户
内存消耗:15 MB, 在所有 Python3 提交中击败了19.14%的用户

## C++

```cpp
class Solution {
public:
    bool isValid(string s) {
        map<char, int> changeNumMap = {{'(', 1}, {')', -1}, {'[', 2}, {']', -2}, {'{', 3}, {'}', -3}};
        vector<int> numList;
        int sum = 0;
        for(int i = 0; s[i] != '\0'; ++i){
            numList.push_back(changeNumMap[s[i]]);
            sum += numList[i];
        }
        if(sum != 0)    return false;
        vector<int> tempNumList;
        for(auto it = numList.begin(); it != numList.end(); ++it){
            if((*it) > 0) tempNumList.push_back((*it));
            else if(tempNumList.size() > 0){
                if((tempNumList.back() + (*it)) != 0) return false;
                else tempNumList.pop_back();
            }
        }
        if(tempNumList.size() > 0)  return false;
        return true;
    }
};
```

执行用时:0 ms, 在所有 C++ 提交中击败了100.00%的用户
内存消耗:6.4 MB, 在所有 C++ 提交中击败了5.19%的用户

## Kotlin

```kotlin
class Solution {
    fun isValid(s: String): Boolean {
        val changeNumMap = mapOf('(' to 1, ')' to -1, '[' to 2, ']' to -2, '{' to 3, '}' to -3)
        var numList = MutableList<Int>(s.length){0}
        for(i in 0 until s.length step 1) numList[i] = changeNumMap[s[i]]!!
        if(numList.sum() != 0) return false
        var tmpStack = ArrayDeque<Int>()
        for(i in numList){
            if(i > 0) tmpStack.push(i)
            else if(tmpStack.size > 0){
                if((tmpStack.peek() + i) != 0) return false
                else tmpStack.pop()
            }
        }
        if(tmpStack.size > 0) return false
        return true
    }
}
```

执行用时:280 ms, 在所有 Kotlin 提交中击败了10.65%的用户
内存消耗:34.7 MB, 在所有 Kotlin 提交中击败了17.59%的用户