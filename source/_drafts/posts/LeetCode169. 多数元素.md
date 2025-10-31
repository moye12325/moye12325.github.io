---
date: 2024-08-24T12:15:15.013Z
updated: 2024-08-24T13:14:36.682Z
title: LeetCode169. 多数元素
slug: 169-majority-element
oid: 66c9ced3ddb9a5c338a29a73
categories: LeetCode
type: post
permalink: /posts/LeetCode/169-majority-element
---


[169. 多数元素](https://leetcode.cn/problems/majority-element/description/)

给定一个大小为 n 的数组 nums，返回其中的多数元素。多数元素是指在数组中出现次数 大于 ⌊ n/2 ⌋ 的元素。

你可以假设数组是非空的，并且给定的数组总是存在多数元素。

 

示例 1：

> 输入：nums = [3,2,3]
> 输出：3
> 示例 2：

> 输入：nums = [2,2,1,1,1,2,2]
> 输出：2

 
### Java

> 出现的次数大于一半，则说明排序后的中间那个数一定是出现次数最多的，直接返回即可

```java
class Solution {
    public int majorityElement(int[] nums) {
        Arrays.sort(nums);
        return nums[nums.length / 2];
    }
}
```

### 候选人算法

> 查看了以前的提交记录，发现使用过哈希表、候选人算法。应该是在练习哈希表的时候做过这题。好吧，再次看到这道题全然想不起以前的解法，说明以前只是看到了但是并没有能深刻理解，无法做到举一反三。

```java
class Solution {
    public int majorityElement(int[] nums) {
        int count = 0;
        int candidate = 0;
        for(int num : nums){
            if(count == 0){
                candidate = num;
            }
            if (num == candidate){
                count++;
            }else{
                count--;
            }
        }
        return candidate;
    }
}
```

### 哈希表

```java
class Solution {
    public int majorityElement(int[] nums) {
        HashMap<Integer, Integer> hashMap = new HashMap<>();
        for (int num : nums) {
            if (!hashMap.containsKey(num)) {
                hashMap.put(num, 1);
            }else {
                hashMap.put(num, hashMap.get(num) + 1);
            }
        }
        for(Map.Entry<Integer, Integer> entry : hashMap.entrySet()) {
            if (entry.getValue() > nums.length / 2) {
                return entry.getKey();
            }
        }
        return 0;
    }
}
```