# Android使用相机时如何设置最优的图片Size问题
在开发Android程序的时候,有时候会用到Camera功能,但是在设置Camera的时候,需要设置Camera的拍照的图片预览Size.怎么设置最优的Size如下

## 定义
定义一个最优Size获取函数.
```kotlin
private fun getOptimalSize(sizeList: Array<Size>?, maxWidth: Int, maxHeight: Int): Size
```
## 处理
主要分三步
1. sizeList里面的Size要比**maxWidth\*maxHeightda**.
2. Size的长宽比要跟**maxWidth/maxHeight**一样或接近.
3. 所有适配Size中面积最小的一组.
4. 如果在第2步的时候找到一个最接近或是一样的长宽比Size的话,就不需要执行第3步了.
