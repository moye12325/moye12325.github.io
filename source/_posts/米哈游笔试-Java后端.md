---
title: 米哈游笔试-Java后端
date: '2025-04-28 06:02:14'
categories:
  - 笔试记录
tags:
  - 笔试记录
---
我们可以证明，对于前 <math><semantics><mrow><mi>i</mi></mrow><annotation>i</annotation></semantics></math>i 个数构成的所有区间，其“数字凸包区间”的并恰好是一个连续区间 <math><semantics><mrow><mo>\[</mo><msub><mi>P</mi><mi>min</mi><mo>⁡</mo></msub><mo>,</mo><msub><mi>P</mi><mi>max</mi><mo>⁡</mo></msub><mo>\]</mo></mrow><annotation>\[P\_{\\min},P\_{\\max}\]</annotation></semantics></math>\[Pmin​,Pmax​\]（其中

<math><semantics><mrow><msub><mi>P</mi><mi>min</mi><mo>⁡</mo></msub><mo>\=</mo><mi>min</mi><mo>⁡</mo><mo>{</mo><msub><mi>a</mi><mn>1</mn></msub><mo>,</mo><mo>…</mo><mo>,</mo><msub><mi>a</mi><mi>i</mi></msub><mo>}</mo><mo>,</mo><msub><mi>P</mi><mi>max</mi><mo>⁡</mo></msub><mo>\=</mo><mi>max</mi><mo>⁡</mo><mo>{</mo><msub><mi>a</mi><mn>1</mn></msub><mo>,</mo><mo>…</mo><mo>,</mo><msub><mi>a</mi><mi>i</mi></msub><mo>}</mo></mrow><annotation>P\_{\\min}=\\min\\{a\_1,\\ldots,a\_i\\},\\quad P\_{\\max}=\\max\\{a\_1,\\ldots,a\_i\\}</annotation></semantics></math>Pmin​\=min{a1​,…,ai​},Pmax​\=max{a1​,…,ai​}

）。这是因为整个区间 <math><semantics><mrow><mo>\[</mo><mn>1</mn><mo>,</mo><mi>i</mi><mo>\]</mo></mrow><annotation>\[1,i\]</annotation></semantics></math>\[1,i\] 作为一个子区间，其数字凸包就是 <math><semantics><mrow><mo>\[</mo><msub><mi>P</mi><mi>min</mi><mo>⁡</mo></msub><mo>,</mo><msub><mi>P</mi><mi>max</mi><mo>⁡</mo></msub><mo>\]</mo></mrow><annotation>\[P\_{\\min},P\_{\\max}\]</annotation></semantics></math>\[Pmin​,Pmax​\]；而其他子区间给出的区间都是这个区间的子区间，不可能扩充出整段连续区间之外的数值。

因此，对每个 <math><semantics><mrow><mi>i</mi></mrow><annotation>i</annotation></semantics></math>i 我们只需维护前缀中的最小值和最大值，从而：

* 若 <math><semantics><mrow><msub><mi>P</mi><mi>min</mi><mo>⁡</mo></msub><mo>></mo><mn>0</mn></mrow><annotation>P\_{\\min}>0</annotation></semantics></math>Pmin​>0（也就是说前缀中没有出现0），那么整个集合不包含从 <math><semantics><mrow><mn>0</mn></mrow><annotation>0</annotation></semantics></math>0 到 <math><semantics><mrow><msub><mi>P</mi><mi>min</mi><mo>⁡</mo></msub><mo>−</mo><mn>1</mn></mrow><annotation>P\_{\\min}-1</annotation></semantics></math>Pmin​−1 的数，此时最小的非负整数就是 <math><semantics><mrow><mn>0</mn></mrow><annotation>0</annotation></semantics></math>0。
* 否则（也即 <math><semantics><mrow><msub><mi>P</mi><mi>min</mi><mo>⁡</mo></msub><mo>\=</mo><mn>0</mn></mrow><annotation>P\_{\\min}=0</annotation></semantics></math>Pmin​\=0），那么由全区间 <math><semantics><mrow><mo>\[</mo><mn>0</mn><mo>,</mo><msub><mi>P</mi><mi>max</mi><mo>⁡</mo></msub><mo>\]</mo></mrow><annotation>\[0,P\_{\\max}\]</annotation></semantics></math>\[0,Pmax​\] 可知所有从 <math><semantics><mrow><mn>0</mn></mrow><annotation>0</annotation></semantics></math>0 到 <math><semantics><mrow><msub><mi>P</mi><mi>max</mi><mo>⁡</mo></msub></mrow><annotation>P\_{\\max}</annotation></semantics></math>Pmax​ 都被覆盖，答案就是 <math><semantics><mrow><msub><mi>P</mi><mi>max</mi><mo>⁡</mo></msub><mo>+</mo><mn>1</mn></mrow><annotation>P\_{\\max}+1</annotation></semantics></math>Pmax​+1。

下面给出Java实现，时间复杂度 <math><semantics><mrow><mi>O</mi><mo>(</mo><mi>n</mi><mo>)</mo></mrow><annotation>O(n)</annotation></semantics></math>O(n)：




```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws IOException {
        // 使用 BufferedReader 读取输入
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        // 第一行可以只包含一个整数n
        int n = Integer.parseInt(line.trim());
        
        // 读取数组
        int[] a = new int[n];
        StringTokenizer st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) {
            a[i] = Integer.parseInt(st.nextToken());
        }
        
        // 前缀最小值和前缀最大值
        int prefixMin = Integer.MAX_VALUE;
        int prefixMax = Integer.MIN_VALUE;
        
        // 构造答案
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) {
            prefixMin = Math.min(prefixMin, a[i]);
            prefixMax = Math.max(prefixMax, a[i]);
            
            // 若前缀没有0，则说明[1,i]的所有区间其并不含0，答案为0；
            // 否则答案就是前缀最大值加1
            if (prefixMin > 0) {
                sb.append("0");
            } else {
                sb.append(prefixMax + 1);
            }
            if (i < n - 1) {
                sb.append(" ");
            }
        }
        
        System.out.println(sb.toString());
    }
}
```

---

### 代码说明

1. **输入处理**  
   使用 `BufferedReader` 和 `StringTokenizer` 提高大数据量时的读入效率。

2. **维护前缀最值**  
   循环中持续维护前 <math><semantics><mrow><mi>i</mi></mrow><annotation>i</annotation></semantics></math>i 个数的最小值 (`prefixMin`) 和最大值 (`prefixMax`)。

3. **判断与输出**

   * 当 `prefixMin > 0` 时，说明前缀中没有0（也就没有比0更小的非负数），答案输出 0。
   * 当 `prefixMin == 0` 时，根据区间覆盖情况（由整段子区间 <math><semantics><mrow><mo>\[</mo><mn>0</mn><mo>,</mo><mi>p</mi><mi>r</mi><mi>e</mi><mi>f</mi><mi>i</mi><mi>x</mi><mi>M</mi><mi>a</mi><mi>x</mi><mo>\]</mo></mrow><annotation>\[0, prefixMax\]</annotation></semantics></math>\[0,prefixMax\] 可知），答案输出 `prefixMax + 1`。

这种做法只对每个 <math><semantics><mrow><mi>i</mi></mrow><annotation>i</annotation></semantics></math>i 进行常数时间操作，总体时间复杂度为 <math><semantics><mrow><mi>O</mi><mo>(</mo><mi>n</mi><mo>)</mo></mrow><annotation>O(n)</annotation></semantics></math>O(n)，能够满足 <math><semantics><mrow><mi>n</mi><mo>≤</mo><mn>2</mn><mo>×</mo><msup><mn>10</mn><mn>5</mn></msup></mrow><annotation>n \\le 2 \\times 10^5</annotation></semantics></math>n≤2×105 的要求。

---

### 题目描述

给定一个长度为 <math><semantics><mrow><mi>n</mi></mrow><annotation>n</annotation></semantics></math>n 的二进制字符串 <math><semantics><mrow><mi>s</mi></mrow><annotation>s</annotation></semantics></math>s，由 0 和 1 组成。我们需要构建一个行数为 <math><semantics><mrow><mi>n</mi></mrow><annotation>n</annotation></semantics></math>n，列数为 <math><semantics><mrow><mi>n</mi></mrow><annotation>n</annotation></semantics></math>n 的方表，由 0 和 1 组成。第一行为原始字符串 <math><semantics><mrow><mi>s</mi></mrow><annotation>s</annotation></semantics></math>s，第二行为字符串 <math><semantics><mrow><mi>s</mi></mrow><annotation>s</annotation></semantics></math>s 向右循环移动一个位置，第三行为字符串 <math><semantics><mrow><mi>s</mi></mrow><annotation>s</annotation></semantics></math>s 向右循环移动两个位置，以此类推。

求表中所有由 0 组成的三角形或矩形的最大面积值。

### 输入描述

输入一个长度为 <math><semantics><mrow><mi>n</mi></mrow><annotation>n</annotation></semantics></math>n 的二进制字符串 <math><semantics><mrow><mi>s</mi></mrow><annotation>s</annotation></semantics></math>s，仅包含 0 和 1 字符，其中 <math><semantics><mrow><mn>1</mn><mo>≤</mo><mi>n</mi><mo>≤</mo><mn>5000</mn></mrow><annotation>1 \\leq n \\leq 5000</annotation></semantics></math>1≤n≤5000。



### 输出描述

输出表中所有由 0 组成的三角形或矩形的最大面积值。

### 示例 1

#### 输入


```
00110
```

#### 输出


```
6
```

---

我们可以证明，由于构造表的方式非常特殊，每一行都是原始二进制串的右循环移位，表中任意一个形状（严格说是其“数字凸包”，也就是该形状中所有单元格对应 <math><semantics><mrow><mi>j</mi><mo>−</mo><mi>i</mi></mrow><annotation>j-i</annotation></semantics></math>j−i（取模 <math><semantics><mrow><mi>n</mi></mrow><annotation>n</annotation></semantics></math>n）组成的区间）的状态只依赖于原串中某个在环上连续的零段。经过简单分析可以证明：

* 若我们选取一个“矩形”（即连续 <math><semantics><mrow><mi>h</mi></mrow><annotation>h</annotation></semantics></math>h 行、连续 <math><semantics><mrow><mi>w</mi></mrow><annotation>w</annotation></semantics></math>w 列）的子区域，其所有单元格对应的 <math><semantics><mrow><mi>j</mi><mo>−</mo><mi>i</mi></mrow><annotation>j-i</annotation></semantics></math>j−i值集合为

<math><semantics><mrow><mo>{</mo><mi>D</mi><mo>−</mo><mo>(</mo><mi>h</mi><mo>−</mo><mn>1</mn><mo>)</mo><mo>,</mo><mi>D</mi><mo>−</mo><mi>h</mi><mo>+</mo><mn>2</mn><mo>,</mo><mo>…</mo><mo>,</mo><mi>D</mi><mo>+</mo><mi>w</mi><mo>−</mo><mn>1</mn><mo>}</mo></mrow><annotation>\\{\\, D - (h-1),\\, D-h+2,\\dots,\\,D+w-1\\,\\}</annotation></semantics></math>{D−(h−1),D−h+2,…,D+w−1}

  （其中 <math><semantics><mrow><mi>D</mi></mrow><annotation>D</annotation></semantics></math>D 为某个偏移量），这实际上是一个长度为 <math><semantics><mrow><mi>w</mi><mo>+</mo><mi>h</mi><mo>−</mo><mn>1</mn></mrow><annotation>w+h-1</annotation></semantics></math>w+h−1 的整数区间（注意区间中相邻两行之间会有重叠）。显然要使区域内全为 0，必须原串中存在一个（环上连续的）零段长度至少为 <math><semantics><mrow><mi>w</mi><mo>+</mo><mi>h</mi><mo>−</mo><mn>1</mn></mrow><annotation>w+h-1</annotation></semantics></math>w+h−1；而在非全零（即 <math><semantics><mrow><mi>w</mi><mo>+</mo><mi>h</mi><mo>−</mo><mn>1</mn><mo><</mo><mi>n</mi></mrow><annotation>w+h-1<n</annotation></semantics></math>w+h−1<n）的情形中，经过取最优选择可以证明最大矩形面积为

<math><semantics><mrow><mi>R</mi><mo>(</mo><mi>L</mi><mo>)</mo><mo>\=</mo><mo>⌊</mo><mfrac><mrow><mi>L</mi><mo>+</mo><mn>1</mn></mrow><mn>2</mn></mfrac><mo>⌋</mo><mo>⋅</mo><mo>⌈</mo><mfrac><mrow><mi>L</mi><mo>+</mo><mn>1</mn></mrow><mn>2</mn></mfrac><mo>⌉</mo><mo>,</mo></mrow><annotation>R(L)=\\lfloor\\frac{L+1}{2}\\rfloor\\cdot\\lceil\\frac{L+1}{2}\\rceil,</annotation></semantics></math>R(L)\=⌊2L+1​⌋⋅⌈2L+1​⌉,

  其中 <math><semantics><mrow><mi>L</mi></mrow><annotation>L</annotation></semantics></math>L 表示原串（视为环状）中零的最长连续段长度。

* 同理，设我们只允许“直角三角形”形状（例如以左上角为直角，每往下一行比上一行多 1 个单元，面积为 <math><semantics><mrow><mn>1</mn><mo>+</mo><mn>2</mn><mo>+</mo><mo>⋯</mo><mo>+</mo><mi>h</mi><mo>\=</mo><mfrac><mrow><mi>h</mi><mo>(</mo><mi>h</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mn>2</mn></mfrac></mrow><annotation>1+2+\\cdots+h=\\frac{h(h+1)}2</annotation></semantics></math>1+2+⋯+h\=2h(h+1)​），那么设三角形高为 <math><semantics><mrow><mi>h</mi></mrow><annotation>h</annotation></semantics></math>h，它“用到”的<math><semantics><mrow><mi>j</mi><mo>−</mo><mi>i</mi></mrow><annotation>j-i</annotation></semantics></math>j−i值正好组成一个长度为 <math><semantics><mrow><mi>h</mi></mrow><annotation>h</annotation></semantics></math>h 的区间，因此需要 <math><semantics><mrow><mi>h</mi><mo>≤</mo><mi>L</mi></mrow><annotation>h\\le L</annotation></semantics></math>h≤L；这样最大的三角形面积为

<math><semantics><mrow><mi>T</mi><mo>(</mo><mi>L</mi><mo>)</mo><mo>\=</mo><mfrac><mrow><mi>L</mi><mo>(</mo><mi>L</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mn>2</mn></mfrac><mi>.</mi></mrow><annotation>T(L)=\\frac{L(L+1)}2.</annotation></semantics></math>T(L)\=2L(L+1)​.

很容易验证，当 <math><semantics><mrow><mi>L</mi><mo>≥</mo><mn>2</mn></mrow><annotation>L\\ge2</annotation></semantics></math>L≥2 时

<math><semantics><mrow><mi>T</mi><mo>(</mo><mi>L</mi><mo>)</mo><mo>\=</mo><mfrac><mrow><mi>L</mi><mo>(</mo><mi>L</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mn>2</mn></mfrac><mo>></mo><mo>⌊</mo><mfrac><mrow><mi>L</mi><mo>+</mo><mn>1</mn></mrow><mn>2</mn></mfrac><mo>⌋</mo><mo>⋅</mo><mo>⌈</mo><mfrac><mrow><mi>L</mi><mo>+</mo><mn>1</mn></mrow><mn>2</mn></mfrac><mo>⌉</mo><mo>\=</mo><mi>R</mi><mo>(</mo><mi>L</mi><mo>)</mo><mo>,</mo></mrow><annotation>T(L)=\\frac{L(L+1)}2> \\lfloor\\frac{L+1}{2}\\rfloor\\cdot\\lceil\\frac{L+1}{2}\\rceil=R(L),</annotation></semantics></math>T(L)\=2L(L+1)​>⌊2L+1​⌋⋅⌈2L+1​⌉\=R(L),

即非全零情况下最佳面积取决于“零三角形”形状。注意：若原串全为 0，则表中所有单元均为 0，这时当然最大面积为整个表面积 <math><semantics><mrow><mi>n</mi><mo>×</mo><mi>n</mi></mrow><annotation>n\\times n</annotation></semantics></math>n×n（因为 <math><semantics><mrow><msup><mi>n</mi><mn>2</mn></msup><mo>></mo><mfrac><mrow><mi>n</mi><mo>(</mo><mi>n</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mn>2</mn></mfrac></mrow><annotation>n^2>\\frac{n(n+1)}2</annotation></semantics></math>n2>2n(n+1)​ ）。

综上，我们可以先扫描原串（按环状计）求出最长连续 0 的长度 <math><semantics><mrow><mi>L</mi></mrow><annotation>L</annotation></semantics></math>L（如果不存在 0，则答案为 0）；接下来判断：

* 若 <math><semantics><mrow><mi>L</mi><mo>\=</mo><mi>n</mi></mrow><annotation>L=n</annotation></semantics></math>L\=n（全零串），答案为 <math><semantics><mrow><msup><mi>n</mi><mn>2</mn></msup></mrow><annotation>n^2</annotation></semantics></math>n2；
* 否则答案为 <math><semantics><mrow><mstyle><mfrac><mrow><mi>L</mi><mo>(</mo><mi>L</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mn>2</mn></mfrac></mstyle></mrow><annotation>\\dfrac{L(L+1)}2</annotation></semantics></math>2L(L+1)​（即构成某个“零三角形”的面积最大值）。

下面给出 Java 代码实现，时间复杂度 <math><semantics><mrow><mi>O</mi><mo>(</mo><mi>n</mi><mo>)</mo></mrow><annotation>O(n)</annotation></semantics></math>O(n)：

---

java

<button>复制</button>

```javascript
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        // 读取输入的二进制字符串（原串s）
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine().trim();
        int n = s.length();
        
        // 计算原串中（按环状）最长连续0的长度 L
        int L = 0;
        int curr = 0;
        // 扫描一遍（不考虑环首与环尾相连的情况）
        for (int i = 0; i < n; i++) {
            if (s.charAt(i) == '0') {
                curr++;
                if (curr > L) {
                    L = curr;
                }
            } else {
                curr = 0;
            }
        }
        // 若首尾均为 '0'，则尝试用环状连接更新 L
        if (n > 0 && s.charAt(0) == '0' && s.charAt(n - 1) == '0') {
            int prefix = 0, suffix = 0;
            for (int i = 0; i < n && s.charAt(i) == '0'; i++) {
                prefix++;
            }
            for (int i = n - 1; i >= 0 && s.charAt(i) == '0'; i--) {
                suffix++;
            }
            if (prefix + suffix > L) {
                L = prefix + suffix;
            }
            // 注意 L 最多为 n（原串长度）
            if (L > n) {
                L = n;
            }
        }
        
        long ans = 0;
        // 如果原串中没有0，答案为0
        if (L == 0) {
            ans = 0;
        }
        // 原串全为0，则表中的每个元素均为0，答案为 n*n
        else if (L == n) {
            ans = (long) n * n;
        }
        // 否则最佳面积来源于“零三角形”，面积为 L*(L+1)/2
        else {
            ans = (long) L * (L + 1) / 2;
        }
        
        System.out.println(ans);
    }
}
```

---

### 代码说明

1. **求最长连续 0 段（环状）**  
   先正向扫描统计连续 0 数；此外注意如果串首和串尾都是 0，则它们在环状上可以连在一起，故额外计算首部和尾部 0 的个数，并更新最长连续数 <math><semantics><mrow><mi>L</mi></mrow><annotation>L</annotation></semantics></math>L（但 <math><semantics><mrow><mi>L</mi></mrow><annotation>L</annotation></semantics></math>L 最大不超过 <math><semantics><mrow><mi>n</mi></mrow><annotation>n</annotation></semantics></math>n）。

2. **判断答案**

   * 若 <math><semantics><mrow><mi>L</mi><mo>\=</mo><mn>0</mn></mrow><annotation>L=0</annotation></semantics></math>L\=0（没有 0），答案为 0。
   * 若 <math><semantics><mrow><mi>L</mi><mo>\=</mo><mi>n</mi></mrow><annotation>L=n</annotation></semantics></math>L\=n（全 0 串），整表全为 0，答案为 <math><semantics><mrow><mi>n</mi><mo>×</mo><mi>n</mi></mrow><annotation>n \\times n</annotation></semantics></math>n×n；
   * 否则答案为 <math><semantics><mrow><mfrac><mrow><mi>L</mi><mo>(</mo><mi>L</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mn>2</mn></mfrac></mrow><annotation>\\frac{L(L+1)}{2}</annotation></semantics></math>2L(L+1)​（这正是构成某个“零三角形”时所能达到的最大面积）。

这样我们就实现了在 <math><semantics><mrow><mi>O</mi><mo>(</mo><mi>n</mi><mo>)</mo></mrow><annotation>O(n)</annotation></semantics></math>O(n) 内求解表中所有由 0 组成的（三角形或矩形）区域的最大面积值。

---

### 小结

由于表中每个单元的值仅取决于 <math><semantics><mrow><mi>s</mi><mo>\[</mo><mo>(</mo><mi>j</mi><mo>−</mo><mi>i</mi><mo>)</mo><mo><mrow><mi>m</mi><mi>o</mi><mi>d</mi></mrow></mo><mi>n</mi><mo>\]</mo></mrow><annotation>s\[(j-i) \\bmod n\]</annotation></semantics></math>s\[(j−i)modn\]，整个问题转化为求原串（环状）中最长的零段长度 <math><semantics><mrow><mi>L</mi></mrow><annotation>L</annotation></semantics></math>L；并证明在非全零情况下，“零直角三角形”的面积为

<math><semantics><mrow><mfrac><mrow><mi>L</mi><mo>(</mo><mi>L</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mn>2</mn></mfrac><mo>,</mo></mrow><annotation>\\frac{L(L+1)}2,</annotation></semantics></math>2L(L+1)​,

始终大于同样受限制的矩形面积。因此最终答案为

* 如果 <math><semantics><mrow><mi>s</mi></mrow><annotation>s</annotation></semantics></math>s 全 0：答案为 <math><semantics><mrow><msup><mi>n</mi><mn>2</mn></msup></mrow><annotation>n^2</annotation></semantics></math>n2；
* 否则：答案为 <math><semantics><mrow><mfrac><mrow><mi>L</mi><mo>(</mo><mi>L</mi><mo>+</mo><mn>1</mn><mo>)</mo></mrow><mn>2</mn></mfrac></mrow><annotation>\\frac{L(L+1)}{2}</annotation></semantics></math>2L(L+1)​。

这种思路不仅降低了时间复杂度（仅 <math><semantics><mrow><mi>O</mi><mo>(</mo><mi>n</mi><mo>)</mo></mrow><annotation>O(n)</annotation></semantics></math>O(n)），同时也利用了构造矩阵时的“循环移位”这一特殊性质。

---

### 题目描述

米小游拿到了一个数组，她有若干次询问，每次询问输入一个 <math><semantics><mrow><mi>x</mi></mrow><annotation>x</annotation></semantics></math>x，她希望你判断 <math><semantics><mrow><mi>x</mi></mrow><annotation>x</annotation></semantics></math>x 是否能由数组中的两个元素相乘得出。用数学语言描述，你需要寻找到两个下标 <math><semantics><mrow><mi>i</mi></mrow><annotation>i</annotation></semantics></math>i 和 <math><semantics><mrow><mi>j</mi></mrow><annotation>j</annotation></semantics></math>j（<math><semantics><mrow><mi>i</mi><mo><</mo><mi>j</mi></mrow><annotation>i < j</annotation></semantics></math>i<j），满足 <math><semantics><mrow><msub><mi>a</mi><mi>i</mi></msub><mo>×</mo><msub><mi>a</mi><mi>j</mi></msub><mo>\=</mo><mi>x</mi></mrow><annotation>a\_i \\times a\_j = x</annotation></semantics></math>ai​×aj​\=x。

### 输入描述

第一行输入一个正整数 <math><semantics><mrow><mi>n</mi></mrow><annotation>n</annotation></semantics></math>n，代表数组的大小。

第二行输入 <math><semantics><mrow><mi>n</mi></mrow><annotation>n</annotation></semantics></math>n 个正整数 <math><semantics><mrow><msub><mi>a</mi><mi>i</mi></msub></mrow><annotation>a\_i</annotation></semantics></math>ai​，代表数组的元素。

第三行输入一个正整数 <math><semantics><mrow><mi>q</mi></mrow><annotation>q</annotation></semantics></math>q，代表询问次数。

接下来的 <math><semantics><mrow><mi>q</mi></mrow><annotation>q</annotation></semantics></math>q 行，每行输入一个正整数 <math><semantics><mrow><mi>x</mi></mrow><annotation>x</annotation></semantics></math>x，代表一次询问。

* <math><semantics><mrow><mn>1</mn><mo>≤</mo><mi>n</mi><mo>,</mo><mi>q</mi><mo>≤</mo><msup><mn>10</mn><mn>5</mn></msup></mrow><annotation>1 \\leq n, q \\leq 10^5</annotation></semantics></math>1≤n,q≤105
* <math><semantics><mrow><mn>1</mn><mo>≤</mo><msub><mi>a</mi><mi>i</mi></msub><mo>,</mo><mi>x</mi><mo>≤</mo><msup><mn>10</mn><mn>6</mn></msup></mrow><annotation>1 \\leq a\_i, x \\leq 10^6</annotation></semantics></math>1≤ai​,x≤106

### 输出描述

对于每次询问，如果无法找到两数乘积等于 <math><semantics><mrow><mi>x</mi></mrow><annotation>x</annotation></semantics></math>x，输出 `-1 -1`。

否则输出 <math><semantics><mrow><mi>i</mi></mrow><annotation>i</annotation></semantics></math>i 和 <math><semantics><mrow><mi>j</mi></mrow><annotation>j</annotation></semantics></math>j（<math><semantics><mrow><mi>i</mi><mo><</mo><mi>j</mi></mrow><annotation>i < j</annotation></semantics></math>i<j），用空格隔开，代表 <math><semantics><mrow><msub><mi>a</mi><mi>i</mi></msub><mo>×</mo><msub><mi>a</mi><mi>j</mi></msub><mo>\=</mo><mi>x</mi></mrow><annotation>a\_i \\times a\_j = x</annotation></semantics></math>ai​×aj​\=x。有多解时输出任意即可。

### 示例 1

#### 输入

basic

<button>复制</button>

```
5
1 2 3 2 4
2
4
5
```

#### 输出

basic

<button>复制</button>

```
2 4
-1 -1
```

#### 说明

* 第一组询问，输出 `1 5` 也是可以的。
* 第二组询问，显然无法找到两个元素相乘等于 5。

---

下面给出 Java 实现。思路是：预处理数组中每个数字在数组中第一次出现和第二次出现的位置，下标记为 1-indexed。这样，对于两个数字 <math><semantics><mrow><mi>a</mi></mrow><annotation>a</annotation></semantics></math>a 和 <math><semantics><mrow><mi>b</mi></mrow><annotation>b</annotation></semantics></math>b 来说：

* 若 <math><semantics><mrow><mi>a</mi><mo>≠</mo><mi>b</mi></mrow><annotation>a \\neq b</annotation></semantics></math>a\\\=b 只需检查数组中是否均出现过；
* 若 <math><semantics><mrow><mi>a</mi><mo>\=</mo><mi>b</mi></mrow><annotation>a=b</annotation></semantics></math>a\=b 则需要出现两次以上。

对于每次询问 <math><semantics><mrow><mi>x</mi></mrow><annotation>x</annotation></semantics></math>x ，我们枚举 <math><semantics><mrow><mi>d</mi></mrow><annotation>d</annotation></semantics></math>d 从 1 到 <math><semantics><mrow><msqrt><mi>x</mi></msqrt></mrow><annotation>\\sqrt{x}</annotation></semantics></math>x​（即所有可能的因子），若 <math><semantics><mrow><mi>d</mi></mrow><annotation>d</annotation></semantics></math>d 能整除 <math><semantics><mrow><mi>x</mi></mrow><annotation>x</annotation></semantics></math>x 则候选另一因子为 <math><semantics><mrow><msub><mi>d</mi><mn>2</mn></msub><mo>\=</mo><mi>x</mi><mi>/</mi><mi>d</mi></mrow><annotation>d\_2=x/d</annotation></semantics></math>d2​\=x/d。对候选对：

* 若 <math><semantics><mrow><mi>d</mi><mo>\=</mo><mo>\=</mo><msub><mi>d</mi><mn>2</mn></msub></mrow><annotation>d==d\_2</annotation></semantics></math>d\==d2​，必须保证数组中该数字出现次数至少为 2。
* 否则只要数组中同时出现了 <math><semantics><mrow><mi>d</mi></mrow><annotation>d</annotation></semantics></math>d 和 <math><semantics><mrow><msub><mi>d</mi><mn>2</mn></msub></mrow><annotation>d\_2</annotation></semantics></math>d2​。

输出时注意需满足 <math><semantics><mrow><mi>i</mi><mo><</mo><mi>j</mi></mrow><annotation>i<j</annotation></semantics></math>i<j 的顺序，输出时将两个下标排序后输出。

时间复杂度：每次询问最多枚举 <math><semantics><mrow><msqrt><mi>x</mi></msqrt></mrow><annotation>\\sqrt{x}</annotation></semantics></math>x​ 个因子，由于 <math><semantics><mrow><mi>x</mi><mo>≤</mo><mn>1</mn><mo>×</mo><msup><mn>10</mn><mn>6</mn></msup></mrow><annotation>x\\le1\\times10^6</annotation></semantics></math>x≤1×106 所以每次最多约 1000 次循环，整体时间复杂度为 <math><semantics><mrow><mi>O</mi><mo>(</mo><mi>q</mi><msqrt><mi>x</mi></msqrt><mo>)</mo></mrow><annotation>O(q\\sqrt{x})</annotation></semantics></math>O(qx​) 。

下面给出完整代码：

---

java

<button>复制</button>

```javascript
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws IOException {
        // 使用 BufferedReader 提高输入效率
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        // 读取数组大小 n
        st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());

        // 因为数字范围 (1 <= a_i <= 1e6)，预分配大小为 1e6+1 的数组
        int MAX = 1000000;
        // firstIndex[v] 表示数字 v 在数组中第一次出现的位置（1-indexed），若未出现值为 0
        int[] firstIndex = new int[MAX + 1];
        // secondIndex[v] 表示数字 v 在数组中第二次出现的位置（1-indexed），若不足两次出现值为 0
        int[] secondIndex = new int[MAX + 1];

        // 读取数组元素
        st = new StringTokenizer(br.readLine());
        for (int i = 1; i <= n; i++) {
            int num = Integer.parseInt(st.nextToken());
            if (firstIndex[num] == 0) {
                firstIndex[num] = i;
            } else if (secondIndex[num] == 0) {
                secondIndex[num] = i;
            }
        }
        
        // 读取查询次数 q
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        
        // 对每个查询进行处理
        for (int qi = 0; qi < q; qi++) {
            // 每个查询给定 x
            int x = Integer.parseInt(br.readLine().trim());
            boolean found = false;
            
            // 枚举可能的因子 d，从 1 到 sqrt(x)
            int sqrtX = (int) Math.sqrt(x);
            for (int d = 1; d <= sqrtX; d++) {
                if (x % d != 0) {
                    continue;  // d 不是 x 的因子
                }
                
                int d2 = x / d;
                // 若 d 或 d2 超出数组中可能的数字范围，则直接跳过
                if (d > MAX || d2 > MAX) {
                    continue;
                }
                
                if (d == d2) {
                    // 两个因子相同，必须存在两次及以上出现
                    if (firstIndex[d] != 0 && secondIndex[d] != 0) {
                        sb.append(firstIndex[d]).append(" ").append(secondIndex[d]).append("\n");
                        found = true;
                        break;
                    }
                } else {
                    // 两个因子不同，只需两者均出现即可
                    if (firstIndex[d] != 0 && firstIndex[d2] != 0) {
                        int i1 = firstIndex[d];
                        int i2 = firstIndex[d2];
                        // 输出两个下标，保证 i1 < i2
                        if (i1 > i2) {
                            int temp = i1;
                            i1 = i2;
                            i2 = temp;
                        }
                        sb.append(i1).append(" ").append(i2).append("\n");
                        found = true;
                        break;
                    }
                }
            }
            
            if (!found) {
                sb.append("-1 -1\n");
            }
        }
        
        System.out.print(sb.toString());
    }
}
```

---

### 代码说明

1. **预处理**  
   对于给定的数组，我们利用两个数组 `firstIndex` 和 `secondIndex` 分别记录每个数字第一次和第二次出现的位置，方便后续判断同一个数字能否作为一对两个相乘相等于 <math><semantics><mrow><mi>x</mi></mrow><annotation>x</annotation></semantics></math>x 的候选。

2. **查询处理**  
   对每个查询 <math><semantics><mrow><mi>x</mi></mrow><annotation>x</annotation></semantics></math>x，枚举 <math><semantics><mrow><mn>1</mn><mo>≤</mo><mi>d</mi><mo>≤</mo><msqrt><mi>x</mi></msqrt></mrow><annotation>1 \\leq d \\leq \\sqrt{x}</annotation></semantics></math>1≤d≤x​：

   * 若 <math><semantics><mrow><mi>d</mi></mrow><annotation>d</annotation></semantics></math>d 不是 <math><semantics><mrow><mi>x</mi></mrow><annotation>x</annotation></semantics></math>x 的因数，跳过；
   * 当 <math><semantics><mrow><mi>d</mi></mrow><annotation>d</annotation></semantics></math>d 正好为平方根（即 <math><semantics><mrow><mi>d</mi><mo>\=</mo><mi>x</mi><mi>/</mi><mi>d</mi></mrow><annotation>d = x / d</annotation></semantics></math>d\=x/d）时判断是否出现至少两次；
   * 否则判断数字 <math><semantics><mrow><mi>d</mi></mrow><annotation>d</annotation></semantics></math>d 与 <math><semantics><mrow><mi>x</mi><mi>/</mi><mi>d</mi></mrow><annotation>x/d</annotation></semantics></math>x/d 是否均在数组中出现。

3. **输出**  
   如果找到满足条件的因子对，则输出它们在数组中的下标（确保 <math><semantics><mrow><mi>i</mi><mo><</mo><mi>j</mi></mrow><annotation>i<j</annotation></semantics></math>i<j）；如果所有候选中均没有满足，则输出 `-1 -1` 。

该算法总体时间复杂度为 <math><semantics><mrow><mi>O</mi><mo>(</mo><mi>q</mi><msqrt><mi>x</mi></msqrt><mo>)</mo></mrow><annotation>O(q\\sqrt{x})</annotation></semantics></math>O(qx​)，足以应对 <math><semantics><mrow><mi>q</mi><mo>≤</mo><msup><mn>10</mn><mn>5</mn></msup></mrow><annotation>q\\le 10^5</annotation></semantics></math>q≤105 的情形。
