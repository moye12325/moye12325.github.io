---
description: "Transformer和Bert有很大联系"
title: Sequence to sequence
date: 2022-08-16 15:01:08
categories: [深度学习]
tags: ['NLP', 'Transformer']
---
# Sequence to sequence

## Batch Normalization

## Transformer 

Transformer和Bert有很大联系

### Sequence-to-sequence (Seq2seq)

不知道output的长度，需要机器自行决定，例如语音辨识输入语音信号，输出是语音辨识的结果  

![Sequence to sequen 配图 1](/images/qiniu/1f603f03.png)

#### 语音合成

语音辨识反过来就是语音合成
![Sequence to sequen 配图 2](/images/qiniu/4e7c48dc.png)

#### 聊天机器人

![Sequence to sequen 配图 3](/images/qiniu/559fbc30.png)

#### NLP任务

往往需要客制化模型
![Sequence to sequen 配图 4](/images/qiniu/ca81943d.png)

#### 文法剖析

![Sequence to sequen 配图 5](/images/qiniu/35c05e26.png)
![Sequence to sequen 配图 6](/images/qiniu/55771c28.png)

#### Encoder

给一排向量输出一排向量
![Sequence to sequen 配图 7](/images/qiniu/4ffb8aa9.png)

每一个block做的事情是好几个layer做的事情。先做一个self-attention，input一排vector，输出一排vector
![Sequence to sequen 配图 8](/images/qiniu/e710feb1.png)

![Sequence to sequen 配图 9](/images/qiniu/74329b5b.png)

#### Decoder

（预测下一个输入）
先给特殊符号作为开始，decoder吐出一个很长的向量 

![Sequence to sequen 配图 10](/images/qiniu/5ff79802.png)
![Sequence to sequen 配图 11](/images/qiniu/f524657c.png)

#### Encoder与Decoder架构区别

![Sequence to sequen 配图 12](/images/qiniu/6f9ebb54.png)
最后会做一个softmax，中间加了一个masked。  
Self-attention看完a1234后输出b1，而Masked Self-attention，则不能再看a234，看完a1输出b1
![Sequence to sequen 配图 13](/images/qiniu/dfcc17ee.png)

![Sequence to sequen 配图 14](/images/qiniu/f08ea9b3.png)

![Sequence to sequen 配图 15](/images/qiniu/383e3b56.png)

