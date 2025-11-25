---
title: Leetcode150. 逆波兰表达式求值
date: 2024-08-24 11:54:37
categories: [Java开发]
tags: ['Java', 'LeetCode', '性能优化']
---
[Leetcode150. 逆波兰表达式求值](https://leetcode.cn/problems/evaluate-reverse-polish-notation/description)

给你一个字符串数组 tokens，表示一个根据 逆波兰表示法 表示的算术表达式。

请你计算该表达式。返回一个表示表达式值的整数。

注意：

> 有效的算符为 '+'、'-'、'*' 和 '/' 。
每个操作数（运算对象）都可以是一个整数或者另一个表达式。
两个整数之间的除法总是 向零截断。
表达式中不含除零运算。
输入是一个根据逆波兰表示法表示的算术表达式。
答案及所有中间计算结果可以用 32 位 整数表示。


#### Java


```java
import java.util.Stack;

class Solution {
    public int evalRPN(String[] tokens) {

        Stack<Integer> opStack = new Stack<>();
        for (int i = 0; i < tokens.length; i++) {

            if (tokens[i].equals("+")) {
                int num2 = opStack.pop();
                int num1 = opStack.pop();
                int num3 = num1 + num2;
                opStack.push(num3);
            }else if (tokens[i].equals("*")) {
                int num2 = opStack.pop();
                int num1 = opStack.pop();
                int num3 = num1 * num2;
                opStack.push(num3);
            }else if (tokens[i].equals("-")) {
                int num2 = opStack.pop();
                int num1 = opStack.pop();
                int num3 = num1 - num2;
                opStack.push(num3);
            }else if (tokens[i].equals("/")) {
                int num2 = opStack.pop();
                int num1 = opStack.pop();
                int num3 = num1 / num2;
                opStack.push(num3);
            }else{
                opStack.push(Integer.valueOf(tokens[i]));
            }

        }
        return opStack.peek();

    }
}
```


#### 优化

1. **简化操作符判断**： `switch` 语句替代多个 `if-else`；
2. **避免重复代码**：将操作符的处理提取到一个函数中。（代码较短，不做处理）
3. **变量声明优化**：在 `switch` 语句中，变量 `num2` 和 `num1` 是重复使用的，考虑在开始时统一声明。

> 箭头函数在jdk11及之后才有

```java
import java.util.Stack;

class Solution {
    public int evalRPN(String[] tokens) {

        Stack<Integer> opStack = new Stack<>();

        for (String token : tokens) {
            switch (token) {
                case "+" -> opStack.push(opStack.pop() + opStack.pop());
                case "-" -> {
                    int num2 = opStack.pop();
                    int num1 = opStack.pop();
                    opStack.push(num1 - num2);
                }
                case "*" -> opStack.push(opStack.pop() * opStack.pop());
                case "/" -> {
                    int num2 = opStack.pop();
                    int num1 = opStack.pop();
                    opStack.push(num1 / num2);
                }
                default -> opStack.push(Integer.valueOf(token));
            }
        }
        return opStack.peek();
    }
}
```

### 为什么 switch 性能优于 switch


1. **字节码优化**：在 `switch` 语句中，如果使用的是整数类型（包括`int`、`byte`、`short`、`char`等），编译器通常会生成 `tableswitch` 或 `lookupswitch` 字节码指令。这些指令在执行时能够快速地定位到正确的分支。例如：  
   * **`tableswitch`**：适用于 case 值连续的情况，通过计算索引直接跳转，性能非常高。  
   * **`lookupswitch`**：适用于 case 值不连续的情况，采用二分查找的方式，性能仍然优于多个 `if-else`。
2. **跳转表**：对于`tableswitch`，JVM 会构建一个跳转表，通过偏移量直接跳转到目标分支。这种方式比逐一比较 `if-else` 快得多。
3. **分支预测**：现代处理器通常有分支预测单元。虽然分支预测适用于`if-else`，但`switch`语句通常可以被处理器更有效地优化，特别是在分支较多的情况下。
4. **可读性和维护性**：虽然这不是直接的性能因素，但更简洁的代码通常更容易被编译器优化。此外，在代码维护时，`switch` 语句也更容易管理和理解，减少了潜在的性能损失。

### 什么时候 `if-else` 更优？

虽然 `switch` 通常更快，但在某些情况下，`if-else` 可能更优：

* **条件非常少**：当只有两个或三个简单的条件时，`if-else` 可能比 `switch` 更直接，开销更小。
* **复杂条件**：如果条件不仅仅是简单的值比较，而是更复杂的表达式，`if-else` 可能更适合。