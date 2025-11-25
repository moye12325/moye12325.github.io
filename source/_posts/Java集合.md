---
title: Java集合
date: 2024-09-20 15:01:20
categories: [数据结构与算法]
tags: ['Java', '数据结构']
---
![](https://qiniu.kanes.top/blog/Java集合.svg)

# Java集合

![Java集合框架](https://qiniu.kanes.top/blog/20241028143343.png)

### 说明
- **Collection** 是所有集合类的顶层接口。
- `List`(对付顺序的好帮手): 存储的元素是有序的、可重复的。**List** 接口下的常用实现有 **ArrayList** 和 **LinkedList**。
- `Set`(注重独一无二的性质): 存储的元素不可重复的。接口下有 **HashSet**、**TreeSet** 和 **LinkedHashSet**。
- `Queue`(实现排队功能的叫号机): 按特定的排队规则来确定先后顺序，存储的元素是有序的、可重复的。 **Queue** 接口常见实现是 **PriorityQueue**。**Deque** 是双端队列，常用实现为 **ArrayDeque**。
- `Map`(用 key 来搜索的专家): 使用键值对（key-value）存储，类似于数学上的函数 y=f(x)，"x" 代表 key，"y" 代表 value，key 是无序的、不可重复的，value 是无序的、可重复的，每个键最多映射到一个值。**Map** 作为键值对集合的顶层接口，其下常用实现有 **HashMap**、**TreeMap** 和 **LinkedHashMap**。

## 概念

### [集合框架底层数据结构总结](https://javaguide.cn/java/collection/java-collection-questions-01.html#%E9%9B%86%E5%90%88%E6%A1%86%E6%9E%B6%E5%BA%95%E5%B1%82%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84%E6%80%BB%E7%BB%93)

#### [List](#list)

- `ArrayList`：`Object[]` 数组。详细可以查看：[ArrayList 源码分析](/java/collection/arraylist-source-code.html)。
- `Vector`：`Object[]` 数组。
- `LinkedList`：双向链表(JDK1.6 之前为循环链表，JDK1.7 取消了循环)。详细可以查看：[LinkedList 源码分析](/java/collection/linkedlist-source-code.html)。

#### [Set](#set)

- `HashSet`(无序，唯一): 基于 `HashMap` 实现的，底层采用 `HashMap` 来保存元素。
- `LinkedHashSet`: `LinkedHashSet` 是 `HashSet` 的子类，并且其内部是通过 `LinkedHashMap` 来实现的。
- `TreeSet`(有序，唯一): 红黑树(自平衡的排序二叉树)。

#### [Queue](#queue)

- `PriorityQueue`: `Object[]` 数组来实现小顶堆。详细可以查看：[PriorityQueue 源码分析](/java/collection/priorityqueue-source-code.html)。
- `DelayQueue`:`PriorityQueue`。详细可以查看：[DelayQueue 源码分析](/java/collection/delayqueue-source-code.html)。
- `ArrayDeque`: 可扩容动态双向数组。

#### [Map](#map)

- `HashMap`：JDK1.8 之前 `HashMap` 由数组+链表组成的，数组是 `HashMap` 的主体，链表则是主要为了解决哈希冲突而存在的（“拉链法”解决冲突）。JDK1.8 以后在解决哈希冲突时有了较大的变化，当链表长度大于阈值（默认为 8）（将链表转换成红黑树前会判断，如果当前数组的长度小于 64，那么会选择先进行数组扩容，而不是转换为红黑树）时，将链表转化为红黑树，以减少搜索时间。详细可以查看：[HashMap 源码分析](/java/collection/hashmap-source-code.html)。
- `LinkedHashMap`：`LinkedHashMap` 继承自 `HashMap`，所以它的底层仍然是基于拉链式散列结构即由数组和链表或红黑树组成。另外，`LinkedHashMap` 在上面结构的基础上，增加了一条双向链表，使得上面的结构可以保持键值对的插入顺序。同时通过对链表进行相应的操作，实现了访问顺序相关逻辑。详细可以查看：[LinkedHashMap 源码分析](/java/collection/linkedhashmap-source-code.html)
- `Hashtable`：数组+链表组成的，数组是 `Hashtable` 的主体，链表则是主要为了解决哈希冲突而存在的。
- `TreeMap`：红黑树（自平衡的排序二叉树）。

### 集合的选用

- 需要根据键值获取到元素值时就选用 `Map` 接口下的集合，需要排序时选择 `TreeMap`,不需要排序时就选择 `HashMap`,需要保证线程安全就选用 `ConcurrentHashMap`。
- 只需要存放元素值时，就选择实现`Collection` 接口的集合，需要保证元素唯一时选择实现 `Set` 接口的集合比如 `TreeSet` 或 `HashSet`，不需要就选择实现 `List` 接口的比如 `ArrayList` 或 `LinkedList`，然后再根据实现这些接口的集合的特点来选用。


### 数组和集合的区别

- 数组是固定长度的数据结构，一旦创建长度就无法改变；
  集合是动态长度的数据结构，动态增删；
  数组可以直接访问元素，集合需要迭代访问。

- 常见的Java集合类：ArrayList、LinkedList、HashMap、HashSet、Tree Map（基于红黑树的有序Map集合）、LinkedHashMap（基于哈希表和双向链表）、PriorityQueue（优先队列）

### Java中线程安全的集合

- Vector

  - 线程安全的动态数组，内部方法经过Synchronized修饰。线程同步有开销

- Hashtable

  - 线程安全的哈希表，有Synchronized修饰，不支持null键值，很少使用，常用ConcurrentHashMap

### Collections和Collection的区别

- Collection是一个接口，所有集合类的接口，定义了通用的方法，如添加、删除、遍历等

- Collections是一个工具类，用于对集合进行操作，排序、查找、替换、反转等

## List

### [ArrayList 和 Array](#arraylist-和-array-数组-的区别)

`ArrayList` 内部基于动态数组实现，比 `Array`（静态数组） 使用起来更加灵活：

- `ArrayList`会根据实际存储的元素动态地扩容或缩容，而 `Array` 被创建之后就不能改变它的长度了。
- `ArrayList` 允许你使用泛型来确保类型安全，`Array` 则不可以。
- `ArrayList` 中只能存储对象。对于基本类型数据，需要使用其对应的包装类（如 Integer、Double 等）。`Array` 可以直接存储基本类型数据，也可以存储对象。
- `ArrayList` 支持插入、删除、遍历等常见操作，并且提供了丰富的 API 操作方法，比如 `add()`、`remove()`等。`Array` 只是一个固定长度的数组，只能按照下标访问其中的元素，不具备动态添加、删除元素的能力。
- `ArrayList`创建时不需要指定大小，而`Array`创建时必须指定大小。

### [ArrayList 和 Vector](#arraylist-和-vector-的区别-了解即可)

- `ArrayList` 是 `List` 的主要实现类，底层使用 `Object[]`存储，适用于频繁的查找工作，线程不安全 。
- `Vector` 是 `List` 的古老实现类，底层使用`Object[]` 存储，线程安全。

### [Vector 和 Stack](#vector-和-stack-的区别-了解即可)

- `Vector` 和 `Stack` 两者都是线程安全的，都是使用 `synchronized` 关键字进行同步处理。
- `Stack` 继承自 `Vector`，是一个后进先出的栈，而 `Vector` 是一个列表。

随着 Java 并发编程的发展，`Vector` 和 `Stack` 已经被淘汰，推荐使用并发集合类（例如 `ConcurrentHashMap`、`CopyOnWriteArrayList` 等）或者手动实现线程安全的方法来提供安全的多线程操作支持。

### [ArrayList 可以添加 null 值吗？](#arraylist-可以添加-null-值吗)

`ArrayList` 中可以存储任何类型的对象，包括 `null` 值。不过，不建议向`ArrayList` 中添加 `null` 值， `null` 值无意义，会让代码难以维护比如忘记做判空处理就会导致空指针异常。

### [ArrayList 插入和删除元素的时间复杂度？](https://javaguide.cn/java/collection/java-collection-questions-01.html#arraylist-%E6%8F%92%E5%85%A5%E5%92%8C%E5%88%A0%E9%99%A4%E5%85%83%E7%B4%A0%E7%9A%84%E6%97%B6%E9%97%B4%E5%A4%8D%E6%9D%82%E5%BA%A6)

对于插入：

- 头部插入：由于需要将所有元素都依次向后移动一个位置，因此时间复杂度是 O(n)。
- 尾部插入：当 `ArrayList` 的容量未达到极限时，往列表末尾插入元素的时间复杂度是 O(1)，因为它只需要在数组末尾添加一个元素即可；当容量已达到极限并且需要扩容时，则需要执行一次 O(n) 的操作将原数组复制到新的更大的数组中，然后再执行 O(1) 的操作添加元素。
- 指定位置插入：需要将目标位置之后的所有元素都向后移动一个位置，然后再把新元素放入指定位置。这个过程需要移动平均 n/2 个元素，因此时间复杂度为 O(n)。

对于删除：

- 头部删除：由于需要将所有元素依次向前移动一个位置，因此时间复杂度是 O(n)。
- 尾部删除：当删除的元素位于列表末尾时，时间复杂度为 O(1)。
- 指定位置删除：需要将目标元素之后的所有元素向前移动一个位置以填补被删除的空白位置，因此需要移动平均 n/2 个元素，时间复杂度为 O(n)。

### [LinkedList 插入和删除元素的时间复杂度？](#linkedlist-插入和删除元素的时间复杂度)

- 头部插入/删除：只需要修改头结点的指针即可完成插入/删除操作，因此时间复杂度为 O(1)。
- 尾部插入/删除：只需要修改尾结点的指针即可完成插入/删除操作，因此时间复杂度为 O(1)。
- 指定位置插入/删除：需要先移动到指定位置，再修改指定节点的指针完成插入/删除，不过由于有头尾指针，可以从较近的指针出发，因此需要遍历平均 n/4 个元素，时间复杂度为 O(n)。

### [LinkedList 为什么不能实现 RandomAccess 接口？](#linkedlist-为什么不能实现-randomaccess-接口)

`RandomAccess` 是一个标记接口，用来表明实现该接口的类支持随机访问（即可以通过索引快速访问元素）。由于 `LinkedList` 底层数据结构是链表，内存地址不连续，只能通过指针来定位，不支持随机快速访问，所以不能实现 `RandomAccess` 接口。


## Set

### 集合特点

- 元素唯一，不会重复

### 实现原理

- 数据结构：哈希表、红黑树等，实现key不重复

当插入元素时，根据元素的hashCode计算元素存储位置，再通过equals判断是否存在相同的元素，存在则不插入

### 有序的Set，插入顺序的集合

- 有序的Set是TreeSet和LinkedHashSet。前者基于红黑树，保证元素的自然顺序；后者基于双重链表和哈希表，保证元素顺序

- 记录插入顺序的集合通常指LinkedHashSet，保证元素唯一，保持元素插入的顺序

### [Comparable 和 Comparator 的区别](https://javaguide.cn/java/collection/java-collection-questions-01.html#comparable-%E5%92%8C-comparator-%E7%9A%84%E5%8C%BA%E5%88%AB)

### [无序性和不可重复性的含义是什么](#无序性和不可重复性的含义是什么)

- 无序性不等于随机性 ，无序性是指**存储的数据**在底层数组中并非按照数组索引的顺序添加 ，而是**根据数据的哈希值决定**的。
- 不可重复性是指添加的元素按照 `equals()` 判断时 ，返回 false，需要同时重写 `equals()` 方法和 `hashCode()` 方法。

### [比较 HashSet、LinkedHashSet 和 TreeSet 三者的异同](#比较-hashset、linkedhashset-和-treeset-三者的异同)

- `HashSet`、`LinkedHashSet` 和 `TreeSet` 都是 `Set` 接口的实现类，都能保证元素唯一，并且都**不是线程安全**的。
- `HashSet`、`LinkedHashSet` 和 `TreeSet` 的主要区别在于底层数据结构不同。**`HashSet` 的底层数据结构是哈希表**（基于 `HashMap` 实现）。**`LinkedHashSet` 的底层数据结构是链表和哈希表**，元素的插入和取出顺序满足 FIFO。`**TreeSet` 底层数据结构是红黑树，元素是有序**的，排序的方式有自然排序和定制排序。
- 底层数据结构不同又导致这三者的应用场景不同。**`HashSet` 用于不需要保证元素插入和取出顺序的场景**，**`LinkedHashSet` 用于保证元素的插入和取出顺序满足 FIFO 的场景**，**`TreeSet` 用于支持对元素自定义排序规则的场景**。

## Queue

### Queue 与 Deque

`Queue` 是单端队列，只能从一端插入元素，另一端删除元素，实现上一般遵循 **先进先出（FIFO）** 规则。

`Queue` 扩展了 `Collection` 的接口，根据 **因为容量问题而导致操作失败后处理方式的不同** 可以分为两类方法: 一种在操作失败后会抛出异常，另一种则会返回特殊值。

|`Queue` 接口|抛出异常|返回特殊值|
|---|---|---|
|插入队尾|add(E e)|offer(E e)|
|删除队首|remove()|poll()|
|查询队首元素|element()|peek()|

`Deque` 是**双端**队列，在队列的两端均可以插入或删除元素。

`Deque` **扩展**了 `Queue` 的接口, **增加了在队首和队尾进行插入和删除**的方法，同样根据失败后处理方式的不同分为两类：

|`Deque` 接口|抛出异常|返回特殊值|
|---|---|---|
|插入队首|addFirst(E e)|offerFirst(E e)|
|插入队尾|addLast(E e)|offerLast(E e)|
|删除队首|removeFirst()|pollFirst()|
|删除队尾|removeLast()|pollLast()|
|查询队首元素|getFirst()|peekFirst()|
|查询队尾元素|getLast()|peekLast()|

事实上，`Deque` 还提供有 `push()` 和 `pop()` 等其他方法，可用于模拟栈。

### ArrayDeque 与 LinkedList

`ArrayDeque` 和 `LinkedList` 都实现了 `Deque` 接口，两者都具有队列的功能，但两者有什么区别呢？

- `ArrayDeque` 是基于可变长的数组和双指针来实现，而 `LinkedList` 则通过链表来实现。
- `ArrayDeque` 不支持存储 `NULL` 数据，但 `LinkedList` 支持。
- `ArrayDeque` 是在 JDK1.6 才被引入的，而`LinkedList` 早在 JDK1.2 时就已经存在。
- `ArrayDeque` 插入时可能存在扩容过程, 不过均摊后的插入操作依然为 O(1)。虽然 `LinkedList` 不需要扩容，但是每次插入数据时均需要申请新的堆空间，均摊性能相比更慢。

从性能的角度上，选用 `ArrayDeque` 来实现队列要比 `LinkedList` 更好。此外，`ArrayDeque` 也可以用于实现栈。

### [PriorityQueue](https://javaguide.cn/java/collection/java-collection-questions-01.html#%E8%AF%B4%E4%B8%80%E8%AF%B4-priorityqueue)

`PriorityQueue` 是在 JDK1.5 中被引入的, 其与 `Queue` 的区别在于元素出队顺序是与优先级相关的，即总是优先级最高的元素先出队。

- `PriorityQueue` 利用了二叉堆的数据结构来实现的，底层使用可变长的数组来存储数据
- `PriorityQueue` 通过堆元素的上浮和下沉，实现了在 O(logn) 的时间复杂度内插入元素和删除堆顶元素。
- `PriorityQueue` 是非线程安全的，且不支持存储 `NULL` 和 `non-comparable` 的对象。
- `PriorityQueue` 默认是小顶堆，但可以接收一个 `Comparator` 作为构造参数，从而来自定义元素优先级的先后。

`PriorityQueue` 在面试中可能更多的会出现在手撕算法的时候，典型例题包括堆排序、求第 K 大的数、带权图的遍历等，所以需要会熟练使用才行。

### [什么是 BlockingQueue？](https://javaguide.cn/java/collection/java-collection-questions-01.html#%E4%BB%80%E4%B9%88%E6%98%AF-blockingqueue)

### [ArrayBlockingQueue 和 LinkedBlockingQueue](https://javaguide.cn/java/collection/java-collection-questions-01.html#arrayblockingqueue-%E5%92%8C-linkedblockingqueue-%E6%9C%89%E4%BB%80%E4%B9%88%E5%8C%BA%E5%88%AB)

## Map

### [HashMap 和 Hashtable 的区别](https://javaguide.cn/java/collection/java-collection-questions-02.html#hashmap-%E5%92%8C-hashtable-%E7%9A%84%E5%8C%BA%E5%88%AB)

- **线程是否安全：** `HashMap` 是非线程安全的，`Hashtable` 是线程安全的,因为 `Hashtable` 内部的方法基本都经过`synchronized` 修饰。（如果你要保证线程安全的话就使用 `ConcurrentHashMap` 吧！）；

- **效率：** 因为线程安全的问题，`HashMap` 要比 `Hashtable` 效率高一点。另外，`Hashtable` 基本被淘汰，不要在代码中使用它；
- **对 Null key 和 Null value 的支持：** `HashMap` 可以存储 null 的 key 和 value，但 null 作为键只能有一个，null 作为值可以有多个；Hashtable 不允许有 null 键和 null 值，否则会抛出
- **初始容量大小和每次扩充容量大小的不同：** 
	- ① 创建时如果不指定容量初始值，`Hashtable` 默认的初始大小为 11，之后每次扩充，容量变为原来的 2n+1。`HashMap` 默认的初始化大小为 16。之后每次扩充，容量变为原来的 2 倍。  
	- ② 创建时如果给定了容量初始值，那么 `Hashtable` 会直接使用你给定的大小，而 `HashMap` 会将其扩充为 2 的幂次方大小（`HashMap` 中的`tableSizeFor()`方法保证。也就是说 `HashMap` 总是使用 2 的幂作为哈希表的大小,后面会介绍到为什么是 2 的幂次方。
- **底层数据结构：** JDK1.8 以后的 `HashMap` 在解决哈希冲突时，当链表长度大于阈值（默认为 8）时，将链表转化为红黑树（将链表转换成红黑树前会判断，如果当前数组的长度小于 64，那么会选择先进行数组扩容，而不是转换为红黑树），以减少搜索时间。`Hashtable` 没有这样的机制。
- **哈希函数的实现**：`HashMap` 对哈希值进行了高位和低位的混合扰动处理以减少冲突，而 `Hashtable` 直接使用键的 `hashCode()` 值。

### HashMap 和 HashSet 区别

`HashSet` 底层就是基于 `HashMap` 实现的。（`HashSet` 的源码非常非常少，因为除了 `clone()`、`writeObject()`、`readObject()`是 `HashSet` 自己不得不实现之外，其他方法都是直接调用 `HashMap` 中的方法。

|`HashMap`|`HashSet`|
|---|---|
|实现了 `Map` 接口|实现 `Set` 接口|
|存储键值对|仅存储对象|
|调用 `put()`向 map 中添加元素|调用 `add()`方法向 `Set` 中添加元素|
|`HashMap` 使用键（Key）计算 `hashcode`|`HashSet` 使用成员对象来计算 `hashcode` 值，对于两个对象来说 `hashcode` 可能相同，所以`equals()`方法用来判断对象的相等性|

### [HashMap和TreeMap](https://javaguide.cn/java/collection/java-collection-questions-02.html#hashmap-%E5%92%8C-treemap-%E5%8C%BA%E5%88%AB)
`TreeMap` 和`HashMap` 都继承自`AbstractMap` ，但是需要注意的是`TreeMap`它还实现了`NavigableMap`接口和`SortedMap` 接口。

实现 `NavigableMap` 接口让 `TreeMap` 有了对集合内元素的搜索的能力。

`NavigableMap` 接口：

- **定向搜索**: `ceilingEntry()`, `floorEntry()`, `higherEntry()`和 `lowerEntry()` 等方法可以用于定位大于等于、小于等于、严格大于、严格小于给定键的最接近的键值对。
- **子集操作**: `subMap()`, `headMap()`和 `tailMap()` 方法可以高效地创建原集合的子集视图，而无需复制整个集合。
- **逆序视图**:`descendingMap()` 方法返回一个逆序的 `NavigableMap` 视图，使得可以反向迭代整个 `TreeMap`。
- **边界操作**: `firstEntry()`, `lastEntry()`, `pollFirstEntry()`和 `pollLastEntry()` 等方法可以方便地访问和移除元素。

这些方法都是基于红黑树数据结构的属性实现的，红黑树保持平衡状态，从而保证了搜索操作的时间复杂度为 O(log n)，这让 `TreeMap` 成为了处理有序集合搜索问题的强大工具。

实现`SortedMap`接口让 `TreeMap` 有了对集合中的元素根据键排序的能力。默认是按 key 的升序排序，不过我们也可以指定排序的比较器。

### [HashSet 如何检查重复?](https://javaguide.cn/java/collection/java-collection-questions-02.html#hashset-%E5%A6%82%E4%BD%95%E6%A3%80%E6%9F%A5%E9%87%8D%E5%A4%8D)

> `HashSet` 会先计算对象的`hashcode`值来判断对象加入的位置，同时也会与其他加入的对象的 `hashcode` 值作比较，如果没有相符的 `hashcode`，`HashSet` 会假设对象没有重复出现。但是如果发现有相同 `hashcode` 值的对象，这时会调用`equals()`方法来检查 `hashcode` 相等的对象是否真的相同。如果两者相同，`HashSet` 就不会让加入操作成功。

### HashMap原理

- jdk1.7之前，使用数组、链表。通过 key 的 `hashcode` 经过扰动函数处理过后得到 hash 值，然后通过 `(n - 1) & hash` 判断当前元素存放的位置（这里的 n 指的是数组的长度），如果当前位置存在元素的话，就判断该元素与要存入的元素的 hash 值以及 key 是否相同，如果相同的话，直接覆盖，不相同就通过拉链法解决冲突。

- 1.8时，当链表长度大于阈值（默认为 8）（将链表转换成红黑树前会判断，如果当前数组的长度小于 64，那么会选择先进行数组扩容，而不是转换为红黑树）时，将链表转化为红黑树，以减少搜索时间。

### 解决哈希冲突的方法

- 链接法：使用链表或其他ds存储冲突的键值对，链接到同一个桶中

- 开放寻址法：找另一个可用的位置存放冲突的键值对

- 再次哈希：使用另一个哈希函数，直到找到一个空槽位

- 哈希桶扩容：动态扩大哈希桶的容量，重新分配键值对


### [HashMap 多线程操作导致死循环](https://javaguide.cn/java/collection/java-collection-questions-02.html#hashmap-%E5%A4%9A%E7%BA%BF%E7%A8%8B%E6%93%8D%E4%BD%9C%E5%AF%BC%E8%87%B4%E6%AD%BB%E5%BE%AA%E7%8E%AF%E9%97%AE%E9%A2%98)

1.7及之前，当一个桶位中有多个元素需要进行扩容时，多个线程同时对链表进行操作，头插法可能会导致链表中的节点指向错误的位置，从而形成一个环形链表，进而使得查询元素的操作陷入死循环无法结束。

1.8 版本的 HashMap 采用了尾插法而不是头插法来避免链表倒置，使得插入的节点永远都是放在链表的末尾，避免了链表中的环形结构。并发环境下，推荐使用 `ConcurrentHashMap` 。

> - 两个线程 1,2 同时进行 put 操作，并且发生了哈希冲突（hash 函数计算出的插入下标是相同的）。
> - 不同的线程可能在不同的时间片获得 CPU 执行的机会，当前线程 1 执行完哈希冲突判断后，由于时间片耗尽挂起。线程 2 先完成了插入操作。
> - 随后，线程 1 获得时间片，由于之前已经进行过 hash 碰撞的判断，所有此时会直接进行插入，这就导致线程 2 插入的数据被线程 1 覆盖了。

### [HashMap 常见的遍历方式?](https://javaguide.cn/java/collection/java-collection-questions-02.html#hashmap-%E5%B8%B8%E8%A7%81%E7%9A%84%E9%81%8D%E5%8E%86%E6%96%B9%E5%BC%8F)
1. 使用迭代器（Iterator）EntrySet 的方式进行遍历；
```java
// 遍历  
Iterator<Map.Entry<Integer, String>> iterator = map.entrySet().iterator();  
while (iterator.hasNext()) {  
	Map.Entry<Integer, String> entry = iterator.next();  
	System.out.println(entry.getKey());  
	System.out.println(entry.getValue());  
}
```
2. 使用迭代器（Iterator）KeySet 的方式进行遍历；
```java
Iterator<Integer> iterator = map.keySet().iterator();  
while (iterator.hasNext()) {  
	Integer key = iterator.next();  
	System.out.println(key);  
	System.out.println(map.get(key));  
}
```
3. 使用 For Each EntrySet 的方式进行遍历；
```java
for (Map.Entry<Integer, String> entry : map.entrySet()) {  
	System.out.println(entry.getKey());  
	System.out.println(entry.getValue());  
}
```
4. 使用 For Each KeySet 的方式进行遍历；
```java
for (Map.Entry<Integer, String> entry : map.keySet()) {  
	System.out.println(entry.getKey());  
	System.out.println(entry.getValue());  
}
```
5. 使用 Lambda 表达式的方式进行遍历；
```java
map.forEach((key, value) -> {  
	System.out.println(key);  
	System.out.println(value);  
});
```
6. 使用 Streams API 单线程的方式进行遍历；
```java
map.entrySet().stream().forEach((entry) -> {  
	System.out.println(entry.getKey());  
	System.out.println(entry.getValue());  
});
```
7. 使用 Streams API 多线程的方式进行遍历。
```java
map.entrySet().parallelStream().forEach((entry) -> {  
	System.out.println(entry.getKey());  
	System.out.println(entry.getValue());  
});
```

### [ConcurrentHashMap 和 Hashtable](https://javaguide.cn/java/collection/java-collection-questions-02.html#concurrenthashmap-%E5%92%8C-hashtable-%E7%9A%84%E5%8C%BA%E5%88%AB)

> 主要体现在实现线程安全的方式上不同。`Hashtable` 已经逐渐被淘汰

`ConcurrentHashMap` 和 `Hashtable` 都是 Java 中的线程安全的 Map 实现类，但它们在性能和实现细节上有较大差异。

#### 1. **锁的机制**
   - **Hashtable**: 使用的是“全表锁”机制，也就是说，对 `Hashtable` 的任何读写操作都会锁定整个表，导致所有线程都需要依次访问，无法进行并发操作，性能较低。
   - **ConcurrentHashMap**: 使用“分段锁”机制，在 Java 8 之前，`ConcurrentHashMap` 将数据分成多个段（segment），每个段有一个锁，只锁定当前访问的段，因此可以实现更高的并发性。在 Java 8 及以后版本中，`ConcurrentHashMap` 用 CAS（Compare-And-Swap）和 `synchronized` 配合实现更细粒度的并发控制，进一步提升了并发性能。

#### 2. **并发性能**
   - **Hashtable**: 由于全表锁限制了并发访问，性能在多线程环境下较差。
   - **ConcurrentHashMap**: 提供了更高的并发性能，可以支持多线程同时进行读写操作，非常适合高并发场景。

#### 3. **空值处理**
   - **Hashtable**: 不允许键或值为 `null`，否则会抛出 `NullPointerException`。
   - **ConcurrentHashMap**: 也不允许键或值为 `null`，主要是为了避免在多线程环境中引起歧义（例如，无法判断 `get(key)` 返回 `null` 是键不存在还是值为 `null`）。

### [ConcurrentHashMap 为什么 key 和 value 不能为 null？](https://javaguide.cn/java/collection/java-collection-questions-02.html#concurrenthashmap-%E4%B8%BA%E4%BB%80%E4%B9%88-key-%E5%92%8C-value-%E4%B8%8D%E8%83%BD%E4%B8%BA-null)

> 主要是为了避免二义性。

null 是一个特殊的值，表示没有对象或没有引用。如果你用 null 作为键，那么你就无法区分这个键是否存在于 `ConcurrentHashMap` 中，还是根本没有这个键。同样，如果你用 null 作为值，那么你就无法区分这个值是否是真正存储在 `ConcurrentHashMap` 中的，还是因为找不到对应的键而返回的。

### [ConcurrentHashMap 能保证复合操作的原子性吗？](https://javaguide.cn/java/collection/java-collection-questions-02.html#concurrenthashmap-%E8%83%BD%E4%BF%9D%E8%AF%81%E5%A4%8D%E5%90%88%E6%93%8D%E4%BD%9C%E7%9A%84%E5%8E%9F%E5%AD%90%E6%80%A7%E5%90%97)

复合操作是指由多个基本操作(如`put`、`get`、`remove`、`containsKey`等)组成的操作，例如先判断某个键是否存在`containsKey(key)`，然后根据结果进行插入或更新`put(key, value)`。这种操作在执行过程中可能会被其他线程打断，导致结果不符合预期。

`ConcurrentHashMap` 提供了一些原子性的复合操作，如 `putIfAbsent`、`compute`、`computeIfAbsent` 、`computeIfPresent`、`merge`等。这些方法都可以接受一个函数作为参数，根据给定的 key 和 value 来计算一个新的 value，并且将其更新到 map 中。