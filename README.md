[TOC]
# DIY一个代码质量管理平台
> 这不是一篇技术文章，所以请不要把她当成技术文章来读。只是想表达一个开发人员对美好生活的憧憬。  

## 背景
代码质量，衡量开发人员成果物的重要标准。那么，作为开发人员如何能交付高质量代码呢？不好意思，我也不知道正确答案:(。不过，我们代码要经过，"静态扫描、动态扫描、单元测试、集成测试、系统测试、性能测试……"，一系列的流程，我想这点大家应该是认同的。  
我们再具体一点，一个开发人员从编码到交付集成测试至少需要经过，静态扫描、单元测试、动态扫描，并提供各阶段的成果物。各阶段成果物包括：静态检查结果、动态检查结果、单元测试代码、单元测试结果、单元测试覆盖率等等。  
如此多的交付内容，是否有统一的规范、格式以及审核流程呢？根据各个项目具体要求这部分流程一定会有，但形式可能会有所不同，大多可能是以文本或表格的形式存在。但不管以哪种形式都不够直观(*如果是直接看各种检查工具的命令行输出，我想一定会有头晕、眼花等不同程度的生理反应:(*)，我们总是期待我们世界会变得更加美好。  
那么……，好吧……，让我们回到主题，《DIY一个代码质量管理平台》。  

## 原材料
> —— 君子生非异也，善假于物也。  
> 人类社会的飞速发展主要仰仗于对已有资源、工具，经验的利用和改造，不断创造新的资源、新的工具并积累更多的宝贵经验，并把她们不断的传承下去。  
> 所谓原材料本质上也是一系列的工具，把它们定位成原材料是因为要对它们的输出结果进行再加工。  

开始动手前，让我们先了解一下原材料需要哪些，当然，所有的原材料都是免费的，所以不用太多考虑成本。  

原材料清单如下：

### 静态检查(Cppcheck)  

先看看市面上C/C++静态检查的原材料都有哪些？PC-Lint/FlexeLint、Splint、Cppcheck。  
1.PC-Lint/FlexeLint：功能很强大。但是是商用的，要钱。  
2.Splint：不要钱，但只适用于C。  
3.Cppcheck：不要钱，C++可以用，而且可以和  jenkins集成，也可以和许多IDE进行集成(Eclipse，Codeblock，VS)。  
·Cppcheck放进购物车`。  

### 动态检查(valgrind)
动态检查材料选择起来就比较简单了，个人认为`valgrind`是功能最强大的，开源的动态检查工具，没有之一。有不同见解的小伙伴可以交流一下(*其实我是想说，不服来辩*)。  
`valgrind`不是一个工具，它是一个工具集，包括以下工具包： 

*Callgrind*：它主要用来检查程序中函数调用过程中出现的问题。  
*Cachegrind*：它主要用来检查程序中缓存使用出现的问题。  
*Helgrind*：它主要用来检查多线程程序中出现的竞争问题。  
*Massif*：它主要用来检查程序中堆栈使用中出现的问题。  
*Extension*：可以利用core提供的功能，自己编写特定的内存调试工具  

`valgrind添加到购物车`。  
**PS. `kachegrind`这货不错，感兴趣的可以试试。**  

### 单元测试(cppunit)
选单元测试材料就有点郁闷了，我的首选是`gtest`，但由于要传承之前项目积累的成果，所以，退而求其次，`cppunit进入了购物车，gtest暂时收藏`。    
本质上没有太大差别，但setup()/teardown()，选择性执行用例，包括打桩，gtest的优势还是比较明显的。

### 代码覆盖率(gcovr/lcov)
这个也没有必要多说，可选择的不多。我们主要是用lcov，没有别的原因，界面友好，几乎不需要做加工。  
再推荐一个gcovr，是python写的C/C++的覆盖率统计工具，效果和lcov差不多，可以考虑用gcovr来代替lcov，原因是lcov对so的支持不好，恰巧，我们项目使用了大量的so。必要时更换原材料。  
`lcov加入购物车，gcovr添加收藏`。

## 工具
> —— 工欲善其事必先利其器。  
原材料准备好了，找几个能加工这些材料的工具。这块不多说，工具太多，找几个顺手来用就可以了。  

先选两瓶胶水(语言)；shell，python  
再来一个能放在口袋里的数据库：sqlite  
找个盒子把我们作品装起来：Django/Beego  
最后弄个漂亮点的包装：bootstrap，jQuery，jqplot  

## 开始动手
> 东北有句话，“能动手的，就尽量少说话。”  
我们的目标是用最短的时间，最简单的方法，实现一个实用的界面友好日常工具。  
好吧……，尽量少说话！开工！！！  

### 第一步 初加工
> 所谓初加工就是利用原材料自带的属性，通过参数，命令行选项得到我们想好的半成品。

#### 导出cppcheck检查结果
```
cppcheck --enable=all --xml you_code_dir 2 > check.xml
```
以xml格式保存静态检查结果。
#### 导出valgrind检查结果
```
valgrind --tool=memcheck --leak-check-full --xml=yes --xml-file=valgrind.xml
```
以xml格式保存动态检查结果。
#### 导出单元测试结果
上面说了，cppunit没有gtest那么好用了。需要改代码才能输出我们想要的结果。
```
std::ofstream xmlFileOut("unit.xml");
CppUnit::XmlOutputter xmlOut(&result, xmlFileOut);
```
#### 统计代码覆盖率

```
# 先要加两个编译选项
-fprofile-arcs -ftest-coverage

# 再链一个库
-lgcov
```
编译执行后导出结果，直接用lcov
```
lcov -c -o cov.info -d ${.gcno .gcda目录} -b ${源代码目录}

# 生成html
genhtml cov.info -o cov_html
```

至此，我们需要的静态扫描，动态扫描，单元测试，测试覆盖率的半成品结果都有了。

### 第二步 深加工
> —— 言治骨角者，既切之而复磋之；治玉石者，既琢之而复磨之；治之已精，而益求其精也。

那么，我们对上面的半成品再切磋琢磨一番。

#### 数据入库
个人习惯是把有规律的数据放到数据库里面，一是归类保存方便，二是用sql查找要比grep更实用。如果有相应的客户端，那么你还会有个友好的操作界面。  
处了代码覆盖率是html，先不管它。其它都是xml。 
 
拿出一瓶标签是python胶水，把xml粘到sqlit上。  

    
```
#!/usr/bin/python
#coding=utf8
"""
# Author: frank
# Created Time : 2017-08-26 14:46:49

# File Name: import_cppcheck.py
# Description:

"""

from xml.dom.minidom import parse
import sqlite3
import os
import sys, getopt

def help():
    print '''usage:
    -h help
    -f cppcheck result file *.xml_file
    -d import sqlite3 db file *.db'''
    sys.exit(1)

opts, args = getopt.getopt(sys.argv[1:], "hf:d:")

xml_file = ''
db_file = ''

for op, value in opts:
    if op == "-f":
        xml_file = value
    elif op == "-d":
        db_file = value
    elif op == "-h":
        help()

if xml_file == '' or db_file == '':
    help()

# if os.path.exists(db_file):
#     os.remove(db_file)

conn = sqlite3.connect(db_file)
c = conn.cursor()

c.execute('''CREATE TABLE CPPCHECK_RESULT 
        (ID INT PRIMARY KEY     NOT NULL,
        FILE           TEXT,     
        LINE           INT, 
        TYPE           TEXT     NOT NULL,
        SEVERITY       TEXT     NOT NULL,
        MSG            TEXT     NOT NULL);
        ''')

id = 0
#打开xml文件
dom = parse(xml_file)

results = dom.documentElement
errors = results.getElementsByTagName("error")
for error in errors:
    id = id + 1
    if error.getAttribute("file"):
        f_file = error.getAttribute("file")
    else:
        f_file = ''

    if error.getAttribute("line"):
        f_line = error.getAttribute("line")
    else:
        f_line = 0
    c.execute ('''INSERT INTO CPPCHECK_RESULT (ID,FILE,LINE,TYPE,SEVERITY,MSG)  
VALUES (''' + str(id) + ''',"''' + f_file + '''",''' +  str(f_line) + ''',"''' + error.getAttribute("id") + '''","''' +  error.getAttribute("severity") + '''","''' +  error.getAttribute("msg") + '''");''')


conn.commit()
conn.close()
```
很容易，去掉注释也就50~60行。这个是将cppcheck结果导入sqlite的代码。另外两个xml的导入，如法炮制。稍微调整一下表结构，分分钟就可以搞定。  
但有人会问，为啥分开写呢？一个脚本把3个xml都读到sqlite不行吗？分开写，可以分开用。拿出来也是个单独的工具。  
那么，问题来了，分开写调用的时候就需要调用3次，多麻烦！好吧，拿出另一瓶标签是shell的胶水。
```
#########################################################################
# File Name: import.sh
# Author: Frank
# mail: frank.x@aliyun.com
# Created Time: 2017-08-26 21:51:15
#########################################################################
#!/bin/bash

set -e

function help()
{
    echo "usage:
    -h help
    -c cppcheck result file *.xml
    -u cppunit result file *.xml
    -v valgrind result file *.xml
    -d import sqlite3 db file *.db"
}

while getopts "c:u:v:d:h" arg
do
    case $arg in
        c)
        check_file=$OPTARG
        ;;
        u)
        unit_file=$OPTARG
        ;;
        v)
        valgrind_file=$OPTARG
        ;;
        d)
        db_file=$OPTARG
        ;;
        h)
        help
        exit 1
        ;;
        ?)
        help
        exit 1
        ;;
    esac
done


if  [ ! -n "$check_file" -o ! -n "$unit_file" -o ! -n "$valgrind_file" -o ! -n "$db_file" ] ;then
    help
    exit 1
fi

rm -rf $db_file


python import_cppcheck.py -f $check_file -d $db_file
python import_cppunit.py -f $unit_file -d $db_file
python import_valgrind.py -f $valgrind_file -d $db_file
```
粘上了，一个脚本搞定。

#### 展示结果  

把各种检查结果写到sqlite不是最终目的，要把它展示出来。  
既简单又快的方式，B/S结构是首选。做这种小东西其实php是最佳选择，因为*“php是世界上最好的编程语言”*，^-^这个段子大家应该听过。用php的一个小问题就是部署稍稍有一点点麻烦(*其实已经很简单了，但有更简单的，我们一定不用简单的，这个是大原则！*)，虽然httpd服务linux默认安装了，但还免不了一些配置。
  
好吧……，再见php！那用啥呢？Django，nodejs还是beego，部署简单，不需要服务器，你想要的脚手架功能它们都有。  
我先选了了Django，必要时还可以把sqlite这层去掉，直接python解析xml然后展示，看上去不错！

说干就干。
```
pip install django -g
```
看似简单的命令，但在向内网迁移的时候……，一万头XXX在我胸口奔腾而过。(XXX这玩意儿学名叫羊驼)，各种包依赖，各种包版本问题，一个一个下载，一个一个手动安装。本来是一根网线加一条pip命令可以解决的问题，结果鼓捣了一个多小时。  
好吧……，不带你玩了！有这时间都搞完了~~  

稳妥点，不需要迁移，外网搞完了直接可以拿到内网用，妥妥的用Go，直接发布二进制可执行文件总行了吧。  

说干就干。尽量少说话，直接上图吧。  

![](leanote://file/getImage?fileId=59bf5eedab644106950013fa)

代码覆盖率展示方面，lcov做了我们想要的一切，不做任何修改，直接拿来用。在Beego里面直接设置其静态目录为lcov导出html的文件夹目录。
```
beego.SetStaticPath("/datas/cov_html","lcov")
```

---
![](leanote://file/getImage?fileId=59bf5eedab644106950013f8)

和Django，nodejs一样Beego做这上面的事情简单得令人发指。只需以下步骤：  
1. 写个router指定跳转的url与controler的关联
2. 利用自带的orm，将表映射为Go的struct，并写一些简单的查询，完成model
3. 通过controler调用model，处理数据，并在view中展示。
4. 编写view，静态html加上template，将数据进行展示。  
典型的MVC架构(*这里不讲技术，况且我现在是个C++程序员:)*)。

至此，数据展示部分完成。*“太low了吧，这玩意儿用你做？弄个sqlite客户端就完了呗。”*  
好吧……，你说的对。但我们总是向往更加美好的世界……。

### 包装
> 上面工序完成后几乎和Excel没啥区别，那就让它更像一个工具吧。对它进行包装。

可能看到这大家会有个疑问，如果只是展示，那为什么要把数据存到sqlite里面，直接用xml一样可以实现web展示功能。没错，但我并不想只是单纯的展示，对这些数据指标进行分析是终极目标之一。  
先来几个我们关心的指标吧：  
- 静态检查问题数
- 静态检查问题分布情况
- 测试用例失败数
- 测试通过率
- 代码覆盖率
- 动态检查问题数
这些东西很容易搞定，因为有sql:)。  

数据方面利用数据库能够很方便的进行统计分析。如果有新的指标要统计，只要sqlite里面有数据源，也是很容易实现的。  

另一个层面的包装就是美工了，这个我不专业，但js还是略知一二。其实不知道也没关系，现成的东西一抓一大把，拿来就用，我们的原则是有现成的就对不去造轮子。

bootstrap，jqplot……，拿来就用。  
尽量少说话，上图~

![](leanote://file/getImage?fileId=59bf5eedab644106950013f7)

至此，产品功能基本完成。

### 装箱
> 收工前还有一个重要的事情，装箱发布。前面一直在提“拿来就用”这个词，别人的东西我们拿来直接用，同样，我们的东西要让别人也能够方便的“拿去就用”。那么我们完成最后一道工序，装箱发布。 

了解Beego的同学一定都知道Bee这个工具，她提供了一些非常方便的工具，其中一个就是打包。  
在你的工程目录下执行  
```
bee pack
```
她会打包生成一个压缩包，包括可执行文件、配置文件、静态文件和自定义文件/文件夹，解压后直接可以运行。  
另外，`bee bale`命令可以将所有的静态文件变成一个变量申明文件，全部编译到二进制文件里面，用户发布的时候携带静态文件(*该命令尚未正式发布*)。  
你会发现，世界真的是很美好，有如此多的工具可供我们是用，一条命令，分分钟搞定。  

另外一件事就是写个一键脚本。看看脚本内容包括啥(*这里不贴代码了，因为所有命令，上文已经提到，剩下的就是写上你的目录*)？  
1. 静态检查，指定生成xml到指定目录
2. 编译程序(*确定把上面说的两个选项和lgcov库链上*)
3. valgrind 执行测试用例，指定单元测试结果xml的目录，指定valgrind结果文件目录。
4. 执行xml导入sqlite的脚本，指定sqlite输出目录。
5. 执行ut_frame。
6. 休息一下，泡杯茶。
7. 打开浏览器，看看我们这次提交的质量吧。  

至此，里程。

### 演进路线
v0.1 完成基本功能。  
v0.2 兼容gcovr，以便支持对so覆盖率的统计。  
v0.3 点击静态/动态检查问题记录，可以定位到源代码文件。  
v0.5 支持更多的统计指标。  
v0.7 支持多次检查的数据结果对比，分析质量提升项。  
v1.0 目标是以插件形式接入ITAS系统(*作为ITAS前期开发人员，再贡献一点余热*)


谁用谁拿，随用随拿。

## 尾声
“更加美好的世界”是我们的向往。“拿来主义”是我们的原则。花几个小时会让你的世界变得更加美好(*惭愧的是写下上面的文字似乎用去了我更长的时间，所以请小编手下留情，酌情删减，打字不易啊~~*)。  

最后以一段鲁迅先生的话作为结束吧，先生说：”总之，我们要拿来。我们要或使用，或存放，或毁灭。那么，主人是新主人，宅子也就会成为新宅子。然而首先要这人沉着，勇猛，有辨别，不自私。没有拿来的，人不能自成为新人，没有拿来的，文艺不能自成为新文艺“。

## 参考文献
1. 《荀子·劝学》
2. 《论语·卫灵公》
3. 《拿来主义》
