---
title: 09 HashTable与HashMap
date: 2024-07-22 17:20:16
categories:
  - 数据结构
---
# HashMap:

### 基本概念

HashMap`是Java集合框架中基于哈希表（Hash Table）实现的键值对（Key-Value）存储结构。它允许存储null值和null键，并且不保证元素的顺序。`HashMap`是非线程安全的，如果需要线程安全的操作，可以使用`ConcurrentHashMap`或者通过Collections工具类将其包装为线程安全的版本。  
​  
### 主要特点  
​  
1. **快速访问**：由于基于哈希表实现，`HashMap`能够在O(1)时间复杂度内完成插入和查找操作（在理想情况下）。  
2. **无序存储**：`HashMap`不保证存储顺序，元素的顺序可能在插入时和取出时不同。  
3. **允许null键和null值**：一个`HashMap`实例可以存储一个null键和多个null值。  
​  
### 实现原理

HashMap`的实现依赖于哈希表和链表。每个键值对存储在一个称为`Node`的内部类中，`Node`包含四个属性：键、值、哈希值和下一个节点的引用。当存储元素时，通过键的哈希值确定元素在哈希表中的位置（桶），如果发生哈希冲突，则通过链表或红黑树（在链表长度超过一定阈值时）来解决冲突。

1. **哈希函数**：`HashMap`使用键的`hashCode()`方法生成哈希值，并通过哈希函数将其映射到数组的索引位置。
    
2. **碰撞处理**：当两个键的哈希值映射到同一位置时，`HashMap`使用链表将这些键值对串联起来。在Java 8及以后版本，当链表长度超过一定阈值（默认8）时，会将链表转换为红黑树，以提高查找效率。
    

### 主要方法

以下是`HashMap`中常用的方法及其功能：

1. **put(K key, V value)**：将指定的键值对插入到`HashMap`中。如果键已存在，则更新对应的值。 java 复制代码 `HashMap<String, Integer> map = new HashMap<>(); map.put("one", 1); map.put("two", 2);`
    
2. **get(Object key)**：根据键获取对应的值，如果键不存在则返回null。 java 复制代码 `Integer value = map.get("one"); // 返回1`
    
3. **remove(Object key)**：根据键删除对应的键值对，并返回被删除的值。 java 复制代码 `Integer removedValue = map.remove("one"); // 返回1`
    
4. **containsKey(Object key)**：检查`HashMap`是否包含指定的键。 java 复制代码 `boolean contains = map.containsKey("two"); // 返回true`
    
5. **containsValue(Object value)**：检查`HashMap`是否包含指定的值。 java 复制代码 `boolean contains = map.containsValue(2); // 返回true`
    
6. **size()**：返回`HashMap`中键值对的数量。 java 复制代码 `int size = map.size(); // 返回1`
    
7. **isEmpty()**：检查`HashMap`是否为空。 java 复制代码 `boolean isEmpty = map.isEmpty(); // 返回false`
    
8. **clear()**：清空`HashMap`，移除所有键值对。 java 复制代码 `map.clear();
    

​  
### 示例代码  ​  
`HashMap`的基本使用：  
```
import java.util.HashMap;
import java.util.Map;

public class HashMapExample {
    public static void main(String[] args) {
        // 创建一个HashMap实例
        HashMap<String, Integer> map = new HashMap<>();

        // 添加键值对
        map.put("one", 1);
        map.put("two", 2);
        map.put("three", 3);

        // 获取值
        Integer value = map.get("two");
        System.out.println("Value for key 'two': " + value);

        // 检查是否包含键或值
        boolean hasKey = map.containsKey("three");
        boolean hasValue = map.containsValue(3);
        System.out.println("Contains key 'three': " + hasKey);
        System.out.println("Contains value 3: " + hasValue);

        // 移除键值对
        Integer removedValue = map.remove("one");
        System.out.println("Removed value: " + removedValue);

        // 遍历HashMap
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            System.out.println("Key: " + entry.getKey() + ", Value: " + entry.getValue());
        }

        // 清空HashMap
        map.clear();
        System.out.println("Map is empty: " + map.isEmpty());
    }
}
```

这个示例展示如何创建一个`HashMap`实例、添加键值对、获取值、检查包含关系、移除键值对、遍历`HashMap`以及清空`HashMap`。  
​
​ 
# HashTable :   ​  
### 基本概念

Hashtable`是Java集合框架中的一个类，提供了一种基于哈希表的数据结构，用于存储键值对。`Hashtable`实现了`Map`接口，类似于`HashMap`，但有几个关键区别，最重要的是`Hashtable`是线程安全的，它的所有方法都是同步的。

### 主要特点

1. **线程安全**：`Hashtable`中的所有方法都是同步的，因此它是线程安全的，适合多线程环境。
    
2. **不允许null键和null值**：`Hashtable`不允许存储null键或null值，如果尝试存储，将抛出`NullPointerException`。
    
3. **无序存储**：和`HashMap`一样，`Hashtable`不保证元素的顺序。
    

### 实现原理

Hashtable`的实现依赖于哈希表和链表。每个键值对存储在一个称为`Entry`的内部类中，`Entry`包含四个属性：键、值、哈希值和下一个节点的引用。当存储元素时，通过键的哈希值确定元素在哈希表中的位置（桶），如果发生哈希冲突，则通过链表解决冲突。  
​  
1. **哈希函数**：`Hashtable`使用键的`hashCode()`方法生成哈希值，并通过哈希函数将其映射到数组的索引位置。  
2. **碰撞处理**：当两个键的哈希值映射到同一位置时，`Hashtable`使用链表将这些键值对串联起来。  

​  
### 主要方法  
​  
以下是`Hashtable`中常用的方法及其功能：  
​  
1. **put(K key, V value)**：将指定的键值对插入到`Hashtable`中。如果键已存在，则更新对应的值。    
java    
复制代码    
`Hashtable<String, Integer> table = new Hashtable<>();    
table.put("one", 1);    
table.put("two", 2);    
`  
2. **get(Object key)**：根据键获取对应的值，如果键不存在则返回null。    
java    
复制代码    
`Integer value = table.get("one"); // 返回1    
`  
3. **remove(Object key)**：根据键删除对应的键值对，并返回被删除的值。    
java    
复制代码    
`Integer removedValue = table.remove("one"); // 返回1    
`  
4. **containsKey(Object key)**：检查`Hashtable`是否包含指定的键。    
java    
复制代码    
`boolean contains = table.containsKey("two"); // 返回true    
`  
5. **contains(Object value)**：检查`Hashtable`是否包含指定的值。    
java    
复制代码    
`boolean contains = table.contains(2); // 返回true    
`  
6. **size()**：返回`Hashtable`中键值对的数量。    
java    
复制代码    
`int size = table.size(); // 返回1    
`  
7. **isEmpty()**：检查`Hashtable`是否为空。    
java    
复制代码    
`boolean isEmpty = table.isEmpty(); // 返回false    
`  
8. **clear()**：清空`Hashtable`，移除所有键值对。    
java    
复制代码    
`table.clear();  

### 示例代码

```
import java.util.Hashtable;
import java.util.Map;

public class HashtableExample {
    public static void main(String[] args) {
        // 创建一个Hashtable实例
        Hashtable<String, Integer> table = new Hashtable<>();

        // 添加键值对
        table.put("one", 1);
        table.put("two", 2);
        table.put("three", 3);

        // 获取值
        Integer value = table.get("two");
        System.out.println("Value for key 'two': " + value);

        // 检查是否包含键或值
        boolean hasKey = table.containsKey("three");
        boolean hasValue = table.contains(3);
        System.out.println("Contains key 'three': " + hasKey);
        System.out.println("Contains value 3: " + hasValue);

        // 移除键值对
        Integer removedValue = table.remove("one");
        System.out.println("Removed value: " + removedValue);

        // 遍历Hashtable
        for (Map.Entry<String, Integer> entry : table.entrySet()) {
            System.out.println("Key: " + entry.getKey() + ", Value: " + entry.getValue());
        }

        // 清空Hashtable
        table.clear();
        System.out.println("Table is empty: " + table.isEmpty());
    }
}

```