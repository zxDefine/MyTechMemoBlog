# UWP访问ApplicationData方法
在UWP开发的过程中会有许多生成的数据文件,这些文件保存在什么地方,可以根据数据文件的性质来选择。

## UWP访问PC端的几种方式
#### [ApplicationData](https://docs.microsoft.com/en-us/uwp/api/windows.storage.applicationdata?wt.mc_id=MVP&view=winrt-20348)
> 提供对应用程序数据存储的访问。 应用程序数据由本地、漫游或临时的文件和设置组成。
#### [Package.InstalledLocation](https://docs.microsoft.com/en-us/uwp/api/windows.applicationmodel.package.installedlocation?view=winrt-20348#Windows_ApplicationModel_Package_InstalledLocation?wt.mc_id=MVP)
> 获取当前包在当前包的原始安装文件夹中的路径。
#### [AppDataPaths](https://docs.microsoft.com/en-us/uwp/api/windows.storage.appdatapaths?wt.mc_id=MVP&view=winrt-20348)
> AppDataPaths 根据 KNOWNFOLDERID 命名模式返回常用应用程序文件夹的路径。可以获取到照片、图片、音乐、视频等文件夹。

## 关于访问ApplicationData
ApplicationData 提供应用程序自己创建的数据的读写能力。它包含这些文件夹: 
* Local: 储存在设备上,可被云端备份,在更新之后此数据保留
* LocalCache: 储存在当前设备上,不备份,在更新后此数据保留
* SharedLocal: 储存在设备上,为所有用户共享
* Roaming: 对于同一个用户,会存在于安装了此应用的所用设备中
* Temporary: 允许操作系统在任何时刻删除的临时文件

#### 代码示例
```C#
private async void button_Click(object sender, RoutedEventArgs e)
{
	int testStr = "the test file";
	string json = JsonConvert.SerializeObject(testStr);
	var file = await ApplicationData.Current.RoamingFolder.CreateFileAsync("TestFile.json");
	await FileIO.WriteTextAsync(file, json);
}
```