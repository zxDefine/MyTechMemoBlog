# UWP的多语言配置
UWP实现本地化的话,只需要提供不同的语言资源文件即可。而针对布局方式,例如阿拉伯地区阅读顺序是从右到左,需要重新适配一下,这里我最常用的语言为以下几种,并不需要重新适配布局,所以这里只记述了怎么添加多语言资源文件以及注意事项。

* 简体中文(zh-CN/zh-Hans)
* 繁体中文(zh-TW/zh-Hant)
* 日文(ja)
* 韩文(ko)
* 英文(en-US)

## 配置步骤
### 设置默认语言
首先需要设置应用的默认使用语言。这里以*英语*为默认语言设置方法。
* 在工程目录下创建**Strings**目录,然后在创建各个**语言代码**为名称的子目录。例如英语为en-US,简体中文可以是zh-Hans。
* 然后每一个语言子目录下面新建一个资源文件,Resources.resw文件。
* 然后打开Package.appxmanifest,在默认语言的选项处填写**en-US**

以上就设置好了默认语言

### 编辑资源文件
然后在**默认语言的资源文件**里面添加资源,**注意,如果是要显示在界面上的,需要根据控件的属性来设置**。例如,TextBlock的文字是Text属性,那资源的名字就命名为HelloWorld.Text,Button的文字是Content属性,所以命名为ClickMe.Content,另外在代码中使用的话不需要设置属性,例如AppName。

### 在XAML界面上使用语言资源
在XAML的Page中放一个 TextBlock,一个Button,一个ComboBox,设置其x:Uid(资源标识符,注意不是x:Name)属性,这样控件就可以根据资源找到其对应的内容。

### 在代码中使用语言资源
```cs
Windows.ApplicationModel.Resources.ResourceLoader.GetForCurrentView().GetString("AppName");
```

### 使用多语言应用包编辑器(可选)
这一步是可选的,如果不使用编辑器的话,只需要手动在其他语言的资源文件里面定义跟默认语言资源文件里面一样的资源名称跟翻译后的值即可使用。

#### 多语言应用工具包安装以及使用
参考微软的[Windows开发文档](https://docs.microsoft.com/zh-cn/windows/apps/design/globalizing/use-mat),简单步骤如下。
* 安装工具包。
* 菜单栏里面工具->Multilingual App Toolkit->启用选定内容。
* 然后在项目右键,点击Multilingual App Toolkit->添加翻译语言。
* 选择需要添加翻译的语言。
* 然后会在项目下生成MultilingualResources目录,里面是新添加的其他语言的xlf文件。
* 右键点击xlf文件,选择打开方式,选择多语言编辑器,然后可以在里面进行翻译操作。
* 编辑完成后,保存,重新编译生成一下项目,重新编译生成一下项目,多语言工具包会根据默认资源去填充其他语言的资源文件。

### 更改首语言
到这个时候,重新运行项目,如果电脑系统默认的是中文的话,那应用也会以中文界面进行显示。但是应用可以自行设置语言。
```cs
Windows.Globalization.ApplicationLanguages.PrimaryLanguageOverride = "zh-Hans";
```
使用以上方法重新设置了首语言之后,**必须重新启动应用**,才能显示。

### 多语言的三个概念
#### 用户语言列表(user profile language list)
可以使用如下接口获取,在Windows10中,实际就是设置中区域和语言里面的首选语言列表。
```cs
Windows.System.UserProfile.GlobalizationPreferences.Languages
```
#### 应用程序语言列表(App manifest language list)
开发UWP的时候,如果要支持多语言,就需要在配置文件中声明需要支持什么语言,在运行时,可以通过如下接口获取当前应用支持什么语言。
```cs
Windows.Globalization.ApplicationLanguages.ManifestLanguages
```
值得注意的是,我们要声明多种语言,可以自动声明,也可以自己手动添加。
#### 运行时语言列表(App runtime language list)
在程序运行时,可通过如下接口获取,简单来说,所谓运行时语言列表,就是 *用户语言列表* 和 *应用程序语言列表* 中两种列表的交集,可以参考[微软开发文档](https://docs.microsoft.com/en-us/windows/apps/design/globalizing/manage-language-and-region)链接。
```cs
Windows.ApplicationModel.Resources.Core.ResourceContext.GetForCurrentView().Languages;
Windows.Globalization.ApplicationLanguages.Languages;
```