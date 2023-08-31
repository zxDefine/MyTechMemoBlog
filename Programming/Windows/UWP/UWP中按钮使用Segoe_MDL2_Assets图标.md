# UWP中按钮使用Segoe MDL2 Assets图标
不只是在Button中,应用中的Icon设置一共有以下几种方式。不过这里只说明怎么使用字体图标Segoe MDL2 Assets。

## 设置Icon的几种方式
### 使用预定义的图标
Microsoft 提供 1000 多个 Segoe MDL2 Assets 字体格式的图标。 从字体获取图标可能不直观,但字体显示技术意味着这些图标在任何显示器、任何分辨率、任何尺寸下都能够有简洁、清晰的外观。图标示例查看 [Segoe MDL2 图标](https://docs.microsoft.com/zh-cn/windows/apps/design/style/segoe-ui-symbol-font#how-do-i-get-this-font)。

### 使用字体
不一定要使用 Segoe MDL2 Assets 字体,也可以使用本地系统上安装的任何字体,如 Wingdings 或 Webdings。

### 使用可缩放矢量图形 (SVG) 文件
SVG 资源非常适合作为图标,因为它们在任何尺寸或分辨率下都可以清晰的使用。并且大多数绘图应用程序都可以导出为 SVG。 相关说明方法可查看[SVGImageSource](https://docs.microsoft.com/zh-cn/uwp/api/windows.ui.xaml.media.imaging.svgimagesource?view=winrt-20348)。

### 使用几何图形对象
与 SVG 文件一样,几何图形也是一种基于矢量的资源,所以在任何尺寸或分辨率下都很清晰。 不过,创建几何图形比较复杂,因为必须单独指定每个点和曲线。 如果需要在应用运行时修改图标(以便对其进行动画处理等),它确实是很好的选择。 相关说明可以查看[移动和绘制几何图形的命令](https://docs.microsoft.com/zh-cn/windows/uwp/xaml-platform/move-draw-commands-syntax)。

### 使用位图(如PNG,GIF或JPEG),不推荐使用
位图以特定尺寸创建,因此它们必须根据你需要的图标大小和屏幕分辨率放大或缩小。 当图像缩小(收缩)时,它可能显示得比较模糊;当放大时,它可能显示为像素颗粒。 如果必须使用位图,建议使用 PNG 或 GIF 而不是 JPEG。

## Segoe MDL2 Assets使用
### 在Xaml中使用
```cs
<Button>
	<RelativePanel>
		<TextBlock x:Name="IconButton" FontFamily="Segoe MDL2 Assets" Text="&#xE80F;" Margin="0,3,0,0"  VerticalAlignment="Center"/>
		<TextBlock Text="Home" RelativePanel.RightOf="IconButton" VerticalAlignment="Center"/>
	</RelativePanel>
</Button>
```
### C#中使用
```cs
TextBlock textBlock = new TextBlock();
textBlock.FontFamily = new FontFamily("Segoe MDL2 Assets");
textBlock.Text = ((char)0xE707).ToString();
mCanvas.Children.Add(textBlock);
```