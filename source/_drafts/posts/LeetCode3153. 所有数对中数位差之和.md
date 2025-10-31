---
date: 2024-08-30T10:50:37.651Z
updated: 2024-08-30T12:35:00.013Z
title: LeetCode3153. 所有数对中数位差之和
slug: LeetCode3153
oid: 66d1a3fdc10f2bbf4994d79a
categories: LeetCode
type: post
permalink: /posts/LeetCode/LeetCode3153
---


## 3153. 所有数对中数位差之和

你有一个数组 `nums`，它只包含正整数，所有正整数的数位长度都相同。

两个整数的数位差指的是两个整数相同位置上不同数字的数目。

请你返回 `nums` 中所有整数对里，数位差之和。

### 示例

#### 示例 1：

- **输入**：`nums = [13, 23, 12]`
- **输出**：`4`

**解释**：
计算过程如下：
- 13 和 23 的数位差为 1。
- 13 和 12 的数位差为 1。
- 23 和 12 的数位差为 2。
所以所有整数数对的数位差之和为 1 + 1 + 2 = 4。

#### 示例 2：

- **输入**：`nums = [10, 10, 10, 10]`
- **输出**：`0`

**解释**：
数组中所有整数都相同，所以所有整数数对的数位不同之和为 0。

### 提示：

- `2 <= nums.length <= 10^5`
- `1 <= nums[i] < 10^9`
- `nums` 中的整数都有相同的数位长度。

## 暴力破解

```java
public class Solution {
    public int sumOfDigitDifferences(int[] nums) {
        int totalDifferenceSum = 0;

        // 遍历所有数对
        for (int i = 0; i < nums.length - 1; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                // 计算每个数对的数位差
                totalDifferenceSum += calculateDigitDifference(nums[i], nums[j]);
            }
        }

        return totalDifferenceSum;
    }

    // 计算两个数字的数位差
    private int calculateDigitDifference(int num1, int num2) {
        int difference = 0;

        while (num1 > 0 && num2 > 0) {
            // 比较两个数字的最后一位
            if (num1 % 10 != num2 % 10) {
                difference++;
            }
            // 去掉数字的最后一位
            num1 /= 10;
            num2 /= 10;
        }

        return difference;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        int[] nums1 = {13, 23, 12};
        int[] nums2 = {10, 10, 10, 10};

        System.out.println(solution.sumOfDigitDifferences(nums1)); // 输出：4
        System.out.println(solution.sumOfDigitDifferences(nums2)); // 输出：0
    }
}
```

### 代码解释：

1. **sumOfDigitDifferences 方法**:
   - 用于计算所有数对的数位差之和。
   - 使用双重循环遍历 `nums` 数组中的所有数对 `(i, j)`，其中 `i < j`。
   - 对于每一个数对，调用 `calculateDigitDifference` 方法来计算数位差。

2. **calculateDigitDifference 方法**:
   - 计算两个数字的数位差。
   - 逐位比较两个数字的数位，如果它们的数位不同，差值加 1。
   - 循环直到两个数字都被处理完。

### 注意：
时间复杂度是 $O(n^2 \times m)$，其中 \(n\) 是数组的长度，\(m\) 是数字的位数（最多 9 位）。

## 优化时间复杂度

```java
class Solution {
    public long sumDigitDifferences(int[] nums) {
        long ans = 0;
        int[][] cnt = new int[Integer.toString(nums[0]).length()][10];
        for (int k = 0; k < nums.length; k++) {
            int x = nums[k];
            for (int i = 0; x > 0; x /= 10, i++) {
                ans += k - cnt[i][x % 10]++;
            }
        }
        return ans;
    }
}
```