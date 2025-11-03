---
title: reasoning≠coding
date: '2024-12-29 12:31:50'
categories:
  - 人工智能
tags:
  - 人工智能
---
很多人说，reasoning=coding，o3就是最能写代码的模型。

我的看法是，reasoning指的是扔一个简单干净的问题，给出天才回答的能力。

这么说吧，如果把o3扔到20世纪，一定是全世界最牛逼的理论CS科学家，3-SAT、max flow、min cut、红黑树、LU分解、KMP、各种proof-base的加密算法，轻轻松松全拿下， 一口气构建整个TCS大厦。

解决TCS问题，就是解决抽象出来的数学、计算、拓扑问题，本质上可以认为和“解决数学难题”是一种类似的能力。

（但是解决CS问题不等于解决数学问题，cs不等于数学，cs和pure math没有直接关系）

但是，真正日常工作上班写代码，跟研究理论计算机问题，是完完全全的两种能力、两种模式、两种思维。

现实中真正的coding能力，不仅是把系统搭好，而且需要强烈的耐压能力和记忆力，还要不断动手配置、动手测试、动手调试、完成各种profiling的工作，

你不止需要跳跃式读代码，和机器互动，你还要跟同事互动，跟一大堆文档互动，跟不同配置环境互动，跟各种dependency的文档互动，然后把这些复杂的关系一一捋清楚，记在脑子里，然后一点点去把模块和功能摸索一遍。

这跟设计一个简单、干净、天才、杰出的TCS算法，是完完全全的两回事。

另外，你也千万不要认为architect（架构师）是在解决高级、抽象、干净、完美的数学题，

真正合格的architect，恰恰是手最脏、摸技术细节最多、调试最多、profiling最多的人——然后从这些反复枯燥的工作中，不断总结和思考，不断用脏手去尝试，做出正确架构和设计的选择，

说“真正的架构师，才需要o3级别的智能”的人，都是纯纯的大外行。

现在所有做coding agent的项目，都遇到一个最直接的死穴：context window太小了，几个文件还能喂进去，整个代码是不可能喂进去的。

现在一堆人在专注于给agent解决memory的问题，但是在针对coding问题上，用memory是不能解决任何问题的。

现在市场上的coding agent大概就是这么一个水平的人：

你给他看一个定义充足、干净、简单、难度高的问题，他可以通过step by step的reasoning，给你一个非常精美的解；

你给他一个20万行代码的巨型project，根本没办法下手；

然后coding agent的作者们，会用各种RAG的方法，去给model去喂一堆各种片段，试图用few shot的办法来直接幻想出答案——结果必然是错的（比如cursor、windsurf），

而另一些coding agent的作者们，试图step by step引导gpt-4o，去完成design driven或者test driven的开发流程，用大量的资源去保证每一步提供gpt-4o的信息量是充足的，以等待他进行下一步的action，包括添加文件、修改文件，或者在terminal里执行运行、编译、测试等等工作（比如devin），

而更麻烦的问题是，现实中绝大多数人还要跟aws打交道，跟database打交道，跟各种private key和权限打交道，跟各种container打交道——本质就是跟不同的环境和人打交道，

而这种coding以外的工作，要么交给一个human proxy，在适当的时刻引导人类去干预指导（非常复杂且需要实时盯着），要么你开始把所有密码、账户、权限都交给它，让它来决定什么时候去操作（非常危险），

总而言之，我反复讲的一点：

LLM和目前Agent技术，可以代替很多tcs（理论计算机） phd，

但是代替不了业务和工作稍微复杂一点点的程序员，包括设计复杂system（包括mlsys）的phd。

所以这也是我为什么从最最一开始就看好moonshot，其实context window在一些诸如coding或者法律工作中上限的能力，

如果你相信scaling law，你就应该不仅相信multi agent，parallel task scheduling，也应该相信context window的问题会逐步解决，

如果不把context window解决掉，或者坚信fine tuning比context window更重要——那么很多问题就会彻底卡死，成为这一轮AI、LLM、vertical AI agent浪潮的真正瓶颈。
