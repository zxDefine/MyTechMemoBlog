# 二进制求和
## 题目
>给你两个二进制字符串，返回它们的和（用二进制表示）。
>输入为**非空**字符串且只包含数字 1 和 0。
>>示例 1:
>>	输入: a = "11", b = "1"
>>	输出: "100"
>>
>>示例 2:
>>	输入: a = "1010", b = "1011"
>>	输出: "10101"
>>
>>>提示:
>>>* 每个字符串仅由字符 '0' 或 '1' 组成。
>>>* 1 \<= a.length, b.length \<= 10^4^
>>>* 符串如果不是 "0" ，就都不含前导零。

## 可以在这里确认
->[LeetCode 67 二进制求和](https://leetcode-cn.com/problems/add-binary/)

## 思考
这个题比较简单，使用反向双指针遍历一遍就好了，直接上方法。

## 解题思路
1. 创建两个Index分别从两个字符串的最后位置开始向前遍历
2. 每遍历一个字符，Index就减一，如果Index小于0的话，自动用“0”补位。
3. 判断遍历的每个字符的相加情况，然后放入新的字符串中即可

## Python

```python
class Solution:
    def addBinary(self, a: str, b: str) -> str: 
        loopNum = max(len(a), len(b))
        lastIdxA = len(a) - 1
        lastIdxB = len(b) - 1
        resList = []
        flg = False
        for i in range(loopNum):
            NumA = "0" if lastIdxA < 0 else a[lastIdxA]
            NumB = "0" if lastIdxB < 0 else b[lastIdxB]
            if NumA == "0" and NumB == "0":
                if flg: resList.append("1")
                else: resList.append("0")
                flg = False
            elif NumA == "1" and NumB == "1":
                if flg: resList.append("1")
                else: resList.append("0")
                flg = True
            else:
                if flg:
                    resList.append("0")
                    flg = True
                else:
                    resList.append("1")
                    flg = False
            lastIdxA -= 1
            lastIdxB -= 1
        if flg:
            resList.append("1")
        return "".join(resList[::-1])
```

执行用时：44 ms, 在所有 Python3 提交中击败了55.91%的用户
内存消耗：14.9 MB, 在所有 Python3 提交中击败了55.64%的用户

## C++

```cpp
class Solution {
public:
    string addBinary(string a, string b) {
        int loopNum = a.length() > b.length() ? a.length() : b.length();
        int lastIdxA = a.length() - 1;
        int lastIdxB = b.length() - 1;
        vector<char> resList;
        bool flg = false;
        for(int i = 0; i < loopNum; ++i){
            char NumA = lastIdxA < 0 ? '0' : a[lastIdxA];
            char NumB = lastIdxB < 0 ? '0' : b[lastIdxB];
            if('0' == NumA && '0' == NumB){
                if(flg) resList.push_back('1');
                else resList.push_back('0');
                flg = false;
            }
            else if('1' == NumA && '1' == NumB){
                if(flg) resList.push_back('1');
                else resList.push_back('0');
                flg = true;
            }
            else{
                if(flg){
                    resList.push_back('0');
                    flg = true;
                }
                else{
                    resList.push_back('1');
                    flg = false;
                }
            }
            lastIdxA--;
            lastIdxB--;
        }
        if(flg) resList.push_back('1');
        string res = "";
        for(auto it = resList.rbegin(); it != resList.rend(); ++it){
            res += *it;
        }
        return res;
    }
};
```

执行用时：8 ms, 在所有 C++ 提交中击败了11.27%的用户
内存消耗：6.2 MB, 在所有 C++ 提交中击败了64.17%的用户

## Kotlin

```kotlin
class Solution {
    fun addBinary(a: String, b: String): String {
        val loopNum = if(a.length > b.length) a.length else b.length
        var lastIdxA = a.length - 1
        var lastIdxB = b.length - 1
        var resList = mutableListOf<Char>()
        var flg = false
        for(i in 0 until loopNum step 1){
            val NumA = if(lastIdxA < 0) '0' else a[lastIdxA]
            val NumB = if(lastIdxB < 0) '0' else b[lastIdxB]
            if('0' == NumA && '0' == NumB){
                if(flg) resList.add('1')
                else resList.add('0')
                flg = false
            }else if('1' == NumA && '1' == NumB){
                if(flg) resList.add('1')    
                else resList.add('0')
                flg = true
            }else{
                if(flg){
                    resList.add('0')
                    flg = true
                }else{
                    resList.add('1')
                    flg = false
                }
            }
            lastIdxA -= 1
            lastIdxB -= 1
        }
        if(flg) resList.add('1')
        var resStr = ""
        for(c in resList.reversed()){
            resStr += c
        }
        return resStr
    }
}
```

执行用时：240 ms, 在所有 Kotlin 提交中击败了8.70%的用户
内存消耗：35.4 MB, 在所有 Kotlin 提交中击败了8.70%的用户