# 如何自定义每一行背景颜色交替不一样的ListView
## 首先创建模板化控件
* 新建项
* 选择XAML
* 选择模板化控件
* 添加

## 添加代码
```cs
public class AlternatingRowListView : ListView
{
	 public static readonly DependencyProperty EvenColorProperty =
        DependencyProperty.Register("EvenColor", typeof(SolidColorBrush), typeof(AlternatingRowListView), new PropertyMetadata(0));
    public SolidColorBrush EvenColor
    {
        get { return (SolidColorBrush)GetValue(EvenColorProperty); }
        set { SetValue(EvenColorProperty, value); }
    }
    
	  public static readonly DependencyProperty OddColorProperty =
        DependencyProperty.Register("OddColor", typeof(SolidColorBrush), typeof(AlternatingRowListView), new PropertyMetadata(0));
    public SolidColorBrush OddColor
    {
        get { return (SolidColorBrush)GetValue(OddColorProperty); }
        set { SetValue(OddColorProperty, value); }
    }
    
    public AlternatingRowListView()
    {
        DefaultStyleKey = typeof(ListView);
        Items.VectorChanged += OnItemsVectorChanged;
    }

    private void OnItemsVectorChanged(IObservableVector<object> sender, IVectorChangedEventArgs args)
    {
        if (args.CollectionChange == CollectionChange.ItemRemoved)
        {
            var removedItemIndex = (int)args.Index;
            for (var i = removedItemIndex; i < Items.Count; i++)
            {
                if (ContainerFromIndex(i) is ListViewItem listViewItem)
                {
                    listViewItem.Background = i % 2 == 0 ? EvenColor : OddColor;
                }
                else
                {
                    break;
                }
            }
        }
    }

    protected override void PrepareContainerForItemOverride(DependencyObject element, object item)
    {
        base.PrepareContainerForItemOverride(element, item);

        if (element is ListViewItem listViewItem)
        {
            var i = IndexFromContainer(element);
            listViewItem.Background = i % 2 == 0 ? EvenColor : OddColor;
        }
    }
}
```
## 在Xaml中使用
```xml
<local:AlternatingRowListView EvenColor="LightCoral"  OddColor="LightGray">
  <ListViewItem>item1</ListViewItem>
  <ListViewItem>item2</ListViewItem>
  <ListViewItem>item3</ListViewItem>
  <ListViewItem>item4</ListViewItem>
</local:AlternatingRowListView>
```

## 参考资料
[Alternate color for listview item UWP](https://stackoverflow.com/questions/46130461/alternate-color-for-listview-item-uwp)
[[UWP 自定义控件]了解模板化控件(1):基础知识](https://www.cnblogs.com/dino623/p/TemplatedControl.html)