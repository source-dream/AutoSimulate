# AutoSimulate

利用多线程实现的一个批量模拟的小工具。

## 使用方法

安装依赖

```shell
pip install -r requirements.txt
```

然后运行

```shell
python main.py
```

>第一次运行会自动生成配置文件

在config.py中配置好全部参数后，再次运行即可。

## 配置填写指南

### REGULAR

这个配置是Alpha表达式

{}代表datafields

案例

```python
REGULAR = "rank({})"
```

## 功能

+ [x] 多线程模拟，最快速度模拟

+ [x] 更方便的配置，简单配置即可模拟

+ [x] 保存历史记录，跳过重复的

+ [ ] 预计耗时，显示剩余模拟时间

+ [ ] 自动筛选，自动筛选最优质的

+ [ ] 优化进度显示，可视化显示

+ [ ] 连续模拟，可同时设置多个公式

+ [ ] 接续模拟，可在不停止程序的情况下新增模拟任务

+ [ ] 配置升级，支持升级配置，无需重写

## 其他资源链接

链接：https://pan.baidu.com/s/1DFQkbilZnephkZ715i2gGg?pwd=bibr 
提取码：bibr 

## 问题反馈

![](https://cdn.sourcedream.cn/image/wechatInvite.jpg)