# 加一
## 题目
>给定一个由整数组成的非空数组所表示的非负整数,在该数的基础上加一。
>最高位数字存放在数组的首位, 数组中每个元素只存储单个数字。你可以假设除了整数 0 之外,这个整数不会以零开头。
>
>>示例 1:
>>输入: [1,2,3]
>>输出: [1,2,4]
>>解释: 输入数组表示数字 123。
>>
>>示例 2:
>>输入: [4,3,2,1]
>>输出: [4,3,2,2]
>>解释: 输入数组表示数字 4321。

## 可以在这里确认
->[LeetCode 66 加一](https://leetcode-cn.com/problems/plus-one/)

## 思考
这个题简单来说,就是给一个数字,以数组的方式存储,数字的每一位各自存在数组中,然后把这个数字加一,再然后在以数组的方式存储,并且返回数组。重点就是在这个数组如果加一后发生进位的话,各种处理,比如9加一的话会变成10,再或者109加一会变成110,之类的这种临界值的处理。

这个题好像没有官解,我就主要写我自己的解法。
**在评论中看到一个关于Python的解法,非常有意思,因为Python的特性,可以简单的在数字,字符串之间来回转换,所以可以简单几句就能完成加一功能。**

## 解题思路
### Python的思路
python的很简单,将数组的值求出来,然后加一,得到的数字转换成字符串,然后遍历字符串每个字符转换成数字添加到数组中,返回即可。

### C++的思路
首先,分为两个大情况,一是数组最后一位数字小于9,一是数组最后一位等于9的情况。
其次,如果小于9,那么只需要最后一位数字加一,然后把每位赋值给新数组然后返回新数组即可。
如果等于9,又要分两种情况,最高位数字是不是等于9,是的话,需要在进一位,这一位是1。
最后,返回新数组。

## Python实现
```python
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        sum = 0
        for i in digits:
            sum = 10 * sum + i
        return [int(j) for j in str(sum + 1)]
```
执行用时 :68 ms, 在所有 Python3 提交中击败了23.08%的用户
内存消耗 :13.6 MB, 在所有 Python3 提交中击败了5.64%的用户

最后一句return语句是Python的语法,叫做**列表生成式**,这个在C++里面没有,因为我主要使用C++,所以这里稍微解释下这个语法。如果想看完整的介绍说明,可以去看看[廖雪峰大佬的官方网站](https://www.liaoxuefeng.com/wiki/1016959663602400/1017317609699776)里面对Python的列表生成式的介绍。

首先语法格式[*exp **for** x **in** list*],还可以加入**if**来筛选[*exp **for** x **in** list **if** exp*],for循环还可以嵌套[*x + y **for** x **in** listA **for** y **in** listB*]。**基本工作过程就是,遍历list里面的元素,然后赋值给x(和y),然后通过表达式exp得到一个新的值,最后把所有得到的新值以一个新列表的形式返回**。

理解了的话,这个Python的语法非常强大,能缩减不少代码。

## C++实现
```cpp
class Solution 
{
public:
    vector<int> plusOne(vector<int>& digits) 
    {
        int length = digits.size();
        vector<int> result;
        
        if((digits[length - 1] + 1) <= 9)
        {
            for(int i = 0; i < length; ++i)
            {
                if(i == length - 1)
                {
                    result.push_back(digits[length - 1] + 1);
                }
                else
                {
                    result.push_back(digits[i]);
                }
            }
        }
        else
        {
            bool bPlus = false;
            bool bInsertZero = true;
            for(int i = length - 1; i >= 0; --i)
            {
                if(9 == digits[i])
                {
                    if(bInsertZero)
                    {
                        bPlus = true;
                        result.insert(result.begin(), 0);
                    }
                    else
                    {
                        bPlus = false;
                        result.insert(result.begin(), 9);
                    }
                }
                else
                {
                    int tempNum = digits[i];
                    if(bPlus)
                    {
                        ++tempNum;
                        bPlus = false;
                        bInsertZero = false;
                    }
                    result.insert(result.begin(), tempNum);
                }
            }
            
            if(bInsertZero && bPlus)
            {
                result.insert(result.begin(), 1);
                bInsertZero = false;
                bPlus = false;
            }
        }
        
        return result;
    }
};
```
执行用时 :12 ms, 在所有 C++ 提交中击败了12.84%的用户
内存消耗 :8.5 MB, 在所有 C++ 提交中击败了42.69%的用户

嗯,虽然时间只击败了12.84%的用户,不过耗时只有12ms,果然壮大我C++。