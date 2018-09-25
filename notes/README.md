## Scrapy爬虫

#### 架构

<center>
    <img src=""/>
</center>

#### 工作流程

1. 引擎打开一个网站，找到处理该网站的Spider并向该Spider请求第一个要爬取的URL
2. 引擎从Spider中获取到一个要爬取的URL并通过调度器（Scheduler）以Request进行调度
3. 引擎向调度器请求下一个要爬取的URL
4. 调度器返回下一个要爬取的URL给引擎，引擎将URL通过下载中间件转发给下载器（Downloader）
5. 一旦页面下载完毕，下载器生成一个该页面的Respongse，并将其通过下载中间件发送给引擎
6. 引擎从下载器中接收到Response并通过Spider中间件发送给Spider处理。
7. Spider处理Response并返回爬取到的Item及（跟进的）新的Request给引擎。
8. 引擎将（Spider返回的）爬取到的Item给Item Pipeline，将（Spider返回的）Request给调度器。
9. （从第二步）重复直到调度器中没有更多的Request，引擎关闭该网站。

接下来是构建一个简单的爬虫项目，它主要工作在Spider模块。

#### 创建爬虫项目

```python
scrapy startproject blogSpider
```

创建后目录如下：

```c++
blogSpider
	| scrapy.cfg
	| 
	|——blogSpider
		|	items.py
		|	pipelines.py
		|	settings.py
		|	__init__.py
		|
		|——spiders
			|	__init__.py
```

- scrapy.cfg：项目部署文件
- blogSpider/: 该项目的python模块
- blogSpider/items.py： 项目中的Item文件
- blogSpider/pipelines.py： 项目中Pipelines文件
- blogSpider/settings.py：项目中配置文件
- blogSpider/spiders/：放置Spider代码的目录

#### 构建爬虫模块

```
首先编写爬虫模块。爬虫模块的代码放置在Spider文件中。爬虫模块是用于从单个网站或者多个网站爬取数据的类，其应该包含初始页面URL，以及跟进网页链、分析页面内容和提取函数。构建一个Spider类，需要继承scrapy.Spider类，并且定义三个属性：
```

- name：spider标识
- start_urls：spider启动时是入口Url列表
- parse()：负责解析返回的数据(response data)、提取数据（生成item）以及生成需要进一步处理的URL的request对象。

```python
import scrapy
class blogSpider(scrapy.Spider):
	name = "blog"
	allowed_domains = ["com"] #允许的域名
	start_urls = [
		"https://www.github.com"
	]
	def parse(self, response):
		#实现网页解析功能
		pass
```

#### 选择器（Selector）

是Scrapy上的数据提取机制，通过特定的XPath或者CSS选择器来选择html文件中的某一部分。选择器用来对返回的响应进行解析。

用法：

- xpath(query)：传入XPath表达式
- css（query)：传入CSS表达式
- extract()：序列化该节点为Unicode字符串并返回list列表
- re(regex)：传入正则表达式



#### 定义Item

爬取的主要目标是从非结构性的数据源提取结构性数据。scrapy提供Item类来存储爬取的数据。Item对象是一种简单的容器，用来保存爬取到的数据，提供类似与词典的API以及用于声明可用字段的简单语法。Item使用简单的class定义语法以及Field对象来声明；

```python
class blogspiderItem(scrapy.Item):
	# define the fields for your item here like:
	url = scrapy.Field()
	time = scrapy.Field()
	title = scrapy.Field()
```

用法：

- 创建blogspiderItem对象

  item = blogspiderItem(title="python爬虫"， content='爬虫开发')

- 获取字段的值

  print item['title']

- 设置字段的值

  item['title'] = "爬虫"

- dict与item的转化

  dict_item = dict(item)

### 构建Item Pipeline

Item Pipeline用于数据的持久化存储。当Item在Spider中被手机之后，它将会被传递到Item Pipeline，一些组建会按照一定的顺序执行对Item的处理

- 清理HTML数据
- 验证爬取的数据的合法性，检查Item是否包含某些字段
- 查重并丢弃
- 将爬取结构保存到文件或者数据库中

#### 定制Item Pipeline

将爬取到的Item存储到本地。

```python
import json
from scrapy.exceptions import DropItem
class blogspiderPipeline(object):
	def __init__(self):
		self.file = open('papers.json', 'wb')

	def process_item(self, item, spider):
		if item['title']:
			line = json.dumps(dict(item)) + "\n"
			self.file.write(line)
			return item
		else:
			raise DropItem("Missing title in %s" % item)
```

Spider类定义了如何爬取某个或者某些网站，包括了爬取的动作，以及如何从网页内容提取结构化数据item。Spider是定义爬取动作以及分析网页结构的地方。

Spider的爬取流程如下：

1. 以入口URL初始化Request，并设置回调函数。此Request下载完毕返回Response，并作为参数传给回调函数。
2. 在回调函数内分析Response，返回Item对象、dict、Request或者一个包含三者的可迭代容器。其中，返回的Request对象之后会经过Scrapy处理，下载相应的内容，并调用设置的回调函数，可以是parse()或者其他函数。
3. 在回调函数内，可以使用选择器或者其他第三方解析器来分析response，并根据分析的数据生成item
4. 最后，由spider返回的item可以经由Item Pipeline被存放到数据库或使用Feed export存入到文件中。

## Scrapy其他组件



### Item Loader

Item Loader提供一种便捷的方式填充爬取到的Items。虽然Items可以使用自带的类字典形式API填充，但是Items Loader提供便捷API，可以分析原始数据并对Item进行赋值。

```python
def parse(self, response):
	l = Item Loader(item=Product(), response=response)
	l.add_xpath('name', '//div[@class="product_name]')
	l.add_value('last_updated', 'today')
	return l.load_item()
```

### 输入输出处理器

Item Loader负责数据的收集、处理和填充，Item仅仅承载了数据本身而已。数据的收集、处理和填充，归功于Item Loader的两个重要组件：输入处理器和输出处理器

- Item Loader在每个字段中都包含输入处理器和输出处理器
- 输入处理器在受到response后理科通过add_xpath()、add_css()等方法提取数据，经过输入处理器的结果被收集起来并且保存在ItemLoader中。
- 收集到所有数据后，调用ItemLoader.load_item()方法来填充并返回Item对象。load_item()方法内部先调用输出处理器来处理收集到的数据，处理后将结构最终存入Item中。

```python
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join

class ProductLoader(ItemLoader):

	default_output_processor = TakeFirst()

	name_in = MapCompose(unicode.title)
	name_out = Join()
```

### 请求与响应

在编写Spider模块中接触最紧密的是请求和响应。

1. #### Request对象

   一个Request对象代表者一个HTTP请求，通常在Spider类中产生，然后传递给下载器，最后返回一个响应。

   构造参数说明：

   | 构造参数              | 说明                    |
   | --------------------- | ----------------------- |
   | url(string)           | 请求的链接              |
   | callback(callable)    | 用于解析请求响应的方法  |
   | method(string)        | HTTP请求方式，默认是get |
   | meta(dict)            | 初始化Request.meta属性  |
   | body(str or unicode)  | 请求的body              |
   | headers(dict)         | 请求头                  |
   | cookies(dict or list) | 请求的cookies信息       |
   | encoding(string)      | 请求的编码              |
   | priority(int)         | 请求的优先级            |
   | dont _filter(boolean) |                         |
   | errback(callable)     | 出现错误处理函数        |

2. Response对象

| 构造参数      | 说明                     |
| ------------- | ------------------------ |
| url(string)   | 响应的URL                |
| headers(dict) | 响应头信息               |
| status        | 响应码                   |
| body          | 响应的body               |
| meta          | 用来初始化Response.meta  |
| flags         | 用来初始化Response.flags |
|               |                          |
|               |                          |
|               |                          |

### 下载器中间件

从Scrapy的框架图可知，下载器中间件是介于Scrapy的request/response处理的钩子框架，是用于全局修改的Scrapy的request和respons，可以帮助我们定制自己的爬虫系统。

编写下载器中间件主要处理的方法是：

- process_request(request, spider)
- process_response(request, response, spider)
- process_exception(request, exception, spider)

### Spider中间件

Spider中间件是用来处理发送给Spiders的Response及Spider产生的Item和Request

编写Spider中间件需要处理的方法是：

- process_spider_input(response, spider)
- process_spider_output(response, result, spider)
- process_spider_exception(response, exception, spider)
- precess_start_requests(start_requests, spider)

### 扩展

扩展框架提供了一种机制，你可以将自定义功能绑定到Scrapy中。扩展只是正常的python类，它们会在Scrapy启动时被实例化、初始化。

定制扩展许哟啊一个入口：from_crawler类方法，它接收一个Crawler类的实例，通过这个对象可以防卫setting、signal(信号)、status(状态)，以便控制爬虫行为。通常来说，扩展需要关联到signals并执行它们触发的任务。

完整代码链接：