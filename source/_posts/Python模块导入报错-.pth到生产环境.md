---
title: Python模块导入报错-.pth到生产环境
date: 2025-11-25 00:00:00
categories: [Python开发]
tags: ['Docker', 'Python', '测试', '部署']
---

## 问题的起点：找不到模块

在Python开发中经常遇到`ModuleNotFoundError`，明明文件就在那里,Python就是找不到。原因很简单:Python只在`sys.path`列出的路径中查找模块,你的项目目录不在这个列表里。

## .pth：开发环境的快速解决方案

.pth文件提供了一个优雅的解决方式。Python启动时会自动读取site-packages目录下的.pth文件，把里面列出的路径加到`sys.path`中。

### 具体操作

找到conda环境的site-packages：
```python
import site
print(site.getsitepackages())
```

创建一个.pth文件（比如`my_project.pth`），每行写一个路径：
```
/home/username/my_project/src
/home/username/another_project
```

重启Python后这些路径就自动加载了。不需要在代码里写`sys.path.append()`，也不需要设置环境变量。

### 为什么这么方便

假设你的项目结构是这样：
```
my_project/
├── src/
│   ├── module_a/
│   └── module_b/
└── tests/
```

配置好.pth后，在任何地方都能直接`from module_a import utils`，非常直观。

## 问题来了：什么是生产环境

很多人搞不清开发环境和生产环境的区别。简单说：

- **开发环境**：你写代码的地方，只有你自己用，可以随便折腾
- **生产环境**：真实用户访问的系统，淘宝的服务器、微信的后台，必须稳定可靠

就像厨师试菜（开发）和餐厅营业（生产）的区别。

## .pth在生产环境的致命问题

### 环境不一致

你在本地配了.pth，代码能跑。但部署到服务器上，忘记配置.pth了，代码直接报错。更糟的是，你有10台服务器，每台都要手动配置，漏了一台就出问题。

### 依赖不透明

别人拿到你的代码和`requirements.txt`，安装完依赖后运行，发现还是报错找不到模块。因为.pth配置的路径根本不在`requirements.txt`里，他们完全不知道还需要配置什么。

### 容器化部署崩溃

现在很多项目用Docker部署。你在Dockerfile里写好了：
```dockerfile
COPY . /app
RUN pip install -r requirements.txt
```

但.pth指向的是`/home/username/my_project`，这个路径在容器里根本不存在，代码直接挂掉。

### 路径硬编码

开发机路径是`/home/zhangsan/projects`，测试服务器是`/opt/apps`，生产服务器是`/var/www`。每个环境都要单独配置.pth，维护成本极高。

这些问题的本质是：.pth把路径配置从代码层面移到了系统层面，但没有任何版本控制和管理机制。

## 正确的解决方案

那不用.pth的话，难道要大规模修改代码吗？其实不用。

### 可编辑安装：零改动的标准方案

在项目根目录创建一个`setup.py`：
```python
from setuptools import setup, find_packages

setup(
    name="my_project",
    version="0.1.0",
    packages=find_packages(),
)
```

然后执行：
```bash
pip install -e .
```

就这样，完成了。代码一行不用改，导入方式完全不变。

`-e`是editable的意思，修改代码后不需要重新安装，效果和.pth一模一样。区别是它走的是标准的Python包安装机制，不是搞一个本地配置文件。

### 为什么这样更好

当你需要部署到生产环境时，把`pip install -e .`改成`pip install .`就行了，会把代码正式安装到Python环境中。或者直接上传到私有PyPI服务器，其他服务器用`pip install my_project`统一安装。

整个过程可以写进CI/CD流程，可以做版本管理，可以回滚到任意版本。

### 如果项目结构特殊

代码在src目录下：
```python
setup(
    name="my_project",
    version="0.1.0",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
)
```

多个分散的模块：
```python
setup(
    name="my_project",
    version="0.1.0",
    packages=['module_a', 'module_b'],
    package_dir={
        'module_a': 'src/module_a',
        'module_b': 'lib/module_b',
    }
)
```

`setup.py`的配置非常灵活，基本能适配任何项目结构。

### 现代化的pyproject.toml

如果不想用`setup.py`，可以用更现代的`pyproject.toml`：
```toml
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "my_project"
version = "0.1.0"

[tool.setuptools.packages.find]
where = ["src"]
```

安装方式完全一样：`pip install -e .`

### 实在不想动结构

如果项目很混乱，暂时不想整理，可以在入口脚本加几行：
```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

# 后面正常写业务代码
from module_a import utils
```

虽然不够优雅，但至少把路径配置放回了代码里，可以进版本控制。

## 三分钟迁移指南

你现在的项目用着.pth，想改成标准方式：

1. 在项目根目录创建`setup.py`（5行代码）
2. 运行`pip install -e .`
3. 删除.pth文件

完成。代码不用动一个字。

## 什么时候该用哪个方案

开发阶段，自己一个人写代码，用.pth完全没问题，方便快捷。

但凡涉及到多人协作、部署上线、容器化，就应该用标准的包安装方式。因为这不是你一个人的事，需要保证团队里任何人拿到代码都能正常运行。

.pth是个人配置，`pip install -e .`是项目标准。前者只在你的机器上生效，后者在任何机器上都能复现。

最关键的是：这两者的使用体验几乎一样，从开发到生产只需要把`-e`参数去掉，为什么不用更规范的方式呢？