import{d as h,o as u,c as r,e as o,j as y,a as c,u as x,k as d,l as n,E as g,M as b}from"./index-uH07H8hv.js";const l={class:"about"},w=o("h1",null,null,-1),E=`
[![Python](https://img.shields.io/badge/Python-3-blue.svg)](https://www.python.org/)
[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/xaoyaoo/pywxdump)](https://github.com/xaoyaoo/PyWxDump)
[![GitHub all releases](https://img.shields.io/github/downloads/xaoyaoo/pywxdump/total)](https://github.com/xaoyaoo/PyWxDump)
[![GitHub stars](https://img.shields.io/github/stars/xaoyaoo/PyWxDump.svg)](https://github.com/xaoyaoo/PyWxDump)
[![GitHub forks](https://img.shields.io/github/forks/xaoyaoo/PyWxDump.svg)](https://github.com/xaoyaoo/PyWxDump/fork)
[![GitHub issues](https://img.shields.io/github/issues/xaoyaoo/PyWxDump)](https://github.com/xaoyaoo/PyWxDump/issues)

[![PyPI](https://img.shields.io/pypi/v/pywxdump)](https://pypi.org/project/pywxdump/)
[![Wheel](https://img.shields.io/pypi/wheel/pywxdump)](https://pypi.org/project/pywxdump/)
[![PyPI-Downloads](https://img.shields.io/pypi/dm/pywxdump)](https://pypistats.org/packages/pywxdump)
[![GitHub license](https://img.shields.io/pypi/l/pywxdump)](https://github.com/xaoyaoo/PyWxDump/blob/master/LICENSE)

* 欢迎大家提供更多的想法，或者提供代码，一起完善这个项目。

### 如果是小白，请关注公众号：\`逍遥之芯\`(下方二维码)，回复：\`PyWxDump\` 获取图文教程。

### 如有问题，请先查看：[FAQ](https://github.com/xaoyaoo/PyWxDump/tree/master/doc/FAQ.md) 是否有答案，或者关注公众号回复: \`FAQ\`。

qq交流群：[276392799](https://s.xaoyo.top/gOLUDl) or [276392799](https://s.xaoyo.top/bgNcRa)（进群密码，请查看[UserGuide.md](https://github.com/xaoyaoo/PyWxDump/tree/master/doc/UserGuide.md)）.


# 一、项目介绍

## 1. 项目简介

[PyWxDump](https://github.com/xaoyaoo/PyWxDump)是一款用于获取账号信息(昵称/账号/手机/邮箱/数据库密钥)、解密数据库、查看聊天记录、备份导出聊天记录为html的工具。

* <strong><big>
  超级想要star，走过路过，帮忙点个[![Star](https://img.shields.io/github/stars/xaoyaoo/PyWxDump.svg?style=social&label=Star)](https://github.com/xaoyaoo/PyWxDump/)
  呗，谢谢啦~</big></strong>

## 2. 功能介绍

#### 2.1 核心功能

* （1）获取微信昵称、微信账号、微信手机号、微信邮箱、微信KEY的**基址偏移**
* （2）获取当前登录微信的微信昵称、微信账号、微信手机号、微信邮箱、微信KEY、微信原始ID（wxid_******）、微信文件夹路径
* （3）根据key解密微信数据库
* （4）合并多种类型数据库，方便统一查看

#### 2.2 扩展功能

* （1）通过web查看聊天记录
* （2）支持导出聊天记录为html、csv,备份微信聊天记录
* （3）远程查看微信聊天记录（必须网络可达，例如局域网）

#### 2.3 文档类

* （1）提供数据库部分字段说明
* （2）提供CE获取基址偏移方法
* （3）提供MAC数据库解密方法

#### 2.4 其他功能

* （1）增加极简版pywxdumpmini，只提供获取数据库密钥以及数据库位置的功能
* （2）支持微信多开场景，获取多用户信息等

**利用场景**

1. 网络安全……
2. 日常备份存档
3. 远程查看聊天记录(通过web查看聊天记录)
4. 等等...............

## 3. 更新计划

* 1.每个人聊天记录分析，生成词云。
* 2.分析每个人每天的聊天数量，生成折线图（天-聊天数量）
* 3.分析不同的人的月聊天数量，年聊天数量，生成折线图
* 4.生成年度可视化报告
* 5.创建GUI图形界面，方便使用（完成部分功能）
* 8.增加企业微信的支持
* 9.增加获取实时聊天记录的功能
* 10.增加好友的信息获取（增加好友信息获取api）
* 11.备份后的聊天记录，恢复到微信中
* 12.朋友圈的查看与备份
* 13.微信存储空间清理，减少微信占用空间
* 14.通过UI控制，自动给指定人发送消息

## 4. 其他

[PyWxDump](https://github.com/xaoyaoo/PyWxDump)是[SharpWxDump](https://github.com/AdminTest0/SharpWxDump)的经过重构的python语言版本，同时添加了很多新的功能。

* 项目地址：https://github.com/xaoyaoo/PyWxDump
* 目前只在windows下测试过，mac、linux下可能会存在问题。
* 如发现[WX_OFFS.json](https://github.com/xaoyaoo/PyWxDump/tree/master/pywxdump/WX_OFFS.json)缺失或错误、bug，有改进意见、想要新增功能, 请提交[issues](https://github.com/xaoyaoo/PyWxDump/issues).
* 常见问题请参考[FAQ](https://github.com/xaoyaoo/PyWxDump/tree/master/doc/FAQ.md)，更新日志请参考[CHANGELOG](https://github.com/xaoyaoo/PyWxDump/tree/master/doc/CHANGELOG.md)
* Web UI的仓库位置 [wxdump_web](https://github.com/xaoyaoo/wxdump_web)
* 如果对wxdump实现原理感兴趣，请关注公众号：\`逍遥之芯\`，回复：\`原理\` 获取原理解析。

* [:sparkling_heart: Support Me](https://github.com/xaoyaoo/xaoyaoo/blob/main/donate.md)

## 5. Star History

[![Star History Chart](https://api.star-history.com/svg?repos=xaoyaoo/pywxdump&type=Date)](https://star-history.com/#xaoyaoo/pywxdump&Date)

# 二、使用说明

* 详细使用说明见 [UserGuide.md](https://github.com/xaoyaoo/PyWxDump/tree/master/doc/UserGuide.md)

* 极简版使用说明见 [pywxdumpmini](https://github.com/xaoyaoo/pywxdumpmini)

* 如果想修改UI，请clone [wx_dump_web](https://github.com/xaoyaoo/wxdump_web) 项目，然后按需修改（该UI采用VUE+ElementUI开发）

【注】:

* 关于基址使用cheat engine获取，参考[CE获取基址.md](https://github.com/xaoyaoo/PyWxDump/tree/master/doc/CE获取基址.md)
  （该方法可用\`wxdump bias\`命令代替，现仅用作学习原理）
* 关于数据库解析，参考[wx数据库简述.md](https://github.com/xaoyaoo/PyWxDump/tree/master/doc/wx数据库简述.md)

# 三、免责声明（非常重要！！！！！！！）

* 本项目仅供学习交流使用，请勿用于非法用途，否则后果自负。

* 您应该在下载保存，编译使用本项目的24小时内，删除本项目的源代码和（编译出的）程序。

* 本项目仅允许在授权情况下对数据库进行备份，严禁用于非法目的，否则自行承担所有相关责任。

* 下载、保存、进一步浏览源代码或者下载安装、编译使用本程序，表示你同意本警告，并承诺遵守它;

* 请勿利用本项目的相关技术从事非法测试，如因此产生的一切不良后果与项目作者无关。

# 四、致谢

[![PyWxDump 贡献者](https://contrib.rocks/image?repo=xaoyaoo/PyWxDump)](https://github.com/xaoyaoo/PyWxDump/graphs/contributors)[![UI 贡献者](https://contrib.rocks/image?repo=xaoyaoo/wxdump_web)](https://github.com/xaoyaoo/wxdump_web/graphs/contributors)

# 五、License

MIT License

Copyright (c) 2023 xaoyaoo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

PyWxDump is hosted at: https://github.com/xaoyaoo/PyWxDump

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
`,W=h({__name:"AboutView",setup(D){const e=async()=>{try{const t=await d.post("/api/check_update"),s=t.latest_version,a=t.msg,i=t.latest_url,p=`${a}：${s} 
 ${i||""}`;g.alert(p,"info",{confirmButtonText:"确认",callback:m=>{n({type:"info",message:`action: ${m}`})}})}catch{return[]}};return(t,s)=>(u(),r("div",l,[o("h1",{id:"-center-pywxdump-center-",style:{"text-align":"center"}},[y(" PyWxDump"),o("a",{onClick:e,target:"_blank",style:{float:"right","margin-right":"30px"}},"检查更新")]),w,c(x(b),{source:E})]))}});export{W as default};
