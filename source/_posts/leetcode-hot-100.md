---
title: Leetcode hot 100
date: '2024-10-14 11:28:11'
updated: '2024-10-17 06:13:25'
categories:
  - LeetCode
tags:
  - LeetCode
summary: >
  1 哈希 1. 两数之和


  49. 字母异位词分组

  > 给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。   字母异位词 是由重新排列源单词的所有字母得到的一个新单词。

  > 思路：   >
  由于互为字母异位词的两个字符串包含的字母相同，因此对两个字符串分别进行排序之后得到的字符串一定是相同的，故可以将排序之后的字符串作为哈希表的键。



  128. 最长连续序
---
## 1 哈希
### 1. 两数之和
```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> hashMap = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            if (hashMap.containsKey(target - nums[i])) {
                return new int[] { hashMap.get(target - nums[i]), i };
            }
            hashMap.put(nums[i], i);
        }
        return new int[0];
    }
}
```

### 49. 字母异位词分组

> 给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。  
字母异位词 是由重新排列源单词的所有字母得到的一个新单词。

> 思路：  
> 由于互为字母异位词的两个字符串包含的字母相同，因此对两个字符串分别进行排序之后得到的字符串一定是相同的，故可以将排序之后的字符串作为哈希表的键。

```java
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> hashMap = new HashMap<>();
        for (String str : strs) {
            char[] charArray = str.toCharArray();
            Arrays.sort(charArray);
            String keyString = new String(charArray);
            List<String> list = hashMap.getOrDefault(keyString, new ArrayList<String>());
            list.add(str);
            hashMap.put(keyString, list);
        }
        return new ArrayList<List<String>>(hashMap.values());
    }
}
```

### 128. 最长连续序列
给定一个未排序的整数数组 nums，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。

```java
class Solution {
    public int longestConsecutive(int[] nums) {
        if (nums.length == 0 || nums.length == 1) return nums.length;
        HashSet<Integer> hashSet = new HashSet<>();
        for (int num : nums) {
            hashSet.add(num);
        }
        if (hashSet.size() == 1) return 1;
        Object[] array = hashSet.toArray();
        Arrays.sort(array);
        int max = 0;
        int cnt = 1;
        for (int i = 0; i < array.length - 1; i++) {
            if ((int) array[i] + 1 == (int) array[i + 1]) {
                cnt++;
            } else {
                cnt = 1;
            }
            max = Math.max(max, cnt);
        }
        return max;
    }
}
```

## 2 双指针
### 283. 移动零

```java
class Solution {
    public void moveZeroes(int[] nums) {
        int slow = 0;
        int fast = 0;
        while (fast < nums.length) {
            if (nums[fast] != 0) {
                nums[slow] = nums[fast];
                slow++;
            }
            fast++;
        }
        for (int i = slow; i < nums.length; i++) {
            nums[i] = 0;
        }
    }
}
```

### 11. 盛最多水的容器
```java
class Solution {
    public int maxArea(int[] height) {
        int left = 0;
        int right = height.length - 1;
        int area = 0;
        while (left < right) {
            if (height[left] < height[right]) {
                area = Math.max(area, (right - left) * height[left]);
                left++;
            } else {
                area = Math.max(area, (right - left) * height[right]);
                right--;
            }
        }
        return area;
    }
}
```

### 15. 三数之和

1. **排序**：首先将数组排序，这样可以方便地使用双指针来进行查找。
2. **遍历数组**：对于每个元素 `nums[i]`，我们将其视为三元组中的第一个数，然后通过双指针来查找剩下的两个数。
3. **双指针查找**：对于当前固定的 `nums[i]`，我们设定两个指针，`left` 指向 `i+1`，`right` 指向数组的末尾。我们检查 `nums[i] + nums[left] + nums[right]`：
   - 如果和为零，记录这个三元组，并同时移动 `left` 和 `right`。
   - 如果和小于零，说明需要让和变大，所以移动 `left`。
   - 如果和大于零，说明需要让和变小，所以移动 `right`。
4. **跳过重复元素**：为了避免重复结果，在移动指针时需要跳过相同的数字。

```java
public class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        if (nums == null || nums.length < 3) {
            return result;
        }
        // 1. 排序数组
        Arrays.sort(nums);
        // 2. 遍历数组
        for (int i = 0; i < nums.length - 2; i++) {
            // 跳过重复的数字
            if (i > 0 && nums[i] == nums[i - 1]) {
                continue;
            }
            // 初始化双指针
            int left = i + 1;
            int right = nums.length - 1;
            // 3. 双指针查找
            while (left < right) {
                int sum = nums[i] + nums[left] + nums[right];

                if (sum == 0) {
                    result.add(Arrays.asList(nums[i], nums[left], nums[right]));
                    // 移动左指针并跳过重复值
                    while (left < right && nums[left] == nums[left + 1]) {
                        left++;
                    }
                    // 移动右指针并跳过重复值
                    while (left < right && nums[right] == nums[right - 1]) {
                        right--;
                    }
                    // 移动指针
                    left++;
                    right--;
                } else if (sum < 0) {
                    // 如果和小于 0，移动左指针
                    left++;
                } else {
                    // 如果和大于 0，移动右指针
                    right--;
                }
            }
        }
        return result;
    }
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.threeSum(new int[]{-1, 0, 1, 2, -1, -4})); // 输出: [[-1, -1, 2], [-1, 0, 1]]
        System.out.println(solution.threeSum(new int[]{0, 1, 1}));             // 输出: []
        System.out.println(solution.threeSum(new int[]{0, 0, 0}));             // 输出: [[0, 0, 0]]
    }
}
```

## 3 滑动窗口
### 3. 无重复字符的最长子串

```java
class Solution {
    public int lengthOfLongestSubstring(String s) {
        HashMap<Character, Integer> map = new HashMap<>();
        int maxLen = 0;//用于记录最大不重复子串的长度
        int left = 0;//滑动窗口左指针
        for (int i = 0; i < s.length() ; i++)
        {
            /**
            1、首先，判断当前字符是否包含在map中，如果不包含，将该字符添加到map（字符，字符在数组下标）,
             此时没有出现重复的字符，左指针不需要变化。此时不重复子串的长度为：i-left+1，与原来的maxLen比较，取最大值；
            2、如果当前字符 ch 包含在 map中，此时有2类情况：
             1）当前字符包含在当前有效的子段中，如：abca，当我们遍历到第二个a，当前有效最长子段是 abc，我们又遍历到a，
             那么此时更新 left 为 map.get(a)+1=1，当前有效子段更新为 bca；
             2）当前字符不包含在当前最长有效子段中，如：abba，我们先添加a,b进map，此时left=0，我们再添加b，发现map中包含b，
             而且b包含在最长有效子段中，就是1）的情况，我们更新 left=map.get(b)+1=2，此时子段更新为 b，而且map中仍然包含a，map.get(a)=0；
             随后，我们遍历到a，发现a包含在map中，且map.get(a)=0，如果我们像1）一样处理，就会发现 left=map.get(a)+1=1，实际上，left此时
             应该不变，left始终为2，子段变成 ba才对。
             为了处理以上2类情况，我们每次更新left，left=Math.max(left , map.get(ch)+1).
             另外，更新left后，不管原来的 s.charAt(i) 是否在最长子段中，我们都要将 s.charAt(i) 的位置更新为当前的i，
             因此此时新的 s.charAt(i) 已经进入到 当前最长的子段中！
             */
            if(map.containsKey(s.charAt(i)))
            {
                left = Math.max(left , map.get(s.charAt(i))+1);
            }
            //不管是否更新left，都要更新 s.charAt(i) 的位置！
            map.put(s.charAt(i) , i);
            maxLen = Math.max(maxLen , i-left+1);
        }
        return maxLen;
    }
}
```
### [438. 找到字符串中所有字母异位词](https://leetcode.cn/problems/find-all-anagrams-in-a-string/)

要解决这个问题，我们可以使用滑动窗口算法。具体地说，滑动窗口可以帮助我们逐渐遍历字符串 `s`，同时维护一个窗口，该窗口的大小等于字符串 `p` 的长度，并检查该窗口内的子串是否为 `p` 的异位词。

1. **计数器**：首先，创建一个字符计数器来存储字符串 `p` 中每个字符的频率。
2. **滑动窗口**：接着，我们使用一个滑动窗口来遍历字符串 `s`。窗口的大小与字符串 `p` 的长度相同。
3. **匹配**：每次窗口滑动时，检查窗口内的子串是否跟 `p` 的字符频率匹配。如果匹配，则记录当前窗口的起始索引。
4. **更新窗口**：每次滑动时，我们通过添加一个新的字符进入窗口，并移除窗口左边的字符，从而保持窗口的大小不变。

```java
public class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        List<Integer> result = new ArrayList<>();
        if (s == null || p == null || s.length() < p.length()) {
            return result;
        }
        // 创建两个数组记录字母频率
        int[] pCount = new int[26];
        int[] sCount = new int[26];
        // 先计算字符串 p 中的字符频率
        for (char c : p.toCharArray()) {
            pCount[c - 'a']++;
        }
        int windowSize = p.length();
        int sLen = s.length();
        // 初始化窗口，计算第一个窗口的字符频率
        for (int i = 0; i < windowSize; i++) {
            sCount[s.charAt(i) - 'a']++;
        }
        // 检查第一个窗口是否是异位词
        if (matches(pCount, sCount)) {
            result.add(0);
        }
        // 滑动窗口，开始从第二个字符开始遍历
        for (int i = windowSize; i < sLen; i++) {
            // 添加新的字符到窗口
            sCount[s.charAt(i) - 'a']++;
            // 移除窗口最左边的字符
            sCount[s.charAt(i - windowSize) - 'a']--;

            // 检查当前窗口是否是异位词
            if (matches(pCount, sCount)) {
                result.add(i - windowSize + 1);
            }
        }
        return result;
    }
    // 检查两个频率数组是否相等
    private boolean matches(int[] pCount, int[] sCount) {
        for (int i = 0; i < 26; i++) {
            if (pCount[i] != sCount[i]) {
                return false;
            }
        }
        return true;
    }
    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.findAnagrams("cbaebabacd", "abc")); // 输出: [0, 6]
        System.out.println(solution.findAnagrams("abab", "ab"));         // 输出: [0, 1, 2]
    }
}
```

## 4 子串
### [560. 和为 K 的子数组](https://leetcode.cn/problems/subarray-sum-equals-k/)
1. **前缀和**：前缀和是指数组从起始位置到当前位置的所有元素的和。假设 `sum(i)` 表示数组从下标 `0` 到 `i` 位置元素的和，那么我们可以通过计算两个前缀和的差来得到某个子数组的和。
2. **公式**：如果我们知道 `sum(j) - sum(i) == k`，那么数组 `nums[i+1...j]` 的和为 `k`。因此，问题可以转化为寻找之前的某个前缀和 `sum(i)`，使得 `sum(j) - sum(i) == k`。
3. **哈希表**：我们使用哈希表来记录每个前缀和出现的次数。对于每个新的前缀和 `sum(j)`，我们查看是否存在 `sum(i)` 使得 `sum(j) - sum(i) = k`，如果存在，则说明找到了一个子数组。

```java
import java.util.HashMap;

class Solution {
    public int subarraySum(int[] nums, int k) {
        // 用于记录前缀和出现的次数
        HashMap<Integer, Integer> prefixSumMap = new HashMap<>();
        // 初始化前缀和为 0 的情况
        prefixSumMap.put(0, 1);

        int count = 0;
        int sum = 0;

        // 遍历数组
        for (int num : nums) {
            // 更新当前前缀和
            sum += num;

            // 检查是否存在前缀和满足 sum - k
            if (prefixSumMap.containsKey(sum - k)) {
                count += prefixSumMap.get(sum - k);
            }

            // 更新当前前缀和在哈希表中的次数
            prefixSumMap.put(sum, prefixSumMap.getOrDefault(sum, 0) + 1);
        }

        return count;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.subarraySum(new int[]{1, 1, 1}, 2)); // 输出: 2
        System.out.println(solution.subarraySum(new int[]{1, 2, 3}, 3)); // 输出: 2
    }
}
```


## 5 普通数组
### 53. 最大子数组和
```java
class Solution {
    public int maxSubArray(int[] nums) {
        int res = nums[0];
        int sum = 0;
        for (int num : nums) {
            sum = Math.max(num, sum + num);
            res = Math.max(res, sum);
        }
        return res;
    }
}
```

### 56. 合并区间 Todo
```java
class Solution {
    public int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, new Comparator<int[]>() {
            public int compare(int[] interval1, int[] interval2) {
                return interval1[0] - interval2[0];
            }
        });
        ArrayList<int[]> arrayList = new ArrayList<int[]>();
        for (int i = 0; i < intervals.length; i++) {
            int L = intervals[i][0], R = intervals[i][1];
            if (arrayList.size() == 0 || arrayList.get(arrayList.size() - 1)[1] < L) {
                arrayList.add(new int[] { L, R });
            } else {
                arrayList.get(arrayList.size() - 1)[1] = Math.max(arrayList.get(arrayList.size() - 1)[1], R);
            }
        }
        return arrayList.toArray(new int[arrayList.size()][]);
    }
}
```

### 189. 轮转数组
```java
class Solution {
    public void rotate(int[] nums, int k) {
        reverse(nums, 0, nums.length-1);//整个反转
        reverse(nums, 0, k-1);//反转前 k 个
        reverse(nums, k, nums.length-1);//反转后面的
    }
    //翻转数组
    public void reverse(int[] nums, int begin, int end) {
        while (begin < end) {
            int temp = nums[begin];
            nums[begin] = nums[end];
            nums[end] = temp;
            begin = begin + 1;
            end = end - 1;
        }
    }
}
```

### 238. 除自身以外数组的乘积

```java
class Solution {
    public int[] productExceptSelf(int[] nums) {
        int[] ans = new int[nums.length];
        int[] left = new int[nums.length];
        int[] right = new int[nums.length];
        left[0] = 1;
        right[nums.length - 1] = 1;
        for (int i = 1; i < left.length; i++) {
            left[i] = nums[i - 1] * left[i - 1];
        }
        for (int i = right.length - 2; i >= 0; i--) {
            right[i] = nums[i + 1] * right[i + 1];
        }
        for (int i = 0; i < ans.length; i++) {
            ans[i] = left[i] * right[i];
        }
        return ans;
    }
}
```
## 6 矩阵

### 73. 矩阵置零

```java
class Solution {
    public void setZeroes(int[][] matrix) {
        int m = matrix.length;
        int n = matrix[0].length;
        boolean[] flagRow = new boolean[m];
        boolean[] flagCol = new boolean[n];

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (matrix[i][j] == 0) {
                    flagRow[i] = true;
                    flagCol[j] = true;
                }
            }
        }
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (flagRow[i] || flagCol[j]) {
                    matrix[i][j] = 0;
                }
            }
        }
    }
}
```
### [54. 螺旋矩阵](https://leetcode.cn/problems/spiral-matrix/)
```java
public List<Integer> spiralOrder(int[][] matrix) {
    List<Integer> list=new ArrayList<>();
    if(matrix.length==0){
        return list;
    }
    int up=0; //上界
    int down=matrix.length-1; //下界
    int left=0;
    int right=matrix[0].length-1;
    while(true){
        // 向右遍历
        for(int i=left;i<=right;i++){
            list.add(matrix[up][i]);
        }
        if(++up>down)break;
        // 向下遍历
        for(int i=up;i<=down;i++){
            list.add(matrix[i][right]);
        }
        if(--right<left) break;
        // 向左遍历
        for(int i=right;i>=left;i--){
            list.add(matrix[down][i]);
        }
        if(--down<up)break;
        // 向上遍历
        for(int i=down;i>=up;i--){
            list.add(matrix[i][left]);
        }
        if(++left>right) break;
    }
    return list;
}
```

### [48. 旋转图像](https://leetcode.cn/problems/rotate-image/)

```java
class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;
        for (int i = 0; i < n / 2; ++i) {
            for (int j = 0; j < (n + 1) / 2; ++j) {
                int temp = matrix[i][j];
                matrix[i][j] = matrix[n - j - 1][i];
                matrix[n - j - 1][i] = matrix[n - i - 1][n - j - 1];
                matrix[n - i - 1][n - j - 1] = matrix[j][n - i - 1];
                matrix[j][n - i - 1] = temp;
            }
        }
    }
}
```

### [240. 搜索二维矩阵 II](https://leetcode.cn/problems/search-a-2d-matrix-ii/)
```java
class Solution {

    public boolean searchMatrix(int[][] matrix, int target) {
        for (int i = 0; i < matrix.length; i++) {
            int binarySearch = binarySearch(matrix[i], target);
            if (binarySearch >= 0) {
                return true;
            }
        }
        return false;
    }
    public int binarySearch(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;
        while (left <= right) {
            int mid = (right - left) / 2 + left;
            if (nums[mid] == target) {
                return mid;
            } else if (nums[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }
}
```

## 7. 链表
### [160. 相交链表](https://leetcode.cn/problems/intersection-of-two-linked-lists/)

```java
public class Solution {
    public ListNode getIntersectionNode(ListNode headA, ListNode headB) {
        ListNode p1 = headA;
        ListNode p2 = headB;
        while (p1 != p2) {
            if (p1 != null) {
                p1 = p1.next;
            } else {
                p1 = headB;
            }
            if (p2 != null) {
                p2 = p2.next;
            } else {
                p2 = headA;
            }
        }
        return p1;
    }
}
```

### [206. 反转链表](https://leetcode.cn/problems/reverse-linked-list/)

```java
class Solution {
    public ListNode reverseList(ListNode head) {
        ListNode cur = head, pre = null;
        while (cur != null) {
            ListNode tmp = cur.next;
            cur.next = pre;
            pre = cur;
            cur = tmp;
        }
        return pre;
    }
}
```

### [234. 回文链表](https://leetcode.cn/problems/palindrome-linked-list/)

```java
class Solution {
    public boolean isPalindrome(ListNode head) {
        List<Integer> list = new ArrayList<>();
        ListNode p = head;
        while (p != null) {
            list.add(p.val);
            p = p.next;
        }
        int left = 0;
        int right = list.size() - 1;
        while (left < right) {
            if (list.get(left) != list.get(right)) {
                return false;
            }
            left++;
            right--;
        }
        return true;
    }
}
```
```java
class Solution {
    ListNode left;
    ListNode right;
    boolean res = true;
    public boolean isPalindrome(ListNode head) {
        left = head;
        reverse(head);
        return res;
    }
    public void reverse(ListNode right) {
        if (right == null) {
            return;
        }
        reverse(right.next);// 走到最后
        if (left.val != right.val) {
            res = false;
        }
        left = left.next;
    }
}
```


### [141. 环形链表](https://leetcode.cn/problems/linked-list-cycle/)
```java
public class Solution {
    public boolean hasCycle(ListNode head) {
        ListNode fast = head;
        ListNode slow = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                return true;
            }
        }
        return false;
    }
}
```

### [142. 环形链表 II](https://leetcode.cn/problems/linked-list-cycle-ii/)

```java
public class Solution {
    public ListNode detectCycle(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                break;// 有环
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
### [21. 合并两个有序链表](https://leetcode.cn/problems/merge-two-sorted-lists/)

```java
class Solution {
    public ListNode mergeTwoLists(ListNode list1, ListNode list2) {
        ListNode dummy = new ListNode(-1);
        ListNode l = dummy;
        ListNode l1 = list1;
        ListNode l2 = list2;
        while (l1 != null && l2 != null) {
            if (l1.val < l2.val) {
                l.next = l1;
                l1 = l1.next;
            } else {
                l.next = l2;
                l2 = l2.next;
            }
            l = l.next;
        }
        if (l1 != null) l.next = l1;
        if (l2 != null) l.next = l2;
        return dummy.next;
    }
}
```

### [2. 两数相加](https://leetcode.cn/problems/add-two-numbers/)

```java
class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        int carry = 0;
        ListNode dummy = new ListNode(0);
        ListNode curr = dummy;
        while (l1 != null || l2 != null) {
            int sum = carry;
            if (l1 != null) {
                sum += l1.val;
                l1 = l1.next;
            }
            if (l2 != null) {
                sum += l2.val;
                l2 = l2.next;
            }
            carry = sum / 10;
            curr.next = new ListNode(sum % 10);
            curr = curr.next;
        }
        if (carry > 0) {
            curr.next = new ListNode(carry);
        }
        return dummy.next;
    }
}
```
### [19. 删除链表的倒数第 N 个结点](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/)
```java
class Solution {
    public ListNode removeNthFromEnd(ListNode head, int n) {
        ListNode dummy = new ListNode(-1);
        dummy.next = head;
        ListNode delNodePrev = removeNthFromEnd1(dummy, n+1);
        delNodePrev.next = delNodePrev.next.next;
        return dummy.next;
    }
    public ListNode removeNthFromEnd1(ListNode head, int n) {
        ListNode p1 = head;
        ListNode p2 = head;
        for (int i = 0; i < n; i++) {
            p1 = p1.next;
        }
        while (p1!=null) {
            p1 = p1.next;p2 = p2.next;
        }
        return p2;
    }
}
```

### [24. 两两交换链表中的节点](https://leetcode.cn/problems/swap-nodes-in-pairs/)

```java
class Solution {
    public ListNode swapPairs(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode newHead = head.next;
        head.next = swapPairs(newHead.next);
        newHead.next = head;
        return newHead;
    }
}
```

### [148. 排序链表](https://leetcode.cn/problems/sort-list/)

```java
class Solution {
    public ListNode sortList(ListNode head) {
        if (head == null || head.next == null)
            return head;
        ListNode fast = head.next, slow = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        ListNode tmp = slow.next;
        slow.next = null;
        ListNode left = sortList(head);
        ListNode right = sortList(tmp);
        ListNode h = new ListNode(0);
        ListNode res = h;
        while (left != null && right != null) {
            if (left.val < right.val) {
                h.next = left;
                left = left.next;
            } else {
                h.next = right;
                right = right.next;
            }
            h = h.next;
        }
        h.next = left != null ? left : right;
        return res.next;
    }
}
```

---

## 二叉树
### [94. 二叉树的中序遍历](https://leetcode.cn/problems/binary-tree-inorder-traversal/)
```java
class Solution {
    public List<Integer> inorderTraversal(TreeNode root) {
        ArrayList<Integer> arrayList = new ArrayList<Integer>();
        inorderTraversal(root,arrayList);
        return arrayList;
    }
    public void inorderTraversal(TreeNode root, List<Integer> res) {
        if (root == null) {
            return;
        }
        inorderTraversal(root.left, res);
        res.add(root.val);
        inorderTraversal(root.right, res);
    }
}
```

### [104. 二叉树的最大深度](https://leetcode.cn/problems/maximum-depth-of-binary-tree/)

```java
class Solution {
    public int maxDepth(TreeNode root) {
        if (root==null) {
            return 0;
        }else{
            int left = maxDepth(root.left);
            int right = maxDepth(root.right);
            return Math.max(left,right)+1;
        }
    }
}
```

### [226. 翻转二叉树](https://leetcode.cn/problems/invert-binary-tree/)

```java
class Solution {
    public TreeNode invertTree(TreeNode root) {
        if (root == null) {
            return null;
        }
        TreeNode lefTreeNode = invertTree(root.left);
        TreeNode rigTreeNode = invertTree(root.right);
        root.left = rigTreeNode;
        root.right = lefTreeNode;
        return root;
    }
}
```

### [101. 对称二叉树](https://leetcode.cn/problems/symmetric-tree/)

```java
class Solution {
    public boolean isSymmetric(TreeNode root) {
        return check(root, root);
    }
    public boolean check(TreeNode p, TreeNode q) {
        if (p == null && q == null) {
            return true;
        }
        if (p == null || q == null) {
            return false;
        }
        return p.val == q.val && check(p.left, q.right) && check(p.right, q.left);
    }
}
```

### [543. 二叉树的直径](https://leetcode.cn/problems/diameter-of-binary-tree/)
```java
class Solution {
    int ans;
    public int diameterOfBinaryTree(TreeNode root) {
        ans = 1;
        depth(root);
        return ans - 1;
    }
    public int depth(TreeNode node) {
        if (node == null) {
            return 0; // 访问到空节点了，返回0
        }
        int L = depth(node.left); // 左儿子为根的子树的深度
        int R = depth(node.right); // 右儿子为根的子树的深度
        ans = Math.max(ans, L+R+1); // 计算d_node即L+R+1 并更新ans
        return Math.max(L, R) + 1; // 返回该节点为根的子树的深度
    }
}
```

### [102. 二叉树的层序遍历](https://leetcode.cn/problems/binary-tree-level-order-traversal/)

```java
public List<List<Integer>> levelOrder(TreeNode root) {
    List<List<Integer>> res = new ArrayList<>();
    Queue<TreeNode> queue = new ArrayDeque<>();
    if (root != null) {
        queue.add(root);
    }
    while (!queue.isEmpty()) {
        int n = queue.size();
        List<Integer> level = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            TreeNode node = queue.poll();
            level.add(node.val);
            if (node.left != null) {
                queue.add(node.left);
            }
            if (node.right != null) {
                queue.add(node.right);
            }
        }
        res.add(level);
    }
    return res;
}
```

### [108. 将有序数组转换为二叉搜索树](https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/)

```java
class Solution {
    public TreeNode sortedArrayToBST(int[] nums) {
        return helper(nums, 0, nums.length - 1);
    }
    public TreeNode helper(int[] nums, int left, int right) {
        if (left > right) {
            return null;
        }
        // 总是选择中间位置左边的数字作为根节点
        int mid = (left + right) / 2;
        TreeNode root = new TreeNode(nums[mid]);
        root.left = helper(nums, left, mid - 1);
        root.right = helper(nums, mid + 1, right);
        return root;
    }
}
```

### [98. 验证二叉搜索树](https://leetcode.cn/problems/validate-binary-search-tree/)

```java
class Solution {
    public boolean isValidBST(TreeNode root) {
        return isValidBST(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }
    public boolean isValidBST(TreeNode node, long lower, long upper) {
        if (node == null) {
            return true;
        }
        if (node.val <= lower || node.val >= upper) {
            return false;
        }
        return isValidBST(node.left, lower, node.val) && isValidBST(node.right, node.val, upper);
    }
}
```

### [230. 二叉搜索树中第 K 小的元素](https://leetcode.cn/problems/kth-smallest-element-in-a-bst/)

```java
class Solution {
    public int kthSmallest(TreeNode root, int k) {
        Deque<TreeNode> stack = new ArrayDeque<TreeNode>();
        while (root != null || !stack.isEmpty()) {
            while (root != null) {
                stack.push(root);
                root = root.left;
            }
            root = stack.pop();
            --k;
            if (k == 0) {
                break;
            }
            root = root.right;
        }
        return root.val;
    }
}
```

### [199. 二叉树的右视图](https://leetcode.cn/problems/binary-tree-right-side-view/)

```java
class Solution {
    public List<Integer> rightSideView(TreeNode root) {
        Map<Integer, Integer> rightmostValueAtDepth = new HashMap<Integer, Integer>();
        int max_depth = -1;
        Queue<TreeNode> nodeQueue = new LinkedList<TreeNode>();
        Queue<Integer> depthQueue = new LinkedList<Integer>();
        nodeQueue.add(root);
        depthQueue.add(0);
        while (!nodeQueue.isEmpty()) {
            TreeNode node = nodeQueue.remove();
            int depth = depthQueue.remove();
            if (node != null) {
                // 维护二叉树的最大深度
                max_depth = Math.max(max_depth, depth);
                // 由于每一层最后一个访问到的节点才是我们要的答案，因此不断更新对应深度的信息即可
                rightmostValueAtDepth.put(depth, node.val);
                nodeQueue.add(node.left);
                nodeQueue.add(node.right);
                depthQueue.add(depth + 1);
                depthQueue.add(depth + 1);
            }
        }
        List<Integer> rightView = new ArrayList<Integer>();
        for (int depth = 0; depth <= max_depth; depth++) {
            rightView.add(rightmostValueAtDepth.get(depth));
        }
        return rightView;
    }
}
```

### [114. 二叉树展开为链表](https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/)

```java
public static void preOrderStack(TreeNode root) {
    if (root == null) return;
    Stack<TreeNode> s = new Stack<TreeNode>();
    while (root != null || !s.isEmpty()) {
        while (root != null) {
            System.out.println(root.val);
            s.push(root);
            root = root.left;
        }
        root = s.pop();
        root = root.right;
    }
}
```

### [105. 从前序与中序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)

```java
class Solution {
    public TreeNode buildTree(int[] preorder, int[] inorder) {
        if (preorder == null || preorder.length == 0)  return null;
        TreeNode root = new TreeNode(preorder[0]);
        Deque<TreeNode> stack = new LinkedList<TreeNode>();
        stack.push(root);
        int inorderIndex = 0;
        for (int i = 1; i < preorder.length; i++) {
            int preorderVal = preorder[i];
            TreeNode node = stack.peek();
            if (node.val != inorder[inorderIndex]) {
                node.left = new TreeNode(preorderVal);
                stack.push(node.left);
            } else {
                while (!stack.isEmpty() && stack.peek().val == inorder[inorderIndex]) {
                    node = stack.pop();
                    inorderIndex++;
                }
                node.right = new TreeNode(preorderVal);
                stack.push(node.right);
            }
        }
        return root;
    }
}
```

### [437. 路径总和 III](https://leetcode.cn/problems/path-sum-iii/)

```java
class Solution {
    public int pathSum(TreeNode root, int targetSum) {
        Map<Long, Integer> prefix = new HashMap<Long, Integer>();
        prefix.put(0L, 1);
        return dfs(root, prefix, 0, targetSum);
    }
    public int dfs(TreeNode root, Map<Long, Integer> prefix, long curr, int targetSum) {
        if (root == null) return 0;
        int ret = 0;
        curr += root.val;
        ret = prefix.getOrDefault(curr - targetSum, 0);
        prefix.put(curr, prefix.getOrDefault(curr, 0) + 1);
        ret += dfs(root.left, prefix, curr, targetSum);
        ret += dfs(root.right, prefix, curr, targetSum);
        prefix.put(curr, prefix.getOrDefault(curr, 0) - 1);
        return ret;
    }
}
```

### [236. 二叉树的最近公共祖先](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/)

```java
class Solution {
    public TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if(root == null || root == p || root == q) return root;
        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);
        if(left == null) return right;
        if(right == null) return left;
        return root;
    }
}
```
