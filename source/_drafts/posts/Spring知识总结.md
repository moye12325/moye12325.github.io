---
date: 2024-09-26T03:41:55.630Z
updated: 2024-10-29T14:49:27.094Z
title: Spring知识总结
slug: understanding-spring-framework
oid: 66f4d803c10f2bbf499584c6
categories: Java
type: post
permalink: /posts/Java/understanding-spring-framework
---


# Spring

## Spring


Spring 是一款开源的轻量级 Java 开发框架，旨在提高开发人员的开发效率以及系统的可维护性。

一般说 Spring 框架指的都是 Spring Framework，是很多模块的集合，使用这些模块可以协助开发，比如说 Spring 支持 IoC（Inversion of Control:控制反转） 和 AOP(Aspect-Oriented Programming:面向切面编程)、可以很方便地对数据库进行访问、可以很方便地集成第三方组件（电子邮件，任务，调度，缓存等等）、对单元测试支持比较好、支持 RESTful Java 应用程序的开发。

### [Spring,Spring MVC,Spring Boot 之间什么关系?](https://javaguide.cn/system-design/framework/spring/spring-knowledge-and-questions-summary.html#spring-spring-mvc-spring-boot-%E4%B9%8B%E9%97%B4%E4%BB%80%E4%B9%88%E5%85%B3%E7%B3%BB)

Spring 包含了多个功能模块，其中最重要的是 Spring-Core（主要提供 IoC 依赖注入功能的支持） 模块， Spring 中的其他模块（比如 Spring MVC）的功能实现基本都需要依赖于该模块。

Spring MVC 是 Spring 中的一个很重要的模块，主要赋予 Spring 快速构建 MVC 架构的 Web 程序的能力。MVC 是模型(Model)、视图(View)、控制器(Controller)的简写，其核心思想是通过将业务逻辑、数据、显示分离来组织代码。

Spring Boot 只是简化配置，如果需要构建 MVC 架构的 Web 程序，还是需要使用 Spring MVC 作为 MVC 框架，只是说 Spring Boot 帮你简化了 Spring MVC 的很多配置，真正做到开箱即用！

### 对Spring的理解

- 四大核心特性

  - IoC容器

    - Spring通过控制反转实现了对象的创建和对象间的依赖关系管理。只需要定义好Bean及其依赖关系，Spring容器负责创建和组装这些对象

  - AOP

    - 面向切面编程，允许开发者定义横切关注点，例如事务管理、安全控制等，独立于业务代码。通过AOP可以将关注点模块化，提高代码的可维护性和可重用性

  - 事务管理

    - Spring提供了一致的事务管理接口，支持声明式和编程式业务。开发者可以轻松进行事务管理，而无需关心具体的事务API

  - MVC框架

    - SpringMVC基于Servlet API构建的web框架，MVC架构，支持灵活的URL到页面控制器的映射，以及多种视图技术

### IoC和AOP

- IoC控制反转

  - 一种创建和获取对象的技术思想，依赖注入DI是实现这种技术的一种方式。

传统方式需要new对象。IoC通过容器来帮我们实例化对象，可以降低耦合度

- AOP面向切面编程

  - 将与业务无关、却同为业务模块所调用的逻辑封装起来，减少系统的重复代码，降低模块之间的耦合。

AOP基于动态代理，代理的对象实现了某个接口，AOP则会使用jdk proxy去创建代理对象，而对于没有实现接口的对象，则无法使用jdk proxy，此时AOP使用cglib生成被代理对象的子类作为代理

- 结合使用

  - IOC容器管理对象的依赖关系，AOP将横切关注点统一切入到需要的业务逻辑中。

  - IoC容器管理service层和DAO层的依赖关系，AOP在Service层实现事务管理、日志记录等横切功能，使业务逻辑更加清晰和可维护

### AOP

AOP(Aspect-Oriented Programming:面向切面编程)能够将那些与业务无关，却为业务模块所共同调用的逻辑或责任（例如事务处理、日志管理、权限控制等）封装起来，便于减少系统的重复代码，降低模块间的耦合度，并有利于未来的可拓展性和可维护性。

Spring AOP 就是基于动态代理的，如果要代理的对象，实现了某个接口，那么 Spring AOP 会使用 **JDK Proxy**，去创建代理对象，而对于没有实现接口的对象，就无法使用 JDK Proxy 去进行代理了，这时候 Spring AOP 会使用 **Cglib** 生成一个被代理对象的子类来作为代理

- 将与业务无关的、却未业务模块所共同调用的逻辑或责任（例如事务管理、日志管理、权限控制等）封装起来，便于减少代码、降低耦合

- 概念
  - AspectJ切面
    - 一个概念，使Join Point、Advice、Pointcut的统称
  - Join Point
    - 连接点，程序执行过程中的一个点，例如方法调用、异常处理等

  - Advice

    - 通知，切面的横切逻辑。around、before、after三种类型。通常作为拦截器

  - Pointcut

    - 切点。用于匹配连接点，一个AspectJ中包含哪些Join point需要有Pointcut进行筛选

  - Introduction

    - 引介，让一个切面可以声明被通知的对象实现任何他们没有真正实现的额外接口。例如让一个代理对象代理两个目标类

  - Weaving

    - 织入，在切点的引导下，将通知逻辑插入到目标方法上，使得我们的通知逻辑在方法调用时执行

  - AOP proxy

    - AOP实现框架中实现切面协议的对象。jdk动态代理、cglib动态代理

  - target object

    - 目标对象，被代理的对象

### IoC和AOP通过什么机制实现

- IOC实现机制

  - 反射

    - IOC容器动态利用Java的反射机制动态的加载类、创建对象实例及调用对象的方法，反射允许在运行时检查类、方法、属性等信息，从而实现灵活的对象实例化管理

  - 依赖注入

    - IoC核心概念是依赖注入，即容器负责管理应用程序组件之间的关系。spring通过构造函数注入、属性注入、方法注入，将组件之前的依赖关系描述在配置文件中或者使用注解

  - 设计模式-工厂模式

    - IoC容器采用工厂模式来管理对象的创建和生命周期。容器作为工厂负责实例化Bean并管理他们的生命周期，将Bean的实例化过程交给容器管理

  - 容器实现

    - 使用BeanFactory或者ApplicationContext管理Bean。BeanFactory是IoC容器的基本形式，提供基本的IoC功能

- AOP实现机制

  - 基于JDK的动态代理

    - 使用java.lang.reflect.Proxy和InvocationHandler接口实现。这种方式需要代理的类实现一个或多个接口

  - 基于GCLIB的动态代理

    - 当被代理的类没有实现接口时，Spring回使用CGLIB库生成一个被代理类的子类作为代理

  - 运行时动态生成代理对象，而不是在编译时。允许开发者在运行时指定要代理的接口和行为，从而实现不修改源码、增强方法的功能

### 如何理解IoC

- Inversion of Control。控制反转，一种思想。

  - 对象的创建、初始化、销毁。
    创建：原本new，现在由spring创建
    初始化：对象自己通过构造器或者setter方法给依赖的对象复制，现在又spring容器自动注入
    销毁对象：直接给对象复制null或者做销毁操作，现在又容器负责销毁

  - 反转，反转控制权，对象脱离程序员的控制，交给Spring

### 依赖倒置、依赖注入、控制反转

- 控制反转

  - 对程序执行流程的控制，控制权反转给框架

- 依赖注入

  - IoC实现的一种方式。不再new，而是将依赖的类对象再外部创建好之后通过构造函数、函数参数等方式传递给类使用

- 依赖倒置

  - 类似控制反转，用于指导框架层面的设计。高层模块不依赖低层，共同依赖同一个抽象。抽象不依赖具体实现细节，具体细节依赖抽象

    - 高层模块（业务逻辑）不应该依赖低层模块（具体实现）。二者都应该依赖于抽象（接口或抽象类）。

    - 抽象不应该依赖于具体实现，具体实现应该依赖于抽象。

### [Spring AOP 和 AspectJ AOP 有什么区别？](https://javaguide.cn/system-design/framework/spring/spring-knowledge-and-questions-summary.html#spring-aop-%E5%92%8C-aspectj-aop-%E6%9C%89%E4%BB%80%E4%B9%88%E5%8C%BA%E5%88%AB)

**Spring AOP 属于运行时增强，而 AspectJ 是编译时增强。** Spring AOP 基于代理(Proxying)，而 AspectJ 基于字节码操作(Bytecode Manipulation)。

Spring AOP 已经集成了 AspectJ ，AspectJ 应该算的上是 Java 生态系统中最完整的 AOP 框架了。AspectJ 相比于 Spring AOP 功能更加强大，但是 Spring AOP 相对来说更简单，

如果我们的切面比较少，那么两者性能差异不大。但是，当切面太多的话，最好选择 AspectJ ，它比 Spring AOP 快很多。

### [AOP 常见的通知类型有哪些？](https://javaguide.cn/system-design/framework/spring/spring-knowledge-and-questions-summary.html#aop-%E5%B8%B8%E8%A7%81%E7%9A%84%E9%80%9A%E7%9F%A5%E7%B1%BB%E5%9E%8B%E6%9C%89%E5%93%AA%E4%BA%9B)

![通知类型](https://qiniu.kanes.top/blog/20241029203917.png)
- **Before**（前置通知）：目标对象的方法调用之前触发
- **After** （后置通知）：目标对象的方法调用之后触发
- **AfterReturning**（返回通知）：目标对象的方法调用完成，在返回结果值之后触发
- **AfterThrowing**（异常通知）：目标对象的方法运行中抛出 / 触发异常后触发。AfterReturning 和 AfterThrowing 两者互斥。如果方法调用成功无异常，则会有返回值；如果方法抛出了异常，则不会有返回值。
- **Around** （环绕通知）：编程式控制目标对象的方法调用。环绕通知是所有通知类型中可操作范围最大的一种，因为它可以直接拿到目标对象，以及要执行的方法，所以环绕通知可以任意的在目标对象的方法调用前后搞事，甚至不调用目标对象的方法




## Bean

简单来说，Bean 代指的就是那些被 IoC 容器所管理的对象。

### Bean作用域

- 指的是Bean实例的生命周期和可见范围

  - 1. singleton。默认的作用域，表示整个应用程序中只存在一个Bean实例，每次请求Bean都会返回同一个实例

  - 2. prototype。每次请求该Bean都会创建一个新的实例。每个实例都有自己的属性值和状态，相互独立

  - 3. request。一个HTTP请求中只存在一个Bean实例。同一个请求中，多次请求该Bean都回返回同一个实例。不同请求之间，该Bean的实例相互独立

  - 4. session。一个http session中只存在一个Bean实例。同一个Session中多次请求该Bean都返回同一个实例。独立

  - 5. application。再一个ServletContext中只存在一个Bean实例。只在上下文有效

  - 6. websocket。一个websocket只存在一个Bean

### 将类声明为Bean的注解有哪些

- @Component通用注解，可标注任意类为Spring主键。不知道Bean属于哪个层，可以使用

- @Repository对应持久层，Dao层 用于数据库相关工作

- @Service对应服务层，设计一些复杂的逻辑
  @Controller控制层

### @Component与@Bean的区别

- 前者作用于类，后者作用于方法

- 前者通过类路径扫描来自动侦测以及自动装配到Spring容器中（@ComponentScan扫描）
  @Bean通常时在标有该注解的方法中定义产生这个Bean，告诉Spring这是个实例

- @Bean的自定义性更强，很多地方只能通过@Bean来注册bean。比如引用第三方库中的类需要装配到Spring容器中

### 注入Bean的注解有哪些

- @Autowired（Spring）

- @Resource（JDK）

- @Inject（JDK）


### [@Autowired 和 @Resource 的区别是什么？](#autowired-和-resource-的区别是什么)

- `@Autowired` 是 Spring 提供的注解，`@Resource` 是 JDK 提供的注解。
- `Autowired` 默认的注入方式为`byType`（根据类型进行匹配），`@Resource`默认注入方式为 `byName`（根据名称进行匹配）。
- 当一个接口存在多个实现类的情况下，`@Autowired` 和`@Resource`都需要通过名称才能正确匹配到对应的 Bean。`Autowired` 可以通过 `@Qualifier` 注解来显式指定名称，`@Resource`可以通过 `name` 属性来显式指定名称。
- `@Autowired` 支持在构造函数、方法、字段和参数上使用。`@Resource` 主要用于字段和方法上的注入，不支持在构造函数或参数上使用。

### Bean 是线程安全的吗？

Spring 框架中的 Bean 是否线程安全，取决于其作用域和状态。

我们这里以最常用的两种作用域 prototype 和 singleton 为例介绍。几乎所有场景的 Bean 作用域都是使用默认的 singleton ，重点关注 singleton 作用域即可。

prototype 作用域下，每次获取都会创建一个新的 bean 实例，不存在资源竞争问题，所以不存在线程安全问题。singleton 作用域下，IoC 容器中只有唯一的 bean 实例，可能会存在资源竞争问题（取决于 Bean 是否有状态）。如果这个 bean 是有状态的话，那就存在线程安全问题（有状态 Bean 是指包含可变的成员变量的对象）。

### [Bean 的生命周期](https://javaguide.cn/system-design/framework/spring/spring-knowledge-and-questions-summary.html#bean-%E7%9A%84%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F%E4%BA%86%E8%A7%A3%E4%B9%88)

1. **创建 Bean 的实例**：Bean 容器首先会找到配置文件中的 Bean 定义，然后使用 Java 反射 API 来创建 Bean 的实例。
2. **Bean 属性赋值/填充**：为 Bean 设置相关属性和依赖，例如`@Autowired` 等注解注入的对象、`@Value` 注入的值、`setter`方法或构造函数注入依赖和值、`@Resource`注入的各种资源。
3. **Bean 初始化**：
	- 如果 Bean 实现了 `BeanNameAware` 接口，调用 `setBeanName()`方法，传入 Bean 的名字。
	- 如果 Bean 实现了 `BeanClassLoaderAware` 接口，调用 `setBeanClassLoader()`方法，传入 `ClassLoader`对象的实例。
	- 如果 Bean 实现了 `BeanFactoryAware` 接口，调用 `setBeanFactory()`方法，传入 `BeanFactory`对象的实例。
	- 与上面的类似，如果实现了其他 `*.Aware`接口，就调用相应的方法。
	- 如果有和加载这个 Bean 的 Spring 容器相关的 `BeanPostProcessor` 对象，执行`postProcessBeforeInitialization()` 方法
	- 如果 Bean 实现了`InitializingBean`接口，执行`afterPropertiesSet()`方法。
	- 如果 Bean 在配置文件中的定义包含 `init-method` 属性，执行指定的方法。
	- 如果有和加载这个 Bean 的 Spring 容器相关的 `BeanPostProcessor` 对象，执行`postProcessAfterInitialization()` 方法。
4. **销毁 Bean**：销毁并不是说要立马把 Bean 给销毁掉，而是把 Bean 的销毁方法先记录下来，将来需要销毁 Bean 或者销毁容器的时候，就调用这些方法去释放 Bean 所持有的资源。
	- 如果 Bean 实现了 `DisposableBean` 接口，执行 `destroy()` 方法。
	- 如果 Bean 在配置文件中的定义包含 `destroy-method` 属性，执行指定的 Bean 销毁方法。或者，也可以直接通过`@PreDestroy` 注解标记 Bean 销毁之前执行的方法。

## Spring MVC

MVC 是模型(Model)、视图(View)、控制器(Controller)的简写，其核心思想是通过将业务逻辑、数据、显示分离来组织代码。

### [Spring MVC 的核心组件](https://javaguide.cn/system-design/framework/spring/spring-knowledge-and-questions-summary.html#spring-mvc-%E7%9A%84%E6%A0%B8%E5%BF%83%E7%BB%84%E4%BB%B6%E6%9C%89%E5%93%AA%E4%BA%9B)
- **`DispatcherServlet`**：**核心的中央处理器**，负责接收请求、分发，并给予客户端响应。
- **`HandlerMapping`**：**处理器映射器**，根据 URL 去匹配查找能处理的 `Handler` ，并会将请求涉及到的拦截器和 `Handler` 一起封装。
- **`HandlerAdapter`**：**处理器适配器**，根据 `HandlerMapping` 找到的 `Handler` ，适配执行对应的 `Handler`；
- **`Handler`**：**请求处理器**，处理实际请求的处理器。
- **`ViewResolver`**：**视图解析器**，根据 `Handler` 返回的逻辑视图 / 视图，解析并渲染真正的视图，并传递给 `DispatcherServlet` 响应客户端

### [SpringMVC 工作原理](https://javaguide.cn/system-design/framework/spring/spring-knowledge-and-questions-summary.html#springmvc-%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86%E4%BA%86%E8%A7%A3%E5%90%97)

![工作原理](https://qiniu.kanes.top/blog/20241029204123.png)

1. 客户端（浏览器）发送请求， `DispatcherServlet`拦截请求。
2. `DispatcherServlet` 根据请求信息调用 `HandlerMapping` 。`HandlerMapping` 根据 URL 去匹配查找能处理的 `Handler`（也就是我们平常说的 `Controller` 控制器） ，并会将请求涉及到的拦截器和 `Handler` 一起封装。
3. `DispatcherServlet` 调用 `HandlerAdapter`适配器执行 `Handler` 。
4. `Handler` 完成对用户请求的处理后，会返回一个 `ModelAndView` 对象给`DispatcherServlet`，`ModelAndView` 顾名思义，包含了数据模型以及相应的视图的信息。`Model` 是返回的数据对象，`View` 是个逻辑上的 `View`。
5. `ViewResolver` 会根据逻辑 `View` 查找实际的 `View`。
6. `DispaterServlet` 把返回的 `Model` 传给 `View`（视图渲染）。
7. 把 `View` 返回给请求者（浏览器）

## [Spring-设计模式](https://javaguide.cn/system-design/framework/spring/spring-design-patterns-summary.html)

- **工厂设计模式** : Spring 使用工厂模式通过 `BeanFactory`、`ApplicationContext` 创建 bean 对象。
- **代理设计模式** : Spring AOP 功能的实现。
- **单例设计模式** : Spring 中的 Bean 默认都是单例的。
- **模板方法模式** : Spring 中 `jdbcTemplate`、`hibernateTemplate` 等以 Template 结尾的对数据库操作的类，它们就使用到了模板模式。
- **包装器设计模式** : 我们的项目需要连接多个数据库，而且不同的客户在每次访问中根据需要会去访问不同的数据库。这种模式让我们可以根据客户的需求能够动态切换不同的数据源。
- **观察者模式:** Spring 事件驱动模型就是观察者模式很经典的一个应用。
- **适配器模式** : Spring AOP 的增强或通知(Advice)使用到了适配器模式、spring MVC 中也是用到了适配器模式适配`Controller`。

## [Spring 的循环依赖](https://javaguide.cn/system-design/framework/spring/spring-knowledge-and-questions-summary.html#spring-%E7%9A%84%E5%BE%AA%E7%8E%AF%E4%BE%9D%E8%B5%96)

### Spring 循环依赖
循环依赖是指 Bean 对象循环引用，是两个或多个 Bean 之间相互持有对方的引用，例如 CircularDependencyA → CircularDependencyB → CircularDependencyA。

Spring 框架通过使用三级缓存来解决这个问题，确保即使在循环依赖的情况下也能正确创建 Bean。

Spring 中的三级缓存其实就是三个 Map。

- **一级缓存（singletonObjects）**：存放最终形态的 Bean（已经实例化、属性填充、初始化），单例池，为“Spring 的单例属性”⽽⽣。一般情况我们获取 Bean 都是从这里获取的，但是并不是所有的 Bean 都在单例池里面，例如原型 Bean 就不在里面。
- **二级缓存（earlySingletonObjects）**：存放过渡 Bean（半成品，尚未属性填充），也就是三级缓存中`ObjectFactory`产生的对象，与三级缓存配合使用的，可以防止 AOP 的情况下，每次调用`ObjectFactory#getObject()`都是会产生新的代理对象的。
- **三级缓存（singletonFactories）**：存放`ObjectFactory`，`ObjectFactory`的`getObject()`方法（最终调用的是`getEarlyBeanReference()`方法）可以生成原始 Bean 对象或者代理对象（如果 Bean 被 AOP 切面代理）。三级缓存只会对单例 Bean 生效。

Spring 创建 Bean 的流程：

1. 先去 **一级缓存 `singletonObjects`** 中获取，存在就返回；
2. 如果不存在或者对象正在创建中，于是去 **二级缓存 `earlySingletonObjects`** 中获取；
3. 如果还没有获取到，就去 **三级缓存 `singletonFactories`** 中获取，通过执行 `ObjectFacotry` 的 `getObject()` 就可以获取该对象，获取成功之后，从三级缓存移除，并将该对象加入到二级缓存中。

### **Spring 如何解决三级缓存**：

在三级缓存这一块，主要记一下 Spring 是如何支持循环依赖的即可，也就是如果发生循环依赖的话，就去 **三级缓存 `singletonFactories`** 中拿到三级缓存中存储的 `ObjectFactory` 并调用它的 `getObject()` 方法来获取这个循环依赖对象的前期暴露对象（虽然还没初始化完成，但是可以拿到该对象在堆中的存储地址了），并且将这个前期暴露对象放到二级缓存中，这样在循环依赖时，就不会重复初始化了！

不过，这种机制也有一些缺点，比如增加了内存开销（需要维护三级缓存，也就是三个 Map），降低了性能（需要进行多次检查和转换）。并且，还有少部分情况是不支持循环依赖的，比如非单例的 bean 和`@Async`注解的 bean 无法支持循环依赖。

### [@Lazy 能解决循环依赖吗？](#lazy-能解决循环依赖吗)

`@Lazy` 用来标识类是否需要懒加载/延迟加载，可以作用在类上、方法上、构造器上、方法参数上、成员变量中。

Spring Boot 2.2 新增了**全局懒加载属性**，开启后全局 bean 被设置为懒加载，需要时再去创建。

如非必要，尽量不要用全局懒加载。全局懒加载会让 Bean 第一次使用的时候加载会变慢，并且它会延迟应用程序问题的发现（当 Bean 被初始化时，问题才会出现）。

如果一个 Bean 没有被标记为懒加载，那么它会在 Spring IoC 容器启动的过程中被创建和初始化。如果一个 Bean 被标记为懒加载，那么它不会在 Spring IoC 容器启动时立即实例化，而是在第一次被请求时才创建。这可以帮助减少应用启动时的初始化时间，也可以用来解决循环依赖问题。

## [Spring 事务](https://javaguide.cn/system-design/framework/spring/spring-transaction.html)

### [Spring 管理事务的方式有几种？](#spring-管理事务的方式有几种)

- **编程式事务**：在代码中硬编码(在分布式系统中推荐使用) : 通过 `TransactionTemplate`或者 `TransactionManager` 手动管理事务，事务范围过大会出现事务未提交导致超时，因此事务要比锁的粒度更小。
- **声明式事务**：在 XML 配置文件中配置或者直接基于注解（单体应用或者简单业务系统推荐使用） : 实际是通过 AOP 实现（基于`@Transactional` 的全注解方式使用最多）

### [Spring 事务中哪几种事务传播行为?](#spring-事务中哪几种事务传播行为)

**事务传播行为是为了解决业务层方法之间互相调用的事务问题**。

当事务方法被另一个事务方法调用时，必须指定事务应该如何传播。例如：方法可能继续在现有事务中运行，也可能开启一个新事务，并在自己的事务中运行。

正确的事务传播行为可能的值如下:

**1.`TransactionDefinition.PROPAGATION_REQUIRED`**

使用的最多的一个事务传播行为，我们平时经常使用的`@Transactional`注解默认使用就是这个事务传播行为。如果当前存在事务，则加入该事务；如果当前没有事务，则创建一个新的事务。

**`2.TransactionDefinition.PROPAGATION_REQUIRES_NEW`**

创建一个新的事务，如果当前存在事务，则把当前事务挂起。也就是说不管外部方法是否开启事务，`Propagation.REQUIRES_NEW`修饰的内部方法会新开启自己的事务，且开启的事务相互独立，互不干扰。

**3.`TransactionDefinition.PROPAGATION_NESTED`**

如果当前存在事务，则创建一个事务作为当前事务的嵌套事务来运行；如果当前没有事务，则该取值等价于`TransactionDefinition.PROPAGATION_REQUIRED`。

**4.`TransactionDefinition.PROPAGATION_MANDATORY`**

如果当前存在事务，则加入该事务；如果当前没有事务，则抛出异常。（mandatory：强制性）

### [Spring 事务中的隔离级别有哪几种?](https://javaguide.cn/system-design/framework/spring/spring-knowledge-and-questions-summary.html#spring-%E4%BA%8B%E5%8A%A1%E4%B8%AD%E7%9A%84%E9%9A%94%E7%A6%BB%E7%BA%A7%E5%88%AB%E6%9C%89%E5%93%AA%E5%87%A0%E7%A7%8D)

### [@Transactional(rollbackFor = Exception.class)注解](https://javaguide.cn/system-design/framework/spring/spring-knowledge-and-questions-summary.html#transactional-rollbackfor-exception-class-%E6%B3%A8%E8%A7%A3%E4%BA%86%E8%A7%A3%E5%90%97)

`Exception` 分为运行时异常 `RuntimeException` 和非运行时异常，即使出现异常情况，它也可以保证数据的一致性。

当 `@Transactional` 注解作用于类上时，该类的所有 public 方法将都具有该类型的事务属性，同时，我们也可以在方法级别使用该标注来覆盖类级别的定义。

`@Transactional` 注解默认回滚策略是只有在遇到`RuntimeException`(运行时异常) 或者 `Error` 时才会回滚事务，而不会回滚 `Checked Exception`（受检查异常）。这是因为 Spring 认为`RuntimeException`和 Error 是不可预期的错误，而受检异常是可预期的错误，可以通过业务逻辑来处理。

## 常用注解
### [1. `@SpringBootApplication`](https://javaguide.cn/system-design/framework/spring/spring-common-annotations.html#_1-springbootapplication)

_这个注解是 Spring Boot 项目的基石，创建 SpringBoot 项目之后会默认在主类加上。_

可以把 `@SpringBootApplication`看作是 `@Configuration`、`@EnableAutoConfiguration`、`@ComponentScan` 注解的集合。

- `@EnableAutoConfiguration`：启用 SpringBoot 的自动配置机制
- `@ComponentScan`：扫描被`@Component` (`@Repository`,`@Service`,`@Controller`)注解的 bean，注解默认会扫描该类所在的包下所有的类。
- `@Configuration`：允许在 Spring 上下文中注册额外的 bean 或导入其他配置类

### [2. Spring Bean 相关](https://javaguide.cn/system-design/framework/spring/spring-common-annotations.html#_2-spring-bean-%E7%9B%B8%E5%85%B3)

####  @Autowired

自动导入对象到类中，被注入进的类同样要被 Spring 容器管理比如：Service 类注入到 Controller 类中。

####  @Component @Repository @Service @Controller

- `@Component`：通用的注解，可标注任意类为 `Spring` 组件。如果一个 Bean 不知道属于哪个层，可以使用`@Component` 注解标注。
- `@Repository` : 对应持久层即 Dao 层，主要用于数据库相关操作。
- `@Service` : 对应服务层，主要涉及一些复杂的逻辑，需要用到 Dao 层。
- `@Controller` : 对应 Spring MVC 控制层，主要用于接受用户请求并调用 Service 层返回数据给前端页面。

#### @RestController

`@RestController`注解是`@Controller`和`@ResponseBody`的合集,表示这是个控制器 bean,并且是将函数的返回值直接填入 HTTP 响应体中,是 REST 风格的控制器。

_Guide：现在都是前后端分离，说实话我已经很久没有用过`@Controller`。如果你的项目太老了的话，就当我没说。_

单独使用 `@Controller` 不加 `@ResponseBody`的话一般是用在要返回一个视图的情况，这种情况属于比较传统的 Spring MVC 的应用，对应于前后端不分离的情况。`@Controller` +`@ResponseBody` 返回 JSON 或 XML 形式数据

#### @Scope

声明 Spring Bean 的作用域，使用方法:

```java
@Bean
@Scope("singleton")
public Person personSingleton() {
    return new Person();
}
```

**四种常见的 Spring Bean 的作用域：**

- singleton : 唯一 bean 实例，Spring 中的 bean 默认都是单例的。
- prototype : 每次请求都会创建一个新的 bean 实例。
- request : 每一次 HTTP 请求都会产生一个新的 bean，该 bean 仅在当前 HTTP request 内有效。
- session : 每一个 HTTP Session 会产生一个新的 bean，该 bean 仅在当前 HTTP session 内有效。

#### @Configuration

一般用来声明配置类，可以使用 `@Component`注解替代，不过使用`@Configuration`注解声明配置类更加语义化。

```java
@Configuration
public class AppConfig {
    @Bean
    public TransferService transferService() {
        return new TransferServiceImpl();}}
```

### 处理常见的 HTTP 请求类型

**5 种常见的请求类型:**

- **GET**：请求从服务器获取特定资源。举个例子：`GET /users`（获取所有学生）
- **POST**：在服务器上创建一个新的资源。举个例子：`POST /users`（创建学生）
- **PUT**：更新服务器上的资源（客户端提供更新后的整个资源）。举个例子：`PUT /users/12`（更新编号为 12 的学生）
- **DELETE**：从服务器删除特定的资源。举个例子：`DELETE /users/12`（删除编号为 12 的学生）
- **PATCH**：更新服务器上的资源（客户端提供更改的属性，可以看做作是部分更新），使用的比较少，这里就不举例子了。

### [前后端传值](https://javaguide.cn/system-design/framework/spring/spring-common-annotations.html#_4-%E5%89%8D%E5%90%8E%E7%AB%AF%E4%BC%A0%E5%80%BC)
用于读取 Request 请求（可能是 POST,PUT,DELETE,GET 请求）的 body 部分并且**Content-Type 为 application/json** 格式的数据，接收到数据之后会自动将数据绑定到 Java 对象上去。系统会使用`HttpMessageConverter`或者自定义的`HttpMessageConverter`将请求的 body 中的 json 字符串转换为 java 对象。

```java
@PostMapping("/sign-up")
public ResponseEntity signUp(@RequestBody @Valid UserRegisterRequest userRegisterRequest) {
  userService.save(userRegisterRequest);
  return ResponseEntity.ok().build();
}
```

### [读取配置信息](https://javaguide.cn/system-design/framework/spring/spring-common-annotations.html#_5-%E8%AF%BB%E5%8F%96%E9%85%8D%E7%BD%AE%E4%BF%A1%E6%81%AF)

`@Value`(常用) `@ConfigurationProperties`(常用)   问题12

### [参数校验](https://javaguide.cn/system-design/framework/spring/spring-common-annotations.html#_6-%E5%8F%82%E6%95%B0%E6%A0%A1%E9%AA%8C)

_问题16_

**数据的校验的重要性就不用说了，即使在前端对数据进行校验的情况下，我们还是要对传入后端的数据再进行一遍校验，避免用户绕过浏览器直接通过一些 HTTP 工具直接向后端请求一些违法数据。**

Bean Validation 是一套定义 JavaBean 参数校验标准的规范 (JSR 303, 349, 380)，它提供了一系列注解，可以直接用于 JavaBean 的属性上，从而实现便捷的参数校验。

SpringBoot 项目的 spring-boot-starter-web 依赖中已经有 hibernate-validator 包，不需要引用相关依赖。


### [全局处理 Controller 层异常](https://javaguide.cn/system-design/framework/spring/spring-common-annotations.html#_7-%E5%85%A8%E5%B1%80%E5%A4%84%E7%90%86-controller-%E5%B1%82%E5%BC%82%E5%B8%B8)
问题17
1. `@ControllerAdvice` :注解定义全局异常处理类
2. `@ExceptionHandler` :注解声明异常处理方法

### [8. JPA 相关](https://javaguide.cn/system-design/framework/spring/spring-common-annotations.html#_8-jpa-%E7%9B%B8%E5%85%B3)

#### [8.1. 创建表](https://javaguide.cn/system-design/framework/spring/spring-common-annotations.html#_8-1-%E5%88%9B%E5%BB%BA%E8%A1%A8)
TODO

### [9. 事务 `@Transactional`](https://javaguide.cn/system-design/framework/spring/spring-common-annotations.html#_9-%E4%BA%8B%E5%8A%A1-transactional)
Spring事务，最后一个问题
在要开启事务的方法上使用`@Transactional`注解即可!

### [json 数据处理](https://javaguide.cn/system-design/framework/spring/spring-common-annotations.html#_10-json-%E6%95%B0%E6%8D%AE%E5%A4%84%E7%90%86)

#### [过滤 json 数据](https://javaguide.cn/system-design/framework/spring/spring-common-annotations.html#_10-1-%E8%BF%87%E6%BB%A4-json-%E6%95%B0%E6%8D%AE)

**`@JsonIgnoreProperties` 作用在类上用于过滤掉特定字段不返回或者不解析。**

```Java
//生成json时将userRoles属性过滤
@JsonIgnoreProperties({"userRoles"})
public class User {
    private String userName;
    private String fullName;
    private String password;
    private List<UserRole> userRoles = new ArrayList<>();
}
```

**`@JsonIgnore`一般用于类的属性上，作用和上面的`@JsonIgnoreProperties` 一样。**

```Java
public class User {
    private String userName;
    private String fullName;
    private String password;
   //生成json时将userRoles属性过滤
    @JsonIgnore
    private List<UserRole> userRoles = new ArrayList<>();
}
```

#### 格式化 json 数据

`@JsonFormat`一般用来格式化 json 数据。

比如：

```
@JsonFormat(shape=JsonFormat.Shape.STRING, pattern="yyyy-MM-dd'T'HH:mm:ss.SSS'Z'", timezone="GMT")
private Date date;
```

####  [扁平化对象](https://javaguide.cn/system-design/framework/spring/spring-common-annotations.html#_10-3-%E6%89%81%E5%B9%B3%E5%8C%96%E5%AF%B9%E8%B1%A1)

```java
@Getter
@Setter
@ToString
public class Account {
    private Location location;
    private PersonInfo personInfo;
  @Getter
  @Setter
  @ToString
  public static class Location {
     private String provinceName;
     private String countyName;
  }
  @Getter
  @Setter
  @ToString
  public static class PersonInfo {
    private String userName;
    private String fullName;
  }
}
```

```json
{
  "location": {
    "provinceName": "湖北",
    "countyName": "武汉"
  },
  "personInfo": {
    "userName": "coder1234",
    "fullName": "shaungkou"
  }
}
```

使用`@JsonUnwrapped` 扁平对象之后：

```java
@Getter
@Setter
@ToString
public class Account {
    @JsonUnwrapped
    private Location location;
    @JsonUnwrapped
    private PersonInfo personInfo;
    ......
}
```

```json
{
  "provinceName": "湖北",
  "countyName": "武汉",
  "userName": "coder1234",
  "fullName": "shaungkou"
}
```

### [测试相关](https://javaguide.cn/system-design/framework/spring/spring-common-annotations.html#_11-%E6%B5%8B%E8%AF%95%E7%9B%B8%E5%85%B3)

**`@ActiveProfiles`一般作用于测试类上， 用于声明生效的 Spring 配置文件。**

```java
@SpringBootTest(webEnvironment = RANDOM_PORT)
@ActiveProfiles("test")
@Slf4j
public abstract class TestBase {
  ......
}
```

**`@Test`声明一个方法为测试方法**
**`@Transactional`被声明的测试方法的数据会回滚，避免污染测试数据。**
**`@WithMockUser` Spring Security 提供的，用来模拟一个真实用户，并且可以赋予权限**

```java
    @Test
    @Transactional
    @WithMockUser(username = "user-id-18163138155", authorities = "ROLE_TEACHER")
    void should_import_student_success() throws Exception {
        ......
    }
```
	
---

## [Spring Data JPA](https://javaguide.cn/system-design/framework/spring/spring-knowledge-and-questions-summary.html#spring-data-jpa)

## 常见问题

### 1. 简单介绍一下 Spring?有啥缺点?

Spring 是重量级企业开发框架 **Enterprise JavaBean（EJB）** 的替代品，Spring 为企业级 Java 开发提供了一种相对简单的方法，通过 依赖注入 和 面向切面编程 ，用简单的 Java 对象（Plain Old Java Object，POJO） 实现了 EJB 的功能  
  
**虽然 Spring 的组件代码是轻量级的，但它的配置却是重量级的（需要大量 XML 配置）** 。  
  
为此，Spring 2.5 引入了基于注解的组件扫描，这消除了大量针对应用程序自身组件的显式 XML 配置。Spring 3.0 引入了基于 Java 的配置，这是一种类型安全的可重构配置方式，可以代替 XML。  
  
尽管如此，我们依旧没能逃脱配置的魔爪。开启某些 Spring 特性时，比如事务管理和 Spring MVC，还是需要用 XML 或 Java 进行显式配置。启用第三方库时也需要显式配置，比如基于 Thymeleaf 的 Web 视图。配置 Servlet 和过滤器（比如 Spring 的DispatcherServlet）同样需要在 web.xml 或 Servlet 初始化代码里进行显式配置。组件扫描减少了配置量，Java 配置让它看上去简洁不少，但 Spring 还是需要不少配置。  
  
光配置这些 XML 文件都够我们头疼的了，占用了我们大部分时间和精力。除此之外，相关库的依赖非常让人头疼，不同库之间的版本冲突也非常常见。

### 2. 为什么要有 SpringBoot?

Spring Boot 的诞生是为了简化 Spring 应用的开发和部署过程，让开发者更专注于业务逻辑的实现。

### 3. 说出使用 Spring Boot 的主要优点

1. 提高生产力：Spring Boot 的自动配置和开箱即用的功能，显著减少了手动配置和样板代码的编写时间，使得开发者能够更快速地构建和交付应用程序。  
2. 与 Spring 生态系统的无缝集成：Spring Boot 可以轻松集成 Spring 的各个模块（如 Spring JDBC、Spring ORM、Spring Data、Spring Security 等），简化了与这些工具的整合过程，增强了开发者的工作效率。  
3. 减少手动配置：Spring Boot 提供了合理的默认配置，开发者可以在大多数情况下直接使用这些默认配置来启动项目。当然，这些默认配置也可以根据项目需求进行修改。  
4. 嵌入式服务器：Spring Boot 自带内嵌的 HTTP 服务器（如 Tomcat、Jetty），开发者可以像运行普通 Java 程序一样运行 Spring Boot 应用程序，极大地简化了开发和测试过程。  
5. 适合微服务架构：Spring Boot 使得每个微服务都可以独立运行和部署，简化了微服务的开发、测试和运维工作，成为构建微服务架构的理想选择。  
6. 多种插件支持：Spring Boot 提供了多种插件，可以使用内置工具(如 Maven 和 Gradle)开发和测试 Spring Boot 应用程序。

### 4. 什么是 Spring Boot Starters?

Spring Boot Starters 是一组便捷的依赖描述符，它们预先打包了常用的库和配置。当我们开发 Spring 应用时，只需添加一个 Starter 依赖项，即可自动引入所有必要的库和配置，而无需手动逐一添加和配置相关依赖。  
  
这种机制显著简化了开发过程，特别是在处理复杂项目时尤为高效。通过添加一个简单的 Starter 依赖，开发者可以快速集成所需的功能，避免了手动管理多个依赖的繁琐和潜在错误。这不仅节省了时间，还减少了配置错误的风险，从而提升了开发效率。  
  
举个例子： 在没有 Spring Boot Starters 之前，开发一个 RESTful 服务或 Web 应用程序通常需要手动添加多个依赖，比如 Spring MVC、Tomcat、Jackson 等。这不仅繁琐，还容易导致版本不兼容的问题。而有了 Spring Boot Starters，我们只需添加一个依赖，如 spring-boot-starter-web，即可包含所有开发 REST 服务所需的库和依赖。

以下是一些常见的 Spring Boot Starter 及其用途：  
  
1. spring-boot-starter：基础的 Starter，包含了启动 Spring 应用所需的核心依赖，如 Spring 框架本身和日志系统（默认使用 SLF4J 和 Logback）。  
2. spring-boot-starter-web：用于构建 Web 应用程序，包括 RESTful 服务。它包含了 Spring MVC、Tomcat（默认嵌入式服务器）、Jackson 等依赖。  
3. spring-boot-starter-data-jpa：用于构建 JPA 应用程序，包含 Spring Data JPA 和 Hibernate。它简化了数据库访问层的开发，提供了对关系型数据库的便捷操作。  
4. spring-boot-starter-security：用于集成 Spring Security，提供身份验证和授权功能，帮助开发者快速实现安全机制。  
5. spring-boot-starter-test：提供测试所需的依赖，包含了 JUnit、Mockito、Spring Test 等库，帮助开发者编写单元测试、集成测试和 Mock 测试。  
6. spring-boot-starter-actuator：可以监控应用程序的运行状态，还可以收集应用程序的各种指标信息。  
7. spring-boot-starter-aop：提供对面向切面编程（AOP）的支持，包含 Spring AOP 和 AspectJ。  
8. spring-boot-starter-validation：集成了 Hibernate Validator，用于实现 Java Bean 的校验机制，通常与 Spring MVC 或 Spring Data 一起使用。

### 5. Spring Boot 支持哪些内嵌 Servlet 容器？如何选择？

Spring Boot 提供了三种 Web 容器，分别为 Tomcat、Jetty 和 Undertow 。在 Spring Boot 项目中，我们可以灵活地选择不同的嵌入式 Servlet 容器来提供 HTTP 服务。默认情况下，Spring Boot 使用 Tomcat 作为嵌入式服务器，但我们也可以根据项目需求选择其他容器，如 Undertow 和 Jetty。  
  
1. Tomcat：适用于大多数常规 Web 应用程序和 RESTful 服务，易于使用和配置，但在高并发场景下确实可能不如 Undertow 表现出色。  
2. Undertow：Undertow 具有极低的启动时间和资源占用，支持非阻塞 IO（NIO），在高并发场景下表现出色，性能优于 Tomcat。  
3. Jetty：如果应用程序涉及即时通信、聊天系统或其他需要保持长连接的场景，Jetty 是一个更好的选择。它在处理长连接和 WebSocket 时表现优越。另外。Jetty 在性能和内存使用方面通常优于 Tomcat，虽然在极端高并发场景中可能略逊于 Undertow。

### 6. 如何在 Spring Boot 应用程序中使用 Jetty 而不是 Tomcat?

Spring Boot （spring-boot-starter-web）使用 Tomcat 作为默认的嵌入式 servlet 容器, 如果你想使用 Jetty 的话只需要修改pom.xml(Maven)或者build.gradle(Gradle)就可以了。

### 7. 介绍一下@SpringBootApplication 注解

可以看出大概可以把 @SpringBootApplication看作是 @Configuration、@EnableAutoConfiguration、@ComponentScan 注解的集合。

根据 SpringBoot 官网，这三个注解的作用分别是：  
  
- ●@EnableAutoConfiguration：启用 SpringBoot 的自动配置机制  
- ●@ComponentScan： 扫描被@Component (@Service,@Controller)注解的 bean，注解默认会扫描该类所在的包下所有的类。  
- ●@Configuration：允许在上下文中注册额外的 bean 或导入其他配置类

### 8. Spring Boot 的自动配置是如何实现的?

Spring Boot 的自动配置机制是通过 @SpringBootApplication 注解启动的，这个注解本质上是几个关键注解的组合。我们可以将 @SpringBootApplication 看作是 @Configuration、@EnableAutoConfiguration 和 @ComponentScan 注解的集合。  
  
- ●@EnableAutoConfiguration: 启用 Spring Boot 的自动配置机制。它是自动配置的核心，允许 Spring Boot 根据项目的依赖和配置自动配置 Spring 应用的各个部分。  

- ●@ComponentScan: 启用组件扫描，扫描被 @Component（以及 @Service、@Controller 等）注解的类，并将这些类注册为 Spring 容器中的 Bean。默认情况下，它会扫描该类所在包及其子包下的所有类。  

- ●@Configuration: 允许在上下文中注册额外的 Bean 或导入其他配置类。它相当于一个具有 @Bean 方法的 Spring 配置类。

### 9. 开发 RESTful Web 服务常用的注解有哪些？

Spring Bean 相关：  
  
- ●@Autowired : 自动导入对象到类中，被注入进的类同样要被 Spring 容器管理。  
- ●@RestController : @RestController注解是@Controller和@ResponseBody的合集,表示这是个控制器 bean,并且是将函数的返回值直 接填入 HTTP 响应体中,是 REST 风格的控制器。  
- ●@Component ：通用的注解，可标注任意类为 Spring 组件。如果一个 Bean 不知道属于哪个层，可以使用@Component 注解标注。  
- ●@Repository : 对应持久层即 Dao 层，主要用于数据库相关操作。  
- ●@Service : 对应服务层，主要涉及一些复杂的逻辑，需要用到 Dao 层。  
- ●@Controller : 对应 Spring MVC 控制层，主要用于接受用户请求并调用 Service 层返回数据给前端页面。  
  
处理常见的 HTTP 请求类型：  
  
- ●@GetMapping : GET 请求、  
- ●@PostMapping : POST 请求。  
- ●@PutMapping : PUT 请求。  
- ●@DeleteMapping : DELETE 请求。

前后端传值：  
  
- ●@RequestParam以及@Pathvariable：@PathVariable用于获取路径参数，@RequestParam用于获取查询参数。  
- ●@RequestBody ：用于读取 Request 请求（可能是 POST,PUT,DELETE,GET 请求）的 body 部分并且 Content-Type 为 application/json 格式的数据，接收到数据之后会自动将数据绑定到 Java 对象上去。系统会使用HttpMessageConverter或者自定义的HttpMessageConverter将请求的 body 中的 json 字符串转换为 Java 对象。

### 10. Spirng Boot 常用的两种配置文件

可以通过 application.properties或者 application.yml 对 Spring Boot 程序进行简单的配置。如果，你不进行配置的话，就是使用的默认配置。

### 11. 什么是 YAML？YAML 配置的优势在哪里 ?

YAML 是一种人类可读的数据序列化语言。它通常用于配置文件。与属性文件相比，如果我们想要在配置文件中添加复杂的属性，YAML 文件就更加结构化，而且更少混淆。可以看出 YAML 具有分层配置数据。

### 12. Spring Boot 常用的读取配置文件的方法有哪些？

1. 通过 @value 读取比较简单的配置信息
2. 通过@ConfigurationProperties读取并与 bean 绑定
3. 通过@ConfigurationProperties读取并校验
4. @PropertySource读取指定的 properties 文件

### 13. Spring Boot 加载配置文件的优先级了解么？

![](https://qiniu.kanes.top/blog/20241029221913.png)


### 14. 常用的 Bean 映射工具有哪些？

常用的 Bean 映射工具有：Spring BeanUtils、Apache BeanUtils、MapStruct、ModelMapper、Dozer、Orika、JMapper 。  
  
由于 Apache BeanUtils 、Dozer 、ModelMapper 性能太差，所以不建议使用。MapStruct 性能更好而且使用起来比较灵活，是一个比较不错的选择。

### 15. Spring Boot 如何监控系统实际运行状况？

我们可以使用 Spring Boot Actuator 来对 Spring Boot 项目进行简单的监控。

集成了这个模块之后，你的 Spring Boot 应用程序就自带了一些开箱即用的获取程序运行时的内部状态信息的 API。  
  
比如通过 GET 方法访问 /health 接口，你就可以获取应用程序的健康指标。  
  
不过，实际工作中，我们一般会使用更成熟的监控系统例如 Prometheus ，很少会直接用 Spring Boot Actuator。

### 16. Spring Boot 如何做请求参数校验？

即使在前端对数据进行校验的情况下，我们还是要对传入后端的数据再进行一遍校验，避免用户绕过浏览器直接通过一些 HTTP 工具直接向后端请求一些违法数据。  
  
Spring Boot 程序做请求参数校验的话只需要spring-boot-starter-web 依赖就够了，它的子依赖包含了我们所需要的东西。

1. 校验注解
	●@Null 被注释的元素必须为 null  
	●@NotNull 被注释的元素必须不为 null  
	●@AssertTrue 被注释的元素必须为 true  
	●@AssertFalse 被注释的元素必须为 false  
	●@Min(value) 被注释的元素必须是一个数字，其值必须大于等于指定的最小值  
	●@Max(value) 被注释的元素必须是一个数字，其值必须小于等于指定的最大值  
	●@DecimalMin(value) 被注释的元素必须是一个数字，其值必须大于等于指定的最小值  
	●@DecimalMax(value) 被注释的元素必须是一个数字，其值必须小于等于指定的最大值  
	●@Size(max=, min=) 被注释的元素的大小必须在指定的范围内  
	●@Digits (integer, fraction) 被注释的元素必须是一个数字，其值必须在可接受的范围内  
	●@Past 被注释的元素必须是一个过去的日期  
	●@Future 被注释的元素必须是一个将来的日期  
	●@Pattern(regex=,flag=) 被注释的元素必须符合指定的正则表达式
2. 验证请求体(RequestBody)
```java
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Person {
@NotNull(message = "classId 不能为空")
private String classId;
@Size(max = 33)
@NotNull(message = "name 不能为空")
private String name;
@Pattern(regexp = "((^Man$|^Woman$|^UGM$))", message = "sex 值不在可选范围")
@NotNull(message = "sex 不能为空")
private String sex;
@Email(message = "email 格式不正确")
@NotNull(message = "email 不能为空")
private String email;}
```
3. 验证请求参数(Path Variables 和 Request Parameters)
```java
@RestController
@RequestMapping("/api")
public class PersonController {
@PostMapping("/person")
public ResponseEntity<Person> getPerson(@RequestBody @Valid Person person) {
return ResponseEntity.ok().body(person);}}
```

### 17. 如何使用 Spring Boot 实现全局异常处理？

Spring Boot 应用程序可以借助 @RestControllerAdvice 和 @ExceptionHandler 实现全局统一异常处理。
```java
@RestControllerAdvice
public class GlobalExceptionHandler {
@ExceptionHandler(BusinessException.class)
public Result businessExceptionHandler(HttpServletRequest request, BusinessException e){
...
return Result.faild(e.getCode(), e.getMessage());
}...}
```

@RestControllerAdvice 是 Spring 4.3 中引入的，是@ControllerAdvice 和 @ResponseBody 的结合体，你也可以将  @RestControllerAdvice 替换为@ControllerAdvice和  @ResponseBody。这样的话，如果响应内容不是数据的话，就不需要在方法上添加 @ResponseBody，更加灵活。

### 18. Spring Boot 中如何实现定时任务 ?

```java
@Component
public class ScheduledTasks {
private static final Logger log = LoggerFactory.getLogger(ScheduledTasks.class);
private static final SimpleDateFormat dateFormat = new SimpleDateFormat("HH:mm:ss");
/**
* fixedRate：固定速率执行。每5秒执行一次。
*/
@Scheduled(fixedRate = 5000)
public void reportCurrentTimeWithFixedRate() {
log.info("Current Thread : {}", Thread.currentThread().getName());
log.info("Fixed Rate Task : The time is now {}", dateFormat.format(new Date()));}}
```

单纯依靠 @Scheduled 注解 还不行，我们还需要在 SpringBoot 中我们只需要在启动类上加上@EnableScheduling 注解，这样才可以启动定时任务。@EnableScheduling 注解的作用是发现注解 @Scheduled 的任务并在后台执行该任务。