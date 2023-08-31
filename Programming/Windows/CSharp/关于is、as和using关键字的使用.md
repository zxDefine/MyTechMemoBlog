# C#中is、as和using关键字的使用
本文直接复制CSDN作者tongyuehong的文章,这里只作为笔记记载,[原文出处](https://blog.csdn.net/tongyuehong137/article/details/51395298).

## 问题描述
在C#中is,as,using关键字具有其特点及使用场景.
* **is**关键字用于检查该对象是否与给定类型兼容
* **as**关键字用于将对象转换为指定类型
* **using**关键字除了用于引入命名空间之外,还具有回收对象资源,如文件资源、网络资源和数据库资源等。

### is
用于检查对象是否与给定类型兼容,如果兼容,则返回true,否则返回false,不会抛出异常。在进行类型转换之前,可以先用is判断对象是否与给定类型兼容,如果兼容再进行转换。
```cs
string str ="test";  
object obj = str;
if(obj is string)  {string str2 = (string)obj};
```
### as
用于引用类型之间转换,直接进行转换,若转换成功,则返回转换后的对象,若转换失败返回null,不抛出异常。
```cs
string str ="test";  
object obj = str;
string str2 = obj as tring;
if(str2 !=null) {转换成功}
```
### using
引用命名空间,有效回收资源,using关键字可以回收多个对象的资源,**关键字后面的小括号内创建的对象必须实现IDisposable接口,或者该类的基类已经实现了IDisposable接口**。回收资源的时机是在using关键字下面的代码块执行完成之后自动调用**接口方法Dispose** 销毁对象。
```cs
using (Test test =new Test()) { 各种操作;}
calss Test :IDisposable {
   public void Dispose() {回收操作;}
}
```

## 代码示例
```cs
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;
 
namespace test1
{
    public partial class Form9 : Form
    {
        public Form9()
        {
            InitializeComponent();
        }
 
        private void button1_Click(object sender, EventArgs e)
        {
            //转为object
            if (obj_rdb.Checked)
            {
                //使用using关键字,在代码块执行完成之后自动回收资源
                //由于FileStream已经实现了IDisposable接口,可以直接使用
                using (FileStream fileStream = new FileStream(@"d:\test.txt", System.IO.FileMode.Create))
                {
                    object obj = fileStream as object;   //直接使用as转换
                    if (obj != null)
                    {
                        MessageBox.Show("FileStream转换为object成功", "提示信息");
                    }
                    else
                    {
                        MessageBox.Show("FileStream转换为object失败", "错误信息");
                    }
                }
            }
            else
            {
                using (FileStream fileStream = new FileStream(@"d:\test.txt", System.IO.FileMode.Create))
                {
                     //直接强制转换
                    try
                    {
                        Stream stream = (Stream)fileStream;
                        MessageBox.Show("FileStream转换为Stream成功", "提示信息");
                    }catch(Exception ex)
                    {
                        MessageBox.Show(ex.Message, "错误信息");
                    }
                    
                }
            }
            
        }
    }
}
```