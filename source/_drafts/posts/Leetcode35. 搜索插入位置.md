---
date: 2024-08-24T13:26:07.036Z
updated: null
title: Leetcode35. 搜索插入位置
slug: leetcode35-search-insert-position
oid: 66c9df6fddb9a5c338a29b77
categories: LeetCode
type: post
permalink: /posts/LeetCode/leetcode35-search-insert-position
---


[Leetcode35. 搜索插入位置](https://leetcode.cn/problems/search-insert-position/description/)

### 题目描述

给定一个排序数组和一个目标值，在数组中找到目标值，并返回其索引。如果目标值不存在于数组中，返回它将会被按顺序插入的位置。

请必须使用时间复杂度为 `O(log n)` 的算法。

#### 示例 1:

- **输入：** `nums = [1,3,5,6]`, `target = 5`
- **输出：** `2`

#### 示例 2:

- **输入：** `nums = [1,3,5,6]`, `target = 2`
- **输出：** `1`

#### 示例 3:

- **输入：** `nums = [1,3,5,6]`, `target = 7`
- **输出：** `4`

### 提示：

- `1 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `nums` 为 **无重复元素** 的 **升序** 排列数组
- `-10^4 <= target <= 10^4`

### Java

```java
class Solution {
    public int searchInsert(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;
        
        while (left <= right) {
            int mid = left + (right - left) / 2;
            
            if (nums[mid] == target) {
                return mid; // 找到目标值，返回索引
            } else if (nums[mid] < target) {
                left = mid + 1; // 目标值在右半部分
            } else {
                right = mid - 1; // 目标值在左半部分
            }
        }
        
        // 未找到目标值，返回应该插入的位置
        return left;
    }
}
```



### 为什么使用 `<=` 而不是 `<`？

`while` 循环条件通常使用 `left <= right` 而不是 `left < right`，这样做是为了确保所有的元素都会被检查到，尤其是在数组长度为 1 或者只有两个元素的情况下。

1. **确保所有元素都被检查**：
   - 如果条件是 `left < right`，当 `left` 和 `right` 相等时，循环会终止。此时有可能数组中间的那个元素还没有被检查。
   - 使用 `<=` 可以确保在最后一次迭代中，`left` 和 `right` 相等时，还能检查那个唯一的元素。

2. **寻找插入位置**：
   - 使用 `<=` 可以确保在 `target` 不存在的情况下，`left` 指向的正是目标值应该插入的位置。如果使用 `<`，在某些情况下，`left` 的值可能没有完全正确地指向应插入的位置，特别是在处理极端情况时。

### 二者的影响

- **如果使用 `left <= right`**：
  - 当数组长度为 1 时，能够正确处理。
  - 如果目标值不存在，`left` 会最终指向插入位置。
  
- **如果使用 `left < right`**：
  - 如果 `left` 和 `right` 相等时直接跳出循环，可能会遗漏对最后一个元素的检查。
  - 对于一些情况，特别是目标值在数组边界或不在数组中的情况下，插入位置的判断可能不准确。

### 例子分析

假设数组 `nums = [1, 3, 5, 6]`，`target = 2`：

- 如果使用 `left <= right`：
  - `left = 0, right = 3`
  - `mid = 1`（检查`nums[1] = 3`，继续调整）
  - `right = 0`（循环继续，最终会确定`left = 1`，此时插入位置正确）

- 如果使用 `left < right`：
  - `left = 0, right = 3`
  - `mid = 1`（检查`nums[1] = 3`，继续调整）
  - `right = 0`（`left == right`时退出循环，`left`此时是`1`，仍然正确）

在这种简单情况下，结果可能一致，但使用 `<=` 的方式更加稳健，能够处理各种边界情况和特殊情况。因此，`while (left <= right)` 是二分查找中更常见和可靠的选择。



### 1. `while (left <= right)` 场景

在编写二分查找或类似算法时，`while (left <= right)` 和 `while (left < right)` 的选择取决于希望在算法中如何处理区间和边界情况。

#### 使用场景：
- **需要检查所有元素，包括区间的最后一个元素**。
- **要处理的区间在每次迭代后可能会缩小到一个单一元素**，且你希望对这个单一元素进行处理。
- **寻找精确匹配或在元素不存在时返回插入位置**。

#### 典型应用：
- **标准二分查找**：在一个排序数组中查找目标值。如果找不到目标值，还需要返回其应插入的位置。
- **寻找上/下界**：当你需要找出一个区间内的最左或最右的符合条件的元素。

#### 示例代码：

```java
public int binarySearch(int[] nums, int target) {
    int left = 0;
    int right = nums.length - 1;

    while (left <= right) {  // 使用 <= 是为了包括最后一个元素
        int mid = left + (right - left) / 2;

        if (nums[mid] == target) {
            return mid;
        } else if (nums[mid] < target) {
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }

    // 如果没有找到，left 就是插入位置
    return left;
}
```

### 2. `while (left < right)` 场景

#### 使用场景：
- **需要处理的区间在每次迭代后会缩小到至少两个元素**。
- **不需要检查单一元素的情况，或者能够保证在跳出循环后能准确处理剩余的元素**。
- **寻找满足某种条件的临界点**，通常是在返回时直接得到结果，而无需再进行额外判断。

#### 典型应用：
- **寻找特定条件的最小值或最大值**：如查找满足某个条件的最小元素，或查找符合某个条件的区间分界点。

#### 示例代码：

```java
public int findFirstGreaterThan(int[] nums, int target) {
    int left = 0;
    int right = nums.length;

    while (left < right) {  // 使用 < 是因为我们不需要检查最后一个元素
        int mid = left + (right - left) / 2;

        if (nums[mid] <= target) {
            left = mid + 1;  // 排除掉 mid，所以 left = mid + 1
        } else {
            right = mid;  // 保持 right 指向可能的候选结果
        }
    }

    // 当循环结束时，left == right，且 nums[left] 是第一个大于 target 的元素
    return left;
}
```

### 总结：

- **使用 `<=`**：
  - 适用于需要检查整个区间，包括最后一个元素。
  - 多用于需要在找到或未找到目标元素时做额外处理的情况，如插入位置的计算。

- **使用 `<`**：
  - 适用于不需要检查最后一个元素，或者可以在跳出循环后自然处理剩余元素的情况。
  - 多用于寻找特定边界或条件下的分界点。