# cogujie
蘑菇街（http://mogujie.com）  图片采集工具

##description
cogujie 用于采集蘑菇街的商品图片和一些参数信息，有三种采集方式：

- 采集单个商品的商品图片
- 给定门类和子门类信息，采集子门类下所有商品的商品图片及信息（如 http://www.mogujie.com/book/neiyi/50041 为内衣门类下的运动内衣子门类） 
- 给定文件，采集文件中指定的所有子门类下的商品信息

cogujie提供了配置文件 ```./config.py```, 可以在配置文件中对一些列参数进行配置，如线程数，存放路径等
如上文所述，cogujie使用多线程，保证了采集的性能

##data
对于每一个将要采集的商品，cogujie采集该商品的展示图片及商品的一些参数信息

如 http://shop.mogujie.com/detail/17ocxes 这条糖果色超萌卡通表情内裤（笑）

cogujie将采集*商品详情*下的所有商品图片，并保存产品参数下的信息

可在配置文件中，设置path['db']来设置采集下来的数据所保存的路径，默认为```./mogujie.db```中

该目录的结构如下：

```
mogujie.db
├── neiyi_50041
│   └── 17ocxes
│       ├── imgs
│       │   ├── 17ocxes_baipai_img2_1.jpg
│       │   ├── 17ocxes_baipai_img2_2.jpg
│       │   ├── 17ocxes_baipai_img2_3.jpg
│       │   ├── 17ocxes_detail_img_4.jpg
│       │   └── 17ocxes_model_img_0.jpg
│       └── info
├── not_specified
│   └── 17ocxes
│       ├── imgs
│       │   ├── 17ocxes_baipai_img2_1.jpg
│       │   ├── 17ocxes_baipai_img2_2.jpg
│       │   ├── 17ocxes_baipai_img2_3.jpg
│       │   ├── 17ocxes_detail_img_4.jpg
│       │   └── 17ocxes_model_img_0.jpg
│       └── info
├── skirt_50099
│   └── 180ohb6
│       ├── imgs
│       │   ├── 180ohb6_model_img_0.jpg
│       │   ├── 180ohb6_model_img_1.jpg
│       └── info
└── t.placeholder
```

其中，```t.placeholder```为占位文件，无实际意义

```neiyi_50041``` 代表 ```neiyi``` 门类下的子门类 ```50041``` 子门类的商品数据存放位置

没有提供门类信息的数据存放在```not_specified```目录下

```17ocxes```是商品的tradeItemId, 该商品的所有信息存储在该目录下

对于每个商品

```info``` 文件中存储商品的一系列信息

```
    内衣
    17ocxes
    糖果色超萌卡通表情内裤

    内裤款型：三角裤 
    腰型：中腰 
    内裤材质：彩棉 
    内裤功能：星期裤 
    款式细节：印花

    model_img: 穿着效果
    baipai_img2: 整体款式
    detail_img: 细节做工
```

前三行分别为商品门类名称、商品tradeItemId和商品名称

然后是商品的属性信息

最后的字段代表图片的种类，商品的图片分为若干类，在命名时使用了这些分类名称，类别和对应的名称记录在info中

```imgs``` 下存放所有的图片文件

##usage:
使用方法请输入 ```python console.py -h``` 或者 ```python console.py --help```查看
