---
title: 百度校招笔试编程题
date: 2024-10-15 11:34:11
updated: 2024-10-15 12:35:57
categories:
  - 笔试记录
summary: >
  题 1
  
  题目描述
  整数 1  n，计算选择 k 个数能够获得多少积分。  
  计分规则：初始积分为 0，对于被选取的整数 i，如果 i + 1 没选取，则积分加 1。
  
  输入描述
  每个测试文件中包含多组测试数据。
  
  - 第一行输入一个整数 T (1 ≤ T ≤ 10^5) 代表数据组数。
  - 每组测试数据描述如下：
    - 在一行上输入两个整数 n, k (1 ≤ n, k ≤ 10^12; k
---
# 题 1

### 题目描述
整数 1 ~ n，计算选择 k 个数能够获得多少积分。  
计分规则：初始积分为 0，对于被选取的整数 i，如果 i + 1 没选取，则积分加 1。

#### 输入描述
每个测试文件中包含多组测试数据。

- 第一行输入一个整数 T (1 ≤ T ≤ 10^5) 代表数据组数。
- 每组测试数据描述如下：
  - 在一行上输入两个整数 n, k (1 ≤ n, k ≤ 10^12; k < n)，含义和题面描述一致。

#### 输出描述
对于每一组测试数据，在一行上输出一个整数，代表最多能够获得的积分。

#### 示例

##### 输入
```
2
1 1
4 2
```

##### 输出
```
1
2
```

#### 说明
- 第一个样例选择 1，积分为 1。
- 第二个样例一种可行方案为 1, 3，积分为 2。

### 解题思路

在这道题中，需要从整数 1 到 \( n \) 中选择 \( k \) 个数，使得按照题目给定的计分规则，能够获得最大的积分。计分规则如下：

- 初始积分为 0。
- 对于被选取的整数 \( i \)，如果 \( i + 1 \) 未被选取，则积分加 1。

目标是**最大化积分**。

#### 目标分析

为了最大化积分：

1. **尽可能多地让被选取的整数 \( i \) 满足 \( i + 1 \) 未被选取**，因为这样每个这样的 \( i \) 都能为积分加 1。
2. **在选择 \( k \) 个数的前提下，最大化满足上述条件的整数数量**。

#### 关键观察

- **每一个被选取的数 \( i \)，如果 \( i + 1 \) 未被选取，就能为积分加 1**。
- **因此，我们需要尽量避免选择连续的数**，因为如果 \( i \) 和 \( i + 1 \) 都被选取，\( i \) 就不能为积分贡献分数。

但是，由于我们必须选取 \( k \) 个数，当 \( k \) 较大时，我们无法避免选择相邻的数。

#### 最大积分的计算

为了计算最大积分，需要考虑两种情况：

1. **当 \( k \leq n - k + 1 \) 时**：

   - 可以安排选择的 \( k \) 个数，使得它们之间尽可能不相邻。
   - 例如，选择位置为奇数的数：1, 3, 5, ...
   - 此时，**最大积分为 \( k \)**，因为每个被选取的数后面都有一个未被选取的数（除非是最后一个数）。
   
2. **当 \( k > n - k + 1 \) 时**：

   - 无法避免选择相邻的数，因为需要选取的数太多了。
   - 此时，能够满足 \( i + 1 \) 未被选取的 \( i \) 的数量受到限制。
   - 实际上，**最大积分为 \( n - k + 1 \)**。
     - 这是因为在最优情况下，可以安排使得相邻的被选取数尽可能少。
     - 但是由于总共只有 \( n - k \) 个未被选取的数，因此最多只能有 \( n - k + 1 \) 个位置满足 \( i + 1 \) 未被选取。

#### 公式推导

综上所述，**最大积分可以表示为**：

$$
\text{最大积分} = \min(k, n - k + 1)
$$

- 当 $k \leq n - k + 1$ 时，最大积分为 $k$。
- 当 $k > n - k + 1$ 时，最大积分为 $n - k + 1$。

#### 示例验证

**示例 1：**

- 输入：$n = 4, k = 2$
- 计算：$\min(2, 4 - 2 + 1) = \min(2, 3) = 2$
- 最大积分为 2。
- 选取的数可以是 1 和 3，积分为 2。

**示例 2：**

- 输入：$n = 5, k = 4$
- 计算：$\min(4, 5 - 4 + 1) = \min(4, 2) = 2$
- 最大积分为 2。
- 无论如何安排，由于需要选取 4 个数，只能有最多 2 个数满足 $i + 1$ 未被选取。


### 代码实现

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static long maxScore(long n, long k) {
        return Math.min(k, n - k + 1);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        while (T-- > 0) {
            String[] parts = br.readLine().trim().split(" ");
            long n = Long.parseLong(parts[0]);
            long k = Long.parseLong(parts[1]);
            long res = maxScore(n, k);
            sb.append(res).append('\n');
        }
        System.out.print(sb.toString());
    }
}
```

### 深入理解

#### 为什么最大积分是 $ \min(k, n - k + 1) $？

- **未被选取的数的数量为 $ n - k $**。
- **在最优情况下，被选取的数与未被选取的数交替排列**，以最大化满足 $ i + 1 $ 未被选取的条件。
- **总共有 $ n - k + 1 $ 个位置可以放置满足条件的被选取数**。

  - 因为每两个未被选取的数之间可以放置一个被选取的数。
  - 再加上开头可以放置一个被选取的数。

- **当 $ k \leq n - k + 1 $ 时**，有足够的位置放置所有的 $ k $ 个被选取的数，使其满足 $ i + 1 $ 未被选取。

- **当 $ k > n - k + 1 $ 时**，无法避免有一些被选取的数后面紧跟着另一个被选取的数（即 $ i + 1 $ 被选取了），因此这些 $ i $ 无法为积分贡献分数。

#### 举例说明

**例子 1：$ n = 7, k = 3 $**

- $ n - k + 1 = 7 - 3 + 1 = 5 $
- 最大积分为 $ \min(3, 5) = 3 $
- 我们可以选择 1, 3, 5，积分为 3。

**例子 2：$ n = 7, k = 5 $**

- $ n - k + 1 = 7 - 5 + 1 = 3 $
- 最大积分为 $ \min(5, 3) = 3 $
- 无法避免有相邻的被选取数。
- 最大积分为 3。

---

## 题 2

### 题目描述
长度为 n，只包含小写字母的字符串 $S$，下标从 1 开始。进行 n 次操作，第 i 次操作将 $S_i$ 移动到字符串末尾。输出 n 次操作后的字符串。

例如字符串 `abqde`：
- 第一步 `"bqdea"`
- 第二步 `"bdeaq"`
- 第三步 `"bdaqe"`
- 第四步 `"bdaqe"`
- 第五步 `"bdaeq"`

### 输入描述
在一行上输入一个由小写字母构成的字符串，长度记为 $n$ $(1 \le n \le 10^6)$。

### 输出描述
在一行上输出一个字符串，表示操作后的字符串。

### 示例

#### 示例 1
##### 输入
```
paectc
```
##### 输出
```
accept
```

##### 说明
- 第一步：`aectcp`
- 第二步：`actcpe`
- 第三步：`accpet`
- 第四步：`acceptp`
- 第五步：`accept`
- 第六步：`accept`

#### 示例 2
##### 输入
```
abqde
```
##### 输出
```
bdaeq
```

## 思路

要高效地解决这个问题，我们需要一种能够在 $ O(n \log n) $ 时间内模拟操作的算法，因为字符串长度 $ n \leq 10^6 $。关键的观察是，在每一步操作 $ i $ 中，我们将当前字符串中第 $ i $ 个字符移动到字符串末尾。这意味着字符的位置在每次操作后都会改变。

使用随机平衡树（Treap），在 $ O(\log n) $ 时间内执行拆分和合并操作。这种数据结构非常适合需要高效移动元素的序列。

**算法思路：**

1. **初始化 Treap：** 将字符串的索引（从 0 到 $ n-1 $）插入到 Treap 中，表示字符的位置。

2. **执行操作：**
   - 对于每次操作 $ i $：
     - **拆分** Treap，将其在位置 $ i-1 $ 和 $ i $ 处分为三部分：
       - **左部分（Left）：** 位置在 $ i-1 $ 之前的节点。
       - **中间部分（Middle）：** 第 $ i $ 个位置的节点（需要移动的字符）。
       - **右部分（RightRest）：** 位置在 $ i $ 之后的节点。
     - **合并**左部分和右部分，形成新的 Treap，不包含第 $ i $ 个字符。
     - **将中间部分**附加到新的 Treap 末尾。

3. **构建最终字符串：**
   - 在所有操作完成后，对 Treap 进行中序遍历，获取字符索引的最终序列。
   - 将这些索引映射回原字符串中的字符，形成最终的字符串。


```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Random;

public class Main {
    static class TreapNode {
        int index;
        int priority;
        int size;
        TreapNode left, right;

        TreapNode(int index) {
            this.index = index;
            this.priority = rand.nextInt();
            this.size = 1;
        }
    }

    static Random rand = new Random();
    static TreapNode root;

    static void update(TreapNode node) {
        if (node != null) {
            node.size = 1;
            if (node.left != null) node.size += node.left.size;
            if (node.right != null) node.size += node.right.size;
        }
    }

    static TreapNode[] split(TreapNode node, int k) {
        if (node == null) return new TreapNode[]{null, null};
        int leftSize = (node.left != null) ? node.left.size : 0;
        if (k <= leftSize) {
            TreapNode[] res = split(node.left, k);
            node.left = res[1];
            update(node);
            return new TreapNode[]{res[0], node};
        } else {
            TreapNode[] res = split(node.right, k - leftSize - 1);
            node.right = res[0];
            update(node);
            return new TreapNode[]{node, res[1]};
        }
    }

    static TreapNode merge(TreapNode left, TreapNode right) {
        if (left == null || right == null)
            return (left != null) ? left : right;
        if (left.priority > right.priority) {
            left.right = merge(left.right, right);
            update(left);
            return left;
        } else {
            right.left = merge(left, right.left);
            update(right);
            return right;
        }
    }

    static void inOrderTraversal(TreapNode node, int[] result, int[] idx) {
        if (node != null) {
            inOrderTraversal(node.left, result, idx);
            result[idx[0]++] = node.index;
            inOrderTraversal(node.right, result, idx);
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        char[] S = br.readLine().toCharArray();
        int n = S.length;

        // 初始化 Treap，插入索引 0 到 n-1
        root = null;
        for (int i = 0; i < n; i++) {
            root = merge(root, new TreapNode(i));
        }

        // 执行 n 次操作
        for (int i = 0; i < n; i++) {
            // 在位置 i 处拆分
            TreapNode[] split1 = split(root, i);
            TreapNode Left = split1[0];
            TreapNode Right = split1[1];

            // 拆分 Right，得到 Middle 和 RightRest
            TreapNode[] split2 = split(Right, 1);
            TreapNode Middle = split2[0];
            TreapNode RightRest = split2[1];

            // 合并 Left 和 RightRest
            TreapNode merged = merge(Left, RightRest);

            // 将 Middle 附加到末尾
            root = merge(merged, Middle);
        }

        // 收集结果
        int[] resultIndices = new int[n];
        inOrderTraversal(root, resultIndices, new int[]{0});

        // 构建最终字符串
        StringBuilder sb = new StringBuilder();
        for (int idx : resultIndices) {
            sb.append(S[idx]);
        }

        System.out.println(sb.toString());
    }
}
```

**代码说明：**

- **TreapNode 类：** 表示 Treap 中的节点，包含索引、优先级（用于平衡）、子树大小，以及左、右子节点。

- **update() 方法：** 更新节点的子树大小。

- **split() 方法：** 根据给定位置 \( k \)，将 Treap 拆分为两个 Treap。

- **merge() 方法：** 合并两个 Treap，保持 Treap 的性质。

- **inOrderTraversal() 方法：** 中序遍历 Treap，收集节点的索引。

- **主逻辑：**
  - 读取输入字符串，初始化 Treap。
  - 执行 \( n \) 次操作，每次根据算法更新 Treap。
  - 在所有操作完成后，对 Treap 进行中序遍历，获取最终的字符索引序列。
  - 根据索引序列构建并输出最终的字符串。


## 题 3

### 题目描述
Ame9 最近沉迷麻将。Ame9 喜欢万子清一色（只包含万子牌的胡牌），他决定只胡万子清一色。

普通的麻将游戏中，万子牌有 1~9 种，每种牌有 4 张，我们用数字 1~9 表示，1 表示一万，2 表示二万，以此类推。而本题中一共有 n 种万字牌，使用数字 1~n 表示。

胡牌，是麻将中的胜利条件。要达成这个条件，手中 14 张牌必须组成四个面子 + 一对对子（不考虑七对子）。

对子即两张相同的牌。

面子又分为顺子和刻子两种：
- **顺子**：三张连续的牌，如 123 或 567
- **刻子**：三张相同的牌，如 333 或 999

无论是顺子还是刻子，均可以构成胡牌所需的面子。

举例：
- `112233355577999` 是胡牌
- `112233344467899` 是胡牌
- `112233344467999` 不是胡牌

现在给出一个正整数 n (1 ≤ n ≤ 13)，假设 Ame9 只能使用 1 至 n 之间的万子牌胡牌，请问他有几种不同的胡牌牌型？两种牌型要是不同的，当且仅当存在一种牌型中的牌和另一种牌型中的枚数不同。

### 输入描述
一行一个正整数 $n$ $(1 \le n \le 13)$。

### 输出描述
一行一个整数，代表胡牌牌型的种数。

### 示例

#### 示例 1
##### 输入
```
1
```
##### 输出
```
0
```
##### 说明
4 张一万凑不齐 14 张牌，当然没有胡牌牌型。

#### 示例 2
##### 输入
```
4
```
##### 输出
```
10
```
##### 说明
合适的胡牌牌型为：
- 11222333434444
- 11122233334444
- 11112223334444
- 等等...

### 思路

### 解题思路

本题要求计算使用编号为 1 到 \( n \) 的万子牌（每种牌有 4 张）构成的胡牌牌型的总数。胡牌的条件是手中 14 张牌必须组成 **4 个面子**（顺子或刻子）加 **1 对对子**。

由于每种牌的张数有限（最多 4 张），并且牌的编号范围为 1 到 \( n \)，需要计算满足以下条件的不同牌型数量：

- 每种牌的数量在 0 到 4 之间。
- 所有牌的总张数为 14。
- 牌可以分解为 4 个面子和 1 对对子。

**总体思路：**

1. **生成所有可能的牌数量组合：**
   - 每种牌的数量在 0 到 4 之间。
   - 所有牌的总张数为 14。
   - 通过递归的方法生成所有可能的牌数量组合（即每种牌使用了多少张）。

2. **对于每一种牌数量组合，尝试所有可能的对子：**
   - 对于每种牌，如果数量不少于 2，可以作为对子。
   - 减去对子所用的 2 张牌，剩余的牌需要能分解为 4 个面子。

3. **检查剩余的牌能否分解为 4 个面子：**
   - 使用递归和记忆化搜索（Memoization）的方法，检查剩余的牌是否能被分解为面子。
   - 面子可以是顺子（3 张连续的牌）或刻子（3 张相同的牌）。

4. **统计满足条件的牌型数量：**
   - 如果剩余的牌能被分解为 4 个面子，则该牌数量组合是一个有效的胡牌牌型。
   - 累计有效的牌型数量。

### 代码实现


```java
import java.util.*;

public class Main {
    static int n;
    static Map<String, Boolean> memo = new HashMap<>();
    static int totalHands = 0;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();
        sc.close();

        // 如果总牌数不足 14 张，无法胡牌
        if (n * 4 < 14) {
            System.out.println(0);
            return;
        }

        int[] counts = new int[n + 1]; // counts[1..n], counts[0] unused
        generateCounts(1, counts, 0);
        System.out.println(totalHands);
    }

    // 生成所有可能的牌数量组合
    static void generateCounts(int pos, int[] counts, int sum) {
        if (pos > n) {
            if (sum == 14) {
                checkHand(counts);
            }
            return;
        }

        for (int cnt = 0; cnt <= 4; cnt++) {
            if (sum + cnt > 14) {
                break;
            }
            counts[pos] = cnt;
            generateCounts(pos + 1, counts, sum + cnt);
            counts[pos] = 0; // 回溯
        }
    }

    // 检查当前牌数量组合是否为有效的胡牌牌型
    static void checkHand(int[] counts) {
        // 尝试每一种可能的对子
        for (int i = 1; i <= n; i++) {
            if (counts[i] >= 2) {
                counts[i] -= 2; // 减去对子
                if (canFormMelds(counts)) {
                    totalHands++;
                    counts[i] += 2; // 还原
                    break; // 一个对子成功即可，不用继续尝试
                }
                counts[i] += 2; // 还原
            }
        }
    }

    // 检查剩余的牌能否分解为 4 个面子
    static boolean canFormMelds(int[] counts) {
        String key = Arrays.toString(counts);
        if (memo.containsKey(key)) {
            return memo.get(key);
        }

        // 检查是否所有牌都用完了
        boolean isEmpty = true;
        for (int i = 1; i <= n; i++) {
            if (counts[i] != 0) {
                isEmpty = false;
                break;
            }
        }
        if (isEmpty) {
            memo.put(key, true);
            return true;
        }

        // 尝试组成刻子
        for (int i = 1; i <= n; i++) {
            if (counts[i] >= 3) {
                counts[i] -= 3;
                if (canFormMelds(counts)) {
                    counts[i] += 3;
                    memo.put(key, true);
                    return true;
                }
                counts[i] += 3;
            }
        }

        // 尝试组成顺子
        for (int i = 1; i <= n - 2; i++) {
            if (counts[i] > 0 && counts[i + 1] > 0 && counts[i + 2] > 0) {
                counts[i]--;
                counts[i + 1]--;
                counts[i + 2]--;
                if (canFormMelds(counts)) {
                    counts[i]++;
                    counts[i + 1]++;
                    counts[i + 2]++;
                    memo.put(key, true);
                    return true;
                }
                counts[i]++;
                counts[i + 1]++;
                counts[i + 2]++;
            }
        }

        memo.put(key, false);
        return false;
    }
}
```

### 代码说明

- **`main` 方法：**
  - 读取输入的 \( n \) 值。
  - 判断总牌数是否足够组成 14 张牌，如果不足，直接输出 0。
  - 初始化牌数量数组 `counts`，长度为 \( n + 1 \)，其中 `counts[0]` 不使用。
  - 调用 `generateCounts` 方法，开始生成所有可能的牌数量组合。

- **`generateCounts` 方法：**
  - 递归地生成每种牌可能的数量（0 到 4），并确保总牌数为 14。
  - 当遍历到第 \( n + 1 \) 种牌时，检查当前组合的总牌数是否为 14。
    - 如果是，调用 `checkHand` 方法检查该组合是否为有效的胡牌牌型。

- **`checkHand` 方法：**
  - 遍历每一种可能的对子（数量不少于 2 的牌）。
  - 减去对子所用的 2 张牌，调用 `canFormMelds` 方法检查剩余的牌能否分解为 4 个面子。
  - 如果可以，累加有效的牌型数量 `totalHands`，并跳出循环（因为只需要找到一个有效的组合即可）。
  - 无论结果如何，都要还原牌的数量（回溯）。

- **`canFormMelds` 方法：**
  - 使用字符串形式的 `counts` 作为键，在 `memo` 中进行记忆化搜索，避免重复计算。
  - 检查是否所有牌都用完了，如果是，返回 `true`。
  - 尝试组成刻子（3 张相同的牌）：
    - 如果某种牌的数量不少于 3，尝试减去 3 张牌，并递归调用 `canFormMelds`。
  - 尝试组成顺子（3 张连续的牌）：
    - 从牌编号 1 遍历到 \( n - 2 \)，如果连续的三种牌数量都不少于 1，尝试减去这些牌，并递归调用 `canFormMelds`。
  - 如果上述尝试都失败，返回 `false`。


### 注意事项

- **记忆化搜索（Memoization）：**
  - 使用 `HashMap` 来保存已经计算过的牌数量组合的结果，避免重复计算，提高效率。
  - 由于每种牌的数量在 0 到 4 之间，牌的编号在 1 到 \( n \) 之间，`counts` 数组的可能取值有限。

- **递归与回溯：**
  - 在尝试组成刻子或顺子时，需要修改 `counts` 数组，递归调用后要及时还原（回溯）。

- **边界条件：**
  - 在组成顺子时，需要注意不能越界，因此循环只需到 \( n - 2 \)。

- **优化：**
  - 当找到一个有效的对子和面子组合后，可以立即计数并跳出对子尝试的循环，因为同一牌数量组合下，不需要重复尝试不同的对子。

### 超时，通过 80% 用例，优化

> 耗时主要是在记忆化搜索的过程中，减少哈希表的开销，提高效率。

- **使用整数编码代替字符串作为哈希表的键：**
  - 由于每种牌的数量在 0 到 4 之间，我们可以将每种牌的数量看作 5 进制的位数，使用一个 `long` 型整数来唯一表示当前的牌数量状态。
  - 这样可以避免使用字符串作为键所带来的大量内存和时间开销。

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.*;

public class Main {
    static int n;
    static Map<Long, Boolean> memo = new HashMap<>();
    static int totalHands = 0;

    public static void main(String[] args) throws IOException {
        // 使用 BufferedReader 读取输入
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        n = Integer.parseInt(br.readLine().trim());
        br.close();

        // 如果总牌数不足 14 张，无法胡牌
        if (n * 4 < 14) {
            System.out.println(0);
            return;
        }

        int[] counts = new int[n + 1]; // counts[1..n], counts[0] 不使用
        generateCounts(1, counts, 0);
        System.out.println(totalHands);
    }

    // 生成所有可能的牌数量组合
    static void generateCounts(int pos, int[] counts, int sum) {
        if (pos > n) {
            if (sum == 14) {
                checkHand(counts);
            }
            return;
        }

        for (int cnt = 0; cnt <= 4; cnt++) {
            if (sum + cnt > 14) {
                break;
            }
            counts[pos] = cnt;
            generateCounts(pos + 1, counts, sum + cnt);
            counts[pos] = 0; // 回溯
        }
    }

    // 检查当前牌数量组合是否为有效的胡牌牌型
    static void checkHand(int[] counts) {
        // 尝试每一种可能的对子
        for (int i = 1; i <= n; i++) {
            if (counts[i] >= 2) {
                counts[i] -= 2; // 减去对子
                if (canFormMelds(counts)) {
                    totalHands++;
                    counts[i] += 2; // 还原
                    break; // 一个对子成功即可，不用继续尝试
                }
                counts[i] += 2; // 还原
            }
        }
    }

    // 编码当前的 counts 数组为一个唯一的 long 型整数
    static long encode(int[] counts) {
        long code = 0;
        for (int i = 1; i <= n; i++) {
            code = code * 5 + counts[i]; // 因为每个 counts[i] 在 0 到 4 之间，使用 5 进制
        }
        return code;
    }

    // 检查剩余的牌能否分解为 4 个面子
    static boolean canFormMelds(int[] counts) {
        long key = encode(counts);
        if (memo.containsKey(key)) {
            return memo.get(key);
        }

        // 检查是否所有牌都用完了
        boolean isEmpty = true;
        for (int i = 1; i <= n; i++) {
            if (counts[i] != 0) {
                isEmpty = false;
                break;
            }
        }
        if (isEmpty) {
            memo.put(key, true);
            return true;
        }

        // 尝试组成刻子
        for (int i = 1; i <= n; i++) {
            if (counts[i] >= 3) {
                counts[i] -= 3;
                if (canFormMelds(counts)) {
                    counts[i] += 3;
                    memo.put(key, true);
                    return true;
                }
                counts[i] += 3;
            }
        }

        // 尝试组成顺子
        for (int i = 1; i <= n - 2; i++) {
            while (counts[i] > 0 && counts[i + 1] > 0 && counts[i + 2] > 0) {
                counts[i]--;
                counts[i + 1]--;
                counts[i + 2]--;
                if (canFormMelds(counts)) {
                    counts[i]++;
                    counts[i + 1]++;
                    counts[i + 2]++;
                    memo.put(key, true);
                    return true;
                }
                counts[i]++;
                counts[i + 1]++;
                counts[i + 2]++;
                break; // 避免重复尝试相同的顺子
            }
        }

        memo.put(key, false);
        return false;
    }
}
```

### 代码说明

- **编码函数 `encode`：**
  - 将 `counts` 数组编码为一个唯一的 `long` 型整数。
  - 因为每个 `counts[i]` 的取值范围是 0 到 4，所以可以将其视为 5 进制的位数。
  - 这样可以高效地将整个数组状态转换为一个整数，方便在哈希表中存储和查找。

- **优化 `canFormMelds` 方法：**
  - 使用 `long` 型整数作为键，减少了字符串的创建和比较操作，提高了哈希表的性能。
  - 在尝试组成顺子时，使用 `while` 循环尽可能多地减少连续的牌数，避免重复状态。
    - **注意：** 在减少牌数后，需要立即还原，以保证不会影响后续的计算。

### 性能分析

- **时间复杂度：**
  - 由于牌的种类和每种牌的数量有限，状态空间虽然较大（约为 \(5^{13}\)），但实际有效状态数量远小于此值。
  - 通过记忆化搜索和状态编码，大大减少了重复计算。
  - 优化后，程序能够在合理的时间内处理所有可能的状态。

- **空间复杂度：**
  - 使用了一个 `Map<Long, Boolean>` 来存储状态，由于状态数在可控范围内，内存占用不会过大。