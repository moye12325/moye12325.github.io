---
title: LeetCode3142. 判断矩阵是否满足条件
date: 2024-08-30 10:58:48
updated: 2024-08-30 10:59:16
categories:
  - LeetCode
summary: >
  3142. 判断矩阵是否满足条件
  
  https://leetcode.cn/problems/check-if-grid-satisfies-conditions/description/
  
  给你一个大小为  的二维矩阵 。你需要判断每一个格子  是否满足以下条件：
  
  - 如果它下面的格子存在，那么它需要等于它下面的格子，即 。
  - 如果它右边的格子存在，那么它需要不等于它右边的格子，即 。
  
  如
---
## 3142. 判断矩阵是否满足条件

https://leetcode.cn/problems/check-if-grid-satisfies-conditions/description/

给你一个大小为 `m x n` 的二维矩阵 `grid`。你需要判断每一个格子 `grid[i][j]` 是否满足以下条件：

- 如果它下面的格子存在，那么它需要等于它下面的格子，即 `grid[i][j] == grid[i + 1][j]`。
- 如果它右边的格子存在，那么它需要不等于它右边的格子，即 `grid[i][j] != grid[i][j + 1]`。

如果所有格子都满足以上条件，则返回 `true`，否则返回 `false`。

### 示例

#### 示例 1：

- **输入**：`grid = [[1,0,2],[1,0,2]]`
- **输出**：`true`

**解释**：网格图中所有格子都符合条件。

#### 示例 2：

- **输入**：`grid = [[1,1,1],[0,0,0]]`
- **输出**：`false`

**解释**：同一行中的格子值都相等。

#### 示例 3：

- **输入**：`grid = [[1],[2],[3]]`
- **输出**：`false`

**解释**：同一列中的格子值不相等。

### 提示：

- `1 <= n, m <= 10`
- `0 <= grid[i][j] <= 9`

```java
import java.util.HashSet;

//leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public boolean satisfiesConditions(int[][] grid) {
        int m = grid.length;
        int n = grid[0].length;

        if (m == 1 && n == 1) return true;
        if (m == 1 && n == 2 && grid[0][0] != grid[0][1]) return true;

        for (int i = 1; i < n; i++) {
            if (grid[0][i] == grid[0][i - 1]) return false;
        }

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                int colValue = grid[0][j];
                if (grid[i][j] != colValue) return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        int[][] grid = {{3,5,3},{3,5,3},{3,5,3}};
        System.out.println(new Solution().satisfiesConditions(grid));
    }
}
```

要优化 `satisfiesConditions` 方法，我们需要分析代码逻辑并找出可以改进的地方。以下是详细的解释和优化后的代码：

### 原代码分析

1. **特殊情况**: 
   - 如果网格是 `1x1`，它显然满足条件。
   - 如果网格是 `1x2`，只要两个元素不同就满足条件。

2. **行检查**:
   - 检查第一行的所有元素是否不同，这需要 \(O(n)\) 的时间复杂度。

3. **列检查**:
   - 检查每列中的所有元素是否相同，这涉及遍历整个网格，时间复杂度为 \(O(m \times n)\)。

### 优化策略

- 当前的方法已经对每个元素只检查一次，时间复杂度为 \(O(m \times n)\)。但我们可以简化逻辑以提高代码清晰度。

### 优化后的代码

```java
class Solution {
    public boolean satisfiesConditions(int[][] grid) {
        int m = grid.length;
        int n = grid[0].length;

        if (m == 1 && n == 1) return true;
        if (m == 1 && n == 2 && grid[0][0] != grid[0][1]) return true;

        // 检查第一行的元素是否都不相同。
        for (int i = 1; i < n; i++) {
            if (grid[0][i] == grid[0][i - 1]) return false;
        }

        // 检查每一列的元素是否相同。
        for (int j = 0; j < n; j++) {
            int colValue = grid[0][j];
            for (int i = 1; i < m; i++) {
                if (grid[i][j] != colValue) return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        int[][] grid = {{3,5,3},{3,5,3},{3,5,3}};
        System.out.println(new Solution().satisfiesConditions(grid));
    }
}
```

### 优化思路

- **行唯一性检查**: 遍历第一行，确保每个元素都与前一个元素不同。
- **列一致性检查**: 检查每列的所有元素是否相同，从第二行开始（第一行作为参考）。
时间复杂度 $O(m \times n)$。

###  使用 Arrays.equals 方法

```java
import java.util.Arrays;

class Solution {
    public boolean satisfiesConditions(int[][] grid) {
        int m = grid.length;
        int n = grid[0].length;

        if (m == 1 && n == 1) return true;
        if (m == 1 && n == 2 && grid[0][0] != grid[0][1]) return true;

        // 检查第一行的元素是否都不相同。
        for (int i = 1; i < n; i++) {
            if (grid[0][i] == grid[0][i - 1]) return false;
        }

        // 检查每一行是否与第一行相同。
        for (int i = 1; i < m; i++) {
            if (!Arrays.equals(grid[i], grid[0])) return false;
        }

        return true;
    }

    public static void main(String[] args) {
        int[][] grid = {{3,5,3},{3,5,3},{3,5,3}};
        System.out.println(new Solution().satisfiesConditions(grid));
    }
}
```

#### 执行时间反而变长


在使用 `Arrays.equals` 后，每次比较整个子数组，看上去降低了时间复杂度。

但其实时间复杂度仍然不变，因为需要检查每一行与第一行是否相同。尽管 `Arrays.equals` 本身是 $O(n)$ 的操作，但你需要对每一行执行这个操作，因此总体复杂度是$O(m \times n)$。

执行时间变长的原因包括：

1. **额外开销**：`Arrays.equals` 有一些方法调用的开销。
2. **数据布局**：缓存性能可能会因为访问模式不同而受到影响。
3. **实现细节**：具体的性能也可能受到 JVM 优化和实现的影响。