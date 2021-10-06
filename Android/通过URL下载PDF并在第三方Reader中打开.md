# 怎么通过URL打开PDF文件?
最开始的Android版本,好像是可以直接通过URL在Chrome里面直接打开PDF的,后来不知道从什么版本开始,因为安全的原因禁止Chrome通过URL直接打开PDF了。所以现在最近的打开PDF的策略有所改变。现在变成了**通过URL把PDF文件下载到本地,然后通过本地的默认打开PDF的app来打开PDF阅览**。这就涉及到一个问题。

## Https链接的证书异常
一般是如下的错误
```java
javax.net.ssl.SSLHandshakeException: java.security.cert.CertPathValidatorException: Trust anchor for certification path not found.
```
产生的原因一般是后端配置的证书有误,即没有在CA进行认证,或者使用了自签名的证书。客户端与服务端忽略证书校验即是在客户端的网络请求和webview中设置**信任所有证书**,然后在与服务端进行Https网络通信的时候,客户端不必进行证书校验也能进行网络通信,否则就会报证书不受信异常。
缺陷:容易受到中间人攻击。

## 自己实现的OpenPDFHelper
```kotlin
object OpenPDFHelper {
    private var mDLFailed = false

    private class MyAsyncTask : AsyncTask<String, Void, File>() {
        override fun doInBackground(vararg params: String?): File? {
            return downPDFFromUrl(params[0])
        }

        override fun onPostExecute(result: File?) {
            when {
                mDLFailed -> {
                    mDLFailed = false
                    Toast.makeText(
                        MyApplication.getContext(),
                        "PDF DL Error",
                        Toast.LENGTH_SHORT).show()
                }
                else -> {
                    openPdf(result)
                }
            }
            //UI etc.
            runCallbackEnd()
        }
    }

    //通过URL下载PDF,然后打开
    fun openPDFFromUrl(pdfUrl: String){
        //下载开始前可以进行一些处理,比如开始显示Loading界面之类的
        //TODO something
        //开始下载,新建一个线程下载
        MyAsyncTask().execute(pdfUrl, null, null)
    }

    private fun runCallbackEnd(){
        //下载结束后可以进行一些处理,比如结束Loading界面显示
    }

    @Suppress("RECEIVER_NULLABILITY_MISMATCH_BASED_ON_JAVA_ANNOTATIONS")
    private fun downPDFFromUrl(pdfUrl: String?): File?{
        if(pdfUrl.isNullOrEmpty()) return null

        try {
            val url = URL(pdfUrl)
            //需要判断是否是HTTPS的URL
            val connection : HttpURLConnection? = if(url.protocol.toUpperCase() == "HTTPS"){
                trustAllHosts() //忽略证书的校验
                val https = url.openConnection() as HttpsURLConnection
                https.setHostnameVerifier { _, _ -> true }
                https
            } else{
                url.openConnection() as HttpURLConnection
            }

            connection!!.requestMethod = "GET"
            connection.doInput = true
            connection.connectTimeout = 5000
            connection.connect()

            var file : File? = null

            //download the file
            if(connection.responseCode == 200){
                val inputS = connection.inputStream
                val arr = ByteArray(1)
                val baos = ByteArrayOutputStream()
                val bos = BufferedOutputStream(baos)
                var n = inputS.read(arr)
                while(n > 0){
                    bos.write(arr)
                    n = inputS.read(arr)
                }
                bos.close()
                var path = MyApplication.getContext().externalCacheDir.path
                val name = pdfUrl.split("/")
                path = "${path}/${name[name.size - 1]}"
                file = File(path)
                val fos = FileOutputStream(file)
                fos.write(baos.toByteArray())
                fos.close()
                baos.close()

                connection.disconnect()
                Log.d("OpenPDFHelper", "Download Success")
                return file
            }
            else{
                Log.d("OpenPDFHelper", "Response Failed:[${connection.responseCode}]")
                runCallbackEnd()
                //Toast DL failed
                mDLFailed = true
            }
        }
        catch (e:Exception){
            Log.d("OpenPDFHelper", "Download Failed")
            runCallbackEnd()
            //Toast DL failed
            mDLFailed = true
        }
        return null
    }

    //使用OS默认的PDF viewer打开PDF文件
    private fun openPdf(pdfFile: File?){
        if(pdfFile == null) return

        if(pdfFile.exists()){
            try{
                val context = MyApplication.getContext()
                val uri = FileProvider.getUriForFile(context,
                    context.applicationContext.packageName + ".provider",
                    pdfFile)
                val intent = Intent()
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
                intent.action = Intent.ACTION_VIEW
                intent.setDataAndType(uri, "application/pdf")

                context.startActivity(intent)

                Log.d("OpenPDFHelper", "Open the pdf:[${pdfFile.path}]")
            }
            catch (e: Exception){
                Log.d("OpenPDFHelper", "Open the pdf failed:[${pdfFile.path}]")
                runCallbackEnd()
            }
        }
        else{
            Log.d("OpenPDFHelper", "pdf file not exists")
            runCallbackEnd()
        }
    }

    //相信所有的证书
    private fun trustAllHosts() {
        // Create a trust manager that does not validate certificate chains
        // Android use X509 cert
        val trustAllCerts =
            arrayOf<TrustManager>(object : X509TrustManager {
                override fun getAcceptedIssuers(): Array<X509Certificate> {
                    return arrayOf()
                }

                @Throws(CertificateException::class)
                override fun checkClientTrusted(
                    chain: Array<X509Certificate>,
                    authType: String
                ) {
                }

                @Throws(CertificateException::class)
                override fun checkServerTrusted(
                    chain: Array<X509Certificate>,
                    authType: String
                ) {
                }
            })

        // Install the all-trusting trust manager
        try {
            val sc: SSLContext = SSLContext.getInstance("TLS")
            sc.init(null, trustAllCerts, SecureRandom())
            HttpsURLConnection
                .setDefaultSSLSocketFactory(sc.socketFactory)
        } catch (e: java.lang.Exception) {
            e.printStackTrace()
        }
    }
}
```

## 参考资料
* [Android网络请求忽略https证书验证](https://www.jianshu.com/p/4dc104b681d7)
* [Android中忽略okhttp ssl验证](https://www.jianshu.com/p/0501769e4183)