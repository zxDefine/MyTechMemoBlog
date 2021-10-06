# 回文数
## 题目
> 给你一个整数 x ,如果 x 是一个回文整数,返回 true ;否则,返回 false 。
> 回文数是指正序(从左向右)和倒序(从右向左)读都是一样的整数。例如,121 是回文,而 123 不是。
>
>>示例1:
>>输入:x = 121
>>输出: true
>>示例2:
>>输入:x = -121
>>输出: false
>>解释: 从左向右读,为-121。从右向左读,为121-。所以它不是一个回文数。
>>示例3:
>>输入: x = 10
>>输出: false
>>解释: 从右向左读, 为 01 。因此它不是一个回文数。
>>示例4:
>>输入:x = -101
>>输出:false
>>
>>>提示:
>>>* -2^31^ \<= x \<= 2^31^ - 1
>>>
>>>进阶:你能不将整数转为字符串来解决这个问题吗?

## 可以在这里确认
->[LeetCode 9 回文数](https://leetcode-cn.com/problems/palindrome-number/)

## 思考
最直接的想法当然就是按照回文数的定义,把一个数转换成字符串然后正序倒序各一串,对比两个字符串是否一样。所以用Python的话非常简单。在评论里有一个一条语句就能完成的,如下:

```python
class Solution:
    def isPalindrome(self, x: int) -> bool:
        return str(x) == str(x)[::-1]
```

执行用时: 84ms,在所有Python3提交中击败 88.59%的用户。
内存消耗: 14.1MB,在所有Python3提交中击败5.01%的用户。

题目里面有个小的追加条件就是**不使用字符串**。官方给出的解法是**反转一半**,非常不错的想法,果然还是网上厉害的人很多,很多奇思妙想。

官解思路如下

> 将数字本身反转,然后将反转后的数字与原始数字进行比较,如果他们相同,那么这个数字就是回文数。但是,如果反转后的数字大于了int.MAX,将遇到整数溢出问题。
>
> 按照这个想法,为了避免数字反转可能导致的溢出问题,为什么不考虑只反转int数字的一半?因为如果是回文数的话,后半部分反转后应该与原来数字的前半部分相同

## 解题思路
按照官解的想法大致可以分为以下几步:
**首先,数字不能是负数,负数的话直接返回false,数字如果在0到9之间,因为只有1位,所以直接返回true。**
**其次,数字开始反转,大概就是先%10,在/10,可以得到最后一位数,并且移除最后一位数。如此循环。**
**最后,比较当原始数字比反转后的数字小的时候,就可以循环结束,然后判断。**
最后判断循环结束的方法确实很好,只需要比较大小就能结束。

## Python

```python
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        if x < 10:
            return True
        
        x1 = x % 10
        x = x // 10
        
        if 0 == x1:
            return False
        
        while(x > x1):
            tmp = x % 10
            x = x // 10
            x1 = x1 * 10 + tmp
            
        return x == x1 or x == (x1 // 10)
```
执行用时:76 ms, 在所有 Python3 提交中击败了58.47%的用户
内存消耗:14.8 MB, 在所有 Python3 提交中击败了77.86%的用户

## C++

```cpp
class Solution {
public:
    bool isPalindrome(int x) {
        if(x < 0)   return false;
        if(x < 10)  return true;

        int x1 = x % 10;
        x = x / 10;
        
        if(0 == x1) return false;
        
        while(x > x1){
            int tmp = x % 10;
            x1 = x1 * 10 + tmp;
            x = x / 10;
        }
        
        return (x == x1) || (x == (x1 / 10));
    }
};
```
执行用时:12 ms, 在所有 C++ 提交中击败了76.03%的用户
内存消耗:5.7 MB, 在所有 C++ 提交中击败了80.47%的用户

## Kotlin

```kotlin
class Solution {
    fun isPalindrome(x: Int): Boolean {
        if(x < 0) return false
        if(x < 10) return true

        var x1: Int = x % 10
        var tmpX: Int = x / 10

        if(0 == x1) return false

        while(tmpX > x1){
            var tmp = tmpX % 10
            tmpX = tmpX / 10
            x1 = x1 * 10 + tmp
        }

        return tmpX == x1 || tmpX == (x1 / 10)
    }
}
```
执行用时:264 ms, 在所有 Kotlin 提交中击败了48.48%的用户
内存消耗:33.9 MB, 在所有 Kotlin 提交中击败了99.24%的用户
