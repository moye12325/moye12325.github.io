---
title: LeetCode 142. 环形链表
date: '2024-09-06 10:21:46'
categories:
  - LeetCode
tags:
  - LeetCode
---
[LeetCode 141. 环形链表](https://leetcode.cn/problems/linked-list-cycle/description/)

> 快慢指针，能相遇则说明有环

```java
public class Solution {
    public ListNode detectCycle(ListNode head) {
        ListNode fast = head;
        ListNode slow = head;
        
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                // 说明存在环
                slow = head;
                break;
            }
        }

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                // 第二次相遇
                return slow;
            }
        }

        return slow;
    }
}
```

[142. 环形链表 II](https://leetcode.cn/problems/linked-list-cycle-ii/description/)

> 给定一个链表的头节点  head，返回链表开始入环的第一个节点。如果链表无环，则返回 null。  
如果链表中有某个节点，可以通过连续跟踪 next 指针再次到达，则链表中存在环。为了表示给定链表中的环，评测系统内部使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。如果 pos 是 -1，则在该链表中没有环。注意：pos 不作为参数进行传递，仅仅是为了标识链表的实际情况。

## 思路分析

* 判断链表是否为空
* 判断链表是否有环
  * 有环，当第一次相遇时，将其中一个指针指向头节点，随后相同步伐后移，再次相遇时就是环的第一个节点
 
[参考链接](https://labuladong.online/algo/essential-technique/linked-list-skills-summary-2/#%E5%88%A4%E6%96%AD%E9%93%BE%E8%A1%A8%E6%98%AF%E5%90%A6%E5%8C%85%E5%90%AB%E7%8E%AF)


```java
public class Solution {
    public ListNode detectCycle(ListNode head) {
        ListNode fast = head;
        ListNode slow = head;

        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                // 说明存在环
                break;
            }
        }

        if (fast==null || fast.next == null) return null;

        slow = head;
        while (fast != slow) {
            slow = slow.next;
            fast = fast.next;
        }
        return slow;
    }
}
```

### 错误代码解析


```java
public class Solution {
    public ListNode detectCycle(ListNode head) {
        ListNode fast = head;
        ListNode slow = head;
        if (fast==null || fast.next == null) return null;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                // 说明存在环
                break;
            }
        }
        slow = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next;
            if (slow == fast) {
                // 第二次相遇
                break;
            }
        }
        return slow;
    }
}
```

第二次的 `while (fast != null && fast.next != null)` 循环存在逻辑上的错误

### 正确的 Floyd 判圈算法流程

1. **检测环是否存在**：
   - 使用两个指针，`fast` 和 `slow`，`fast` 每次移动两步，`slow` 每次移动一步。如果存在环，`fast` 和 `slow` 会在环内相遇；如果没有环，`fast` 会先到达链表的末尾，说明链表无环。

2. **找到环的起点**：
   - 当 `fast` 和 `slow` 第一次在环内相遇时，`slow` 被重置回链表的头节点，而 `fast` 保持在相遇点。接着，`slow` 和 `fast` 每次都只移动一步，直到它们再次相遇。第二次相遇的节点就是环的起点。

### 第二次的 `while` 循环


```java
while (fast != null && fast.next != null) {
    slow = slow.next;
    fast = fast.next;
    if (slow == fast) {
        // 第二次相遇
        break;
    }
}
```

#### 1. 误用的循环条件

 `while (fast != null && fast.next != null)`这个检查在第一次循环结束后已经不再需要了。实际上，第一次循环已经确定了链表是否有环，并且如果存在环，`fast` 和 `slow` 已经在环内相遇。

问题是，这段代码重新使用相同的条件来检查 `fast` 和 `slow`，试图寻找第二次相遇，这不符合 Floyd 算法的设计。在寻找环的起点时，不需要再检查 `fast != null && fast.next != null`，因为在有环的情况下，`fast` 永远不会变为 `null`。

#### 2. 不正确的步进方式

在寻找环的起点时，您让 `slow` 和 `fast` 以不同的速度移动：

```java
slow = slow.next;
fast = fast.next;
```

- **问题**：在 Floyd 算法中，当找到相遇点后，`slow` 和 `fast` 必须以**相同的步长**（即都每次移动一步）来确保它们在环的起点相遇。 
- 第二次相遇时，它们应该同时从链表头和相遇点出发，一步步移动。而这段代码让 `fast` 和 `slow` 分别按照两种速度移动，破坏了同步相遇的原则。

因此，在此代码中，即使它们第一次相遇了，第二次的步进方式也无法正确找到环的起点，最终无法保证程序的正确性。

#### 3. 缺少返回值逻辑

此外，您的代码在第二次 `while` 循环中的 `if (slow == fast)` 判断后并没有返回任何值，而是仅仅用 `break` 退出循环，这样会导致后续的 `return slow;` 可能返回了一个错误的值。

### 正确的第二次相遇逻辑

在正确的 Floyd 判圈算法中，第二次的 `while` 循环应该这样写：

```java
slow = head; // 将 slow 重置为链表头
while (slow != fast) { // 快慢指针同步移动
    slow = slow.next;
    fast = fast.next;
}
return slow; // 返回环的起点
```

- `slow` 从链表的头节点开始，`fast` 从相遇点开始，它们每次都只移动一步，直到它们再次相遇时，相遇点就是环的起点。
- 在这个过程里，我们不需要再检查 `fast != null`，因为在有环的情况下，`fast` 不会变成 `null`。
