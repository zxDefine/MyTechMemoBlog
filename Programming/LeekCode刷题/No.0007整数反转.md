# 整数反转
## 题目
> 给你一个**32**位的有符号整数x,返回将x中的数字部分反转后的结果。
> 如果反转后整数超过32位的有符号整数的范围\[-2^31^, 2^31^ - 1\] ,就返回 0。
> **假设环境不允许存储 64 位整数(有符号或无符号)**。
>> 示例1
>> 输入:x = 123
>> 输出:321
>> 示例2
>> 输出:x = -123
>> 输出:-321
>> 示例3
>> 输入:x = 120
>> 输出:21
>> 示例4
>> 输入:x = 0
>> 输出:0
>>> 提示
>>>* -2^31^ \<= x \<= 2^31^ - 1


## 可以在这里确认
->[LeetCode 7 整数反转](https://leetcode-cn.com/problems/reverse-integer/)


## 解题思路
首先,循环倒序求出每一位数字。然后叠加到最后结果上,最后需要判断不要超出32位的有符号整数的表示范围。

## Python

```python
class Solution:
    def reverse(self, x: int) -> int:
        tempX = x
        bNegative = False
        intMax = pow(2, 31) - 1
        intMin = -pow(2, 31)
        
        if tempX < 0:
            tempX = abs(tempX)
            bNegative = True
            
        res = 0
        while tempX != 0:
            num = tempX % 10
            tempX = tempX // 10
            res = res * 10 + num
            if res >= intMax or res <= intMin:
                return 0
            
        if bNegative:
            res *= -1
            
        return res
```
执行用时:40 ms, 在所有 Python3 提交中击败了77.39%的用户
内存消耗:14.9 MB, 在所有 Python3 提交中击败了16.63%的用户

## C++

```cpp
class Solution {
public:
    int reverse(int x) {
        int num = 0;
        int tempX = x;
        int res = 0;
        int intMax = pow(2, 31) - 1;
        int intMin = -pow(2, 31);
        
        while(tempX != 0){
            num = tempX % 10;
            tempX = int(tempX / 10);
            // intMax = 2147483647
            if((res > intMax / 10) || ((res == intMax / 10) && (num > 7))){
                return 0;
            }
            // intMin = -2147483648
            if((res < intMin / 10) || ((res == intMin / 10) && (num < -8))){
                return 0;
            }
            res = res * 10 + num;
        }
        return res;
    }
};
```

执行用时:8 ms, 在所有 C++ 提交中击败了5.32%的用户
内存消耗:5.8 MB, 在所有 C++ 提交中击败了59.02%的用户

## Kotlin

```kotlin
class Solution {
    fun reverse(x: Int): Int {
        var num = 0
        var tempX = x
        var res = 0
        val intMax = Int.MAX_VALUE
        val intMin = Int.MIN_VALUE


        while(tempX != 0){
            num = tempX % 10
            tempX = tempX / 10
            // intMax = 2147483647
            if((res > intMax / 10) || ((res == intMax / 10) && (num > 7))){
                return 0;
            }
            // intMin = -2147483648
            if((res < intMin / 10) || ((res == intMin / 10) && (num < -8))){
                return 0;
            }
            res = res * 10 + num
        }

        return res
    }
}
```

执行用时:180 ms, 在所有 Kotlin 提交中击败了38.75%的用户
内存消耗:32.4 MB, 在所有 Kotlin 提交中击败了83.13%的用户
