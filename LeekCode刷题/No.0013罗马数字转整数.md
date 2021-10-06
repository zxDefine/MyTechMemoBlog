# 罗马数字转整数
## 题目
> 罗马数字包含以下七种字符: I, V, X, L,C,D 和 M。
>
>> 字符 数值
>> I = 1
>> V = 5
>> X = 10
>> L = 50
>> C = 100
>> D = 500
>> M = 1000
>
> 例如, 罗马数字 2 写做 II ,即为两个并列的 1。12 写做 XII ,即为 X + II 。 27 写做  XXVII, 即为 XX + V + II 。
>
> 通常情况下,罗马数字中小的数字在大的数字的右边。但也存在特例,例如 4 不写做 IIII,而是 IV。数字 1 在数字 5 的左边,所表示的数等于大数 5 减小数 1 得到的数值 4。同样地,数字 9 表示为 IX。这个特殊的规则只适用于以下六种情况:
>
>* I 可以放在 V (5) 和 X (10) 的左边,来表示 4 和 9。
>* X 可以放在 L (50) 和 C (100) 的左边,来表示 40 和 90。 
>* C 可以放在 D (500) 和 M (1000) 的左边,来表示 400 和 900。
>* 给定一个罗马数字,将其转换成整数。输入确保在 1 到 3999 的范围内。
>
>> 示例 1:
>> 输入: "III"
>> 输出: 3
>>
>> 示例 2:
>> 输入: "IV"
>> 输出: 4
>>
>> 示例 3:
>> 输入: "IX"
>> 输出: 9
>>
>> 示例 4:
>> 输入: "LVIII"
>> 输出: 58
>> 解释: L = 50, V= 5, III = 3.
>>
>> 示例 5:
>> 输入: "MCMXCIV"
>> 输出: 1994
>> 解释: M = 1000, CM = 900, XC = 90, IV = 4.
>> 
>>> 提示
>>>* 1 \<= s.length \<= 15
>>>* s 仅含字符 ('I', 'V', 'X', 'L', 'C', 'D', 'M')
>>>* 题目数据保证 s 是一个有效的罗马数字,且表示整数在范围 \[1, 3999\] 内
>>>* 题目所给测试用例皆符合罗马数字书写规则,不会出现跨位等情况。
>>>* IL 和 IM 这样的例子并不符合题目要求,49 应该写作 XLIX,999 应该写作 CMXCIX 。
>>>* 关于罗马数字的详尽书写规则,可以参考 [罗马数字 - Mathematics](https://b2b.partcommunity.com/community/knowledge/zh_CN/detail/10753/%E7%BD%97%E9%A9%AC%E6%95%B0%E5%AD%97#knowledge_article) 。

## 可以在这里确认
->[LeetCode 13 罗马数字转整数](https://leetcode-cn.com/problems/roman-to-integer/)

## 思考
这个题,我一上来想到的就是最直观的解法,把所有可能的组合字符找出来,例如“IV”,“XL”,“CM”之类的,然后去跟得到的字符串比较,有组合字符的先把组合字符的值求出来,在求单个字符的值。评论里解法里都有很多非常好的类似算法。不过在思考的过程中,我发现凡是需要组合显示的字符都可以这么来理解,就是右边的那个字符需要减去左边的那个字符的值。所以我有个更好的想法大概如下。

## 解题思路
1. 建立基本字符字典,不需要组合字符
2. 将得到的字符串倒序后,重新排列,例如“IXLV”->“VLXI”
3. 然后对照字典把每个字符的值找出来,放进数组中
4. 遍历数值数组,凡是靠后面的数值比前面的数值小的话,将那个数值变为负数
5. 然后将数组所有元素相加

## Python

```python
class Solution:
    def romanToInt(self, s: str) -> int:
        #1
        d = {'I' : 1, 'V' : 5,'X' : 10,'L' : 50,'C' : 100,'D' : 500,'M' : 1000}
        #2,3
        newNumList = [d[x] for x in s[::-1]]
        
        maxNum = 0
        index = 0
        #4
        for i in newNumList:
            if maxNum < i:
                maxNum = i
            if newNumList[index] < maxNum:
                newNumList[index] = -newNumList[index]
            index += 1
        #5
        return sum(newNumList)
```

执行用时:72 ms, 在所有 Python3 提交中击败了12.24%的用户
内存消耗:14.7 MB, 在所有 Python3 提交中击败了95.14%的用户

## C++

```cpp
class Solution {
public:
    int romanToInt(string s) {
        map<char, int> charValue = {{'I', 1}, {'V', 5}, {'X', 10}, {'L', 50}, {'C', 100}, {'D', 500}, {'M', 1000},};
        vector<int> valueList;
        
        reverse(s.begin(), s.end());
        int listLength = s.size();
        valueList.reserve(listLength);
        for(int i = 0; i < listLength; ++i){
            valueList.push_back(charValue[s[i]]);
        }
        
        int maxNum = 0;
        for(int i = 0; i < listLength; ++i){
            if(maxNum < valueList[i]) maxNum = valueList[i];
            if(valueList[i] < maxNum) valueList[i] = -valueList[i];
        }
        
        int sum = 0;
        for(int i = 0; i < listLength; ++i){
            sum += valueList[i];            
        }
        
        return sum;
    }
};
```

执行用时:24 ms, 在所有 C++ 提交中击败了29.90%的用户
内存消耗:8.4 MB, 在所有 C++ 提交中击败了22.80%的用户

## Kotlin

```kotlin
class Solution {
    fun romanToInt(s: String): Int {
        val map:Map<Char, Int> = mapOf('I' to 1, 'V' to 5, 'X' to 10, 'L' to 50, 'C' to 100, 'D' to 500, 'M' to 1000)
        val newStr: String = s.reversed()
        val valList = mutableListOf<Int>()
        for(str in newStr){
            map[str]?.let{it->
                valList.add(it)
            }
        }
        var tmpNum = 0
        for(i in 0 until valList.size - 1 step 1){
            if(tmpNum < valList[i]) tmpNum = valList[i]
            if(valList[i] < tmpNum) valList[i] = -valList[i]
        }

        return valList.sum()
    }
}
```

执行用时:24 ms, 在所有 C++ 提交中击败了29.90%的用户
内存消耗:8.4 MB, 在所有 C++ 提交中击败了22.80%的用户

