## Scrapy 爬虫调试方法

### Parse命令

检查spider输出的基本方法使用Parse命令。可以检查spider各个部分的效果。

查看特定url爬取到的item，命令格式为 

scrapy parse --spider=  \<spidername>  -c \<parse item> -d 2 \<item url>

可以配合使用--verbose或-v选项，可以查看各个层次的详细状态。

### Scrapy shell

Parse除了显示收到的response及输出外，其对检查回调函数内部的过程并没有提供便利，这个时候可以通过scrapy.shell.inspect_response方法来查看spider的某个位置中被处理的response，以确认期望的response是是否达到特定的位置。

可以在parse方法里添加两句代码：

```c++
from scrapy.shell import inspect_response
inspect_response(response, self)
```

当程序运行到inspect response方法时会暂停，并切换进shell中，可以方便我们对当前的response进行调试

### logging

logging是另一个获取spider运行消息的方法。日志可以在以后的运行中页可以看到。