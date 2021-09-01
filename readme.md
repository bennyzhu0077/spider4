## **Important！**

1. 请在登录淘宝（https://www.taobao.com）, 京东（https://www.jd.com）和1688（https://pjjx.1688.com/）之后获取到headers

2. 此框架添加了抓取京东评论数据的函数，需要在抓取数据动态页面函数get_jd_comment()的header和cookie变量与字典内容

3. 京东评价内容必须在登录之后才能查看，否则此数据正常浏览的情况下不显示在页面。数据储存在页面返回的jQuery文件中

4. 本地查看需要设置虚拟环境运行页面

5. 由于爬虫发出的流量比较大，所以服务端会经常提示超时，经过调整之后稍微减少了爬取的页数保证服务器能及时返回数据。本地端爬取数据不受超时限制，可以在以下图示的行修改爬取的页数

   ​

   ![63050199358](C:\Users\benny\AppData\Local\Temp\1630501993586.png)

   ​

   ![63050204437](C:\Users\benny\AppData\Local\Temp\1630502044371.png)

   ​

   ![63050209083](C:\Users\benny\AppData\Local\Temp\1630502090836.png)

   ​

6. 淘宝页面爬取比较敏感，所以云端服务器爬取比较容易被淘宝服务器拦截。建议爬取较多数据的时候使用本地端。



京东商品信息返回页面，右键选择拷贝curl

![63048776202](C:\Users\benny\AppData\Local\Temp\1630487762025.png)

拷贝京东的header字段，拷贝字段必须带上花括号以及里面的所有内容。1688，淘宝和京东的评价信息的cookie和header操作一样

![63048867819](C:\Users\benny\AppData\Local\Temp\1630488678191.png)

京东商品评价信息返回文件，搜索任意内容后点开商品信息，找到此文件，为JSON文件储存的字典数据，右键拷贝curl

![63048857423](C:\Users\benny\AppData\Local\Temp\1630488574239.png)

1688商品信息返回文件，为JSON文件储存的字典数据，右键拷贝curl

![63048805932](C:\Users\benny\AppData\Local\Temp\1630488059321.png)

淘宝商品信息返回文件，为JSON文件储存的字典数据，右键拷贝curl

![63048822299](C:\Users\benny\AppData\Local\Temp\1630488222990.png)



将这些粘贴到添加字段里面的对应的项目，提交后就可以使用爬虫爬取数据。

![63050160178](C:\Users\benny\AppData\Local\Temp\1630501601781.png)