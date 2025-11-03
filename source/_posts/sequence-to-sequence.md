---
title: Sequence to sequence
date: 2022-08-16 15:01:08
categories:
  - DL李宏毅
summary: >
  Sequence to sequence
  
  Batch Normalization
  
  Transformer 
  
  Transformer和Bert有很大联系
  
  Sequence-to-sequence (Seq2seq)
  
  不知道output的长度，需要机器自行决定，例如语音辨识输入语音信号，输出是语音辨识的结果  
  
  
  
  语音合成
  
  语音辨识反过来就是语音合成
  
  
  聊天机器人
  
  
  
  NLP任务
---
# Sequence to sequence

## Batch Normalization

## Transformer 

Transformer和Bert有很大联系

### Sequence-to-sequence (Seq2seq)

不知道output的长度，需要机器自行决定，例如语音辨识输入语音信号，输出是语音辨识的结果  

![](https://qiniu.kanes.top/blog/1f603f03.png)

#### 语音合成

语音辨识反过来就是语音合成
![](https://qiniu.kanes.top/blog/4e7c48dc.png)

#### 聊天机器人

![](https://qiniu.kanes.top/blog/559fbc30.png)

#### NLP任务

往往需要客制化模型
![](https://qiniu.kanes.top/blog/ca81943d.png)

#### 文法剖析

![](https://qiniu.kanes.top/blog/35c05e26.png)
![](https://qiniu.kanes.top/blog/55771c28.png)

#### Encoder

给一排向量输出一排向量
![](https://qiniu.kanes.top/blog/4ffb8aa9.png)

每一个block做的事情是好几个layer做的事情。先做一个self-attention，input一排vector，输出一排vector
![](https://qiniu.kanes.top/blog/e710feb1.png)

![](https://qiniu.kanes.top/blog/74329b5b.png)

#### Decoder

（预测下一个输入）
先给特殊符号作为开始，decoder吐出一个很长的向量 

![](https://qiniu.kanes.top/blog/5ff79802.png)
![](https://qiniu.kanes.top/blog/f524657c.png)

#### Encoder与Decoder架构区别

![](https://qiniu.kanes.top/blog/6f9ebb54.png)
最后会做一个softmax，中间加了一个masked。  
Self-attention看完a1234后输出b1，而Masked Self-attention，则不能再看a234，看完a1输出b1
![](https://qiniu.kanes.top/blog/dfcc17ee.png)

![](https://qiniu.kanes.top/blog/f08ea9b3.png)

![](https://qiniu.kanes.top/blog/383e3b56.png)