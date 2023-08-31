# 合并两个有序链表
## 题目
>将两个有序链表合并为一个新的有序链表并返回。新链表是通过拼接给定的两个链表的所有节点组>成的。 
>
>>  示例:
>>	输入:1->2->4, 1->3->4
>>	输出:1->1->2->3->4->4

## 可以在这里确认
->[LeetCode 21 合并两个有序链表](https://leetcode-cn.com/problems/merge-two-sorted-lists/)

## 思考
对于这道题,我的想法过于直接了,没有任何技巧,简单来说就是同时遍历两个链表,比较每一个链表的元素,然后排列链接起来而已。
官解里面,有个递归算法,简单解释就是两个链表,相当于其中一个链表的表头加上剩下的所有元素:较小的表头+函数:返回最小的元素。

## 解题思路
这一次,分成两部分,一部分是自己写的算法,或者算不上算吧,代码吧,一部分是从官解以及题解里面学来的递归算法。

## 自己的代码
### Python实现
自己的代码只实现了Python的,C++没有写,步骤类似。
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        if None == l1:
            return l2
        if None == l2:
            return l1
        
        resNode = None

        if l1.val <= l2.val:
            resNode = l1
            l1 = l1.next
        else:
            resNode = l2
            l2 = l2.next
            
        tempNode = resNode

        while 1:
            if l1 != None and l2 != None:
                if l1.val <= l2.val:
                    tempNode.next = l1
                    l1 = l1.next
                else:
                    tempNode.next = l2
                    l2 = l2.next
                
            if None == l1 and None == l2:
                break
            if None == l1:
                if None == tempNode.next:
                    tempNode.next = l2
                else:
                    tempNode.next.next = l2
                break
            if None == l2:
                if None == tempNode.next:
                    tempNode.next = l1
                else:
                    tempNode.next.next = l1
                break 
                
            tempNode = tempNode.next
            
        return resNode
```

执行用时 :64 ms, 在所有 Python3 提交中击败了36.45%的用户
内存消耗 :13.9 MB, 在所有 Python3 提交中击败了5.66%的用户

可以看出,我自己的解法比较复杂,并且代码冗长。

## 官解以及题解学来的代码
### Python实现
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        if l1 and l2:
            if l1.val > l2.val:
                l1,l2 = l2,l1#交换,始终保持了l1是最小的
            l1.next = self.mergeTwoLists(l1.next, l2)
        return l1 or l2
```

执行用时 :48 ms, 在所有 Python3 提交中击败了96.07%的用户
内存消耗 :13.9 MB, 在所有 Python3 提交中击败了5.66%的用户

这是题解里面一个大神写的Python代码,瞧瞧,人家写的多么的简小精干,而且还深得递归真谛,这里膜拜学习。

### C++实现
```cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
        if(l1 && l2)
        {
            if(l1->val > l2->val)
            {
                ListNode* temP = l2;
                l2 = l1;
                l1 = temP;
            }
            
            l1->next = this->mergeTwoLists(l1->next, l2);
        }
        return l1 ? l1 : l2;
    }
};
```

执行用时 :8 ms, 在所有 C++ 提交中击败了98.07%的用户
内存消耗 :8.7 MB, 在所有 C++ 提交中击败了98.96%的用户

这里的C++代码,是仿造上面Python的做法写的,基本思想是一样,采用递归算法。基本思想是一样,采用递归算法。