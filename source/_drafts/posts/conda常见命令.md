---
date: 2024-07-22T17:47:41.513Z
updated: null
title: conda常见命令
slug: '5765347365487'
oid: 669e9b3d2a6fe84dfe920956
categories: 所遇问题
type: post
permalink: /posts/所遇问题/5765347365487
---


# An In-Depth Guide to Conda Commands

Conda is a powerful package management system that allows you to create and manage isolated environments for different projects, making it easier to work with different sets of dependencies. Whether you're a beginner or an experienced user, understanding the various Conda commands is essential for efficient package management. In this blog post, we will explore the detailed use of Conda commands in markdown format.

## Installation

Before we dive into the various commands, let's start with the installation process for Conda. You can download and install Conda by following the instructions provided on the official Conda website (https://conda.io). Once installed, you can open your terminal or command prompt and begin using Conda.

## Creating and Managing Environments

### Creating a New Environment

To create a new environment with Conda, use the `conda create` command followed by the desired environment name. You can also specify the Python version you want to use:

```
conda create --name myenv python=3.9
```

### Activating an Environment

To activate an environment, use the `conda activate` command followed by the environment name:

```
conda activate myenv
```

### Deactivating an Environment

To deactivate the current environment and return to the base environment, use the `conda deactivate` command:

```
conda deactivate
```

### Listing Environments

To list all the environments created with Conda, you can use the `conda env list` command:

```
conda env list
```

### Removing an Environment

To remove an environment, use the `conda env remove` command followed by the environment name:

```
conda env remove --name myenv
```

## Managing Packages

### Installing Packages

To install packages into your active environment, you can use the `conda install` command followed by the package names:

```
conda install numpy pandas matplotlib
```

You can also specify the version of a package if needed:

```
conda install numpy=1.21.0
```

### Updating Packages

To update packages to their latest versions, use the `conda update` command followed by the package names:

```
conda update numpy pandas matplotlib
```

To update all packages in the current environment, use the following command:

```
conda update --all
```

### Listing Installed Packages

To list all the packages installed in the current environment, you can use the `conda list` command:

```
conda list
```

### Removing Packages

To remove a specific package from the environment, use the `conda remove` command followed by the package name:

```
conda remove numpy
```

### Searching for Packages

To search for packages available in the Conda repository, you can use the `conda search` command followed by the package name or keywords:

```
conda search pandas
```

## Managing Channels

### Adding Channels

Conda allows you to add additional channels to search for packages. To add a channel, use the `conda config` command with the `--add channels` flag followed by the channel name:

```
conda config --add channels conda-forge
```

### Removing Channels

To remove a channel from the configuration, use the `conda config` command with the `--remove channels` flag followed by the channel name:

```
conda config --remove channels conda-forge
```

### Listing Channels

To list all the channels in your Conda configuration, use the `conda config` command with the `--show channels` flag:

```
conda config --show channels
```

## Miscellaneous Commands

### Creating an Environment from an Environment File

To create an environment based on an environment file, you can use the `conda env create` command followed by the

 file name:

```
conda env create --file environment.yml
```

### Exporting an Environment

To export the current environment to an environment file, use the `conda env export` command:

```
conda env export > environment.yml
```

### Activating Conda in a Shell

If you're using a shell other than Bash or Zsh, you might need to activate Conda using the `conda init` command:

```
conda init <shell_name>
```

Replace `<shell_name>` with your shell name (e.g., `conda init fish`).

## Conclusion

Conda provides a comprehensive set of commands to create, manage, and maintain isolated environments with ease. Understanding and utilizing these commands effectively can significantly enhance your workflow and make package management a breeze. In this blog post, we covered the fundamental Conda commands for creating and managing environments, installing and updating packages, managing channels, and a few miscellaneous commands. With this knowledge, you're well on your way to becoming a Conda power user.

Happy Conda-ing!



# Conda 命令深入指南

Conda 是一个功能强大的包管理系统，允许您为不同的项目创建和管理隔离的环境，从而更轻松地处理不同的依赖项集。 

## 安装

可以按照 Conda 官方网站 (https://conda.io) 上提供的说明下载并安装 Conda。 安装后，可以打开终端或命令提示符并开始使用 Conda。

## 创建和管理环境

### 创建新环境

要使用 Conda 创建新环境，请使用“conda create”命令，后跟所需的环境名称。 您还可以指定要使用的 Python 版本：

```
conda create --name myenv python=3.9
```

### 激活环境

要激活环境，请使用“conda activate”命令，后跟环境名称：

```
conda activate myenv
```

### 停用当前环

要停用当前环境并返回到基本环境，请使用“conda deactivate”命令：

```
conda deactivate
```

### 列出环境

要列出使用 Conda 创建的所有环境，可以使用 `conda env list` 命令：

```
conda env list
```

### 删除环境

要删除环境，请使用“conda env remove”命令，后跟环境名称：

```
conda env remove --name myenv
```

## 软件包管理

### 软件包安装

要将软件包安装到活动环境中，您可以使用“conda install”命令，后跟软件包名称：

```
conda install numpy pandas matplotlib
```

如果需要，您还可以指定包的版本：

```
conda install numpy=1.21.0
```

### 更新包

要将软件包更新到最新版本，请使用“conda update”命令，后跟软件包名称：

```
conda update numpy pandas matplotlib
```

要更新当前环境中的所有软件包，请使用以下命令：

```
conda update --all
```

### 列出已安装的软件包

要列出当前环境中安装的所有软件包，可以使用 `conda list` 命令：

```
conda list
```

### 删除包

要从环境中删除特定包，请使用“conda remove”命令，后跟包名称：

```
conda remove numpy
```

### 搜索包

要搜索 Conda 存储库中可用的包，您可以使用“conda search”命令，后跟包名称或关键字：

```
conda search pandas
```

## 管理渠道（安装源）

### 添加渠道

Conda 允许您添加额外的渠道来搜索包。 要添加通道，请使用“conda config”命令和“--addchannels”标志，后跟通道名称：

```
conda config --add channels conda-forge
```

### 删除渠道

要从配置中删除通道，请使用“conda config”命令和“--removechannels”标志，后跟通道名称：

```
conda config --remove channels conda-forge
```

### 列出渠道

要列出 Conda 配置中的所有渠道，请使用带有“--showchannels”标志的“conda config”命令：

```
conda config --show channels
```

## 杂项命令

### 从环境文件创建环境

要基于环境文件创建环境，可以使用 `conda env create` 命令，后跟

  文件名：

```
conda env create --file environment.yml
```

### 导出环境

要将当前环境导出到环境文件，请使用“conda env export”命令：

```
conda env export > environment.yml
```

### 在 Shell 中激活 Conda

如果您使用的是 Bash 或 Zsh 以外的 shell，则可能需要使用“conda init”命令激活 Conda：

```
conda init <shell_name>
```

将 `<shell_name>` 替换为您的 shell 名称（例如，`conda init Fish`）。

## 额外链接（待整理）
[重置base](https://blog.csdn.net/weixin_39967072/article/details/124628696)：https://blog.csdn.net/weixin_39967072/article/details/124628696
[删除、关闭anaconda的base环境](https://blog.csdn.net/m0_46114594/article/details/110696046)：https://blog.csdn.net/m0_46114594/article/details/110696046
[Conda清理缓存](https://blog.csdn.net/weixin_41481113/article/details/88411241)：https://blog.csdn.net/weixin_41481113/article/details/88411241