---
title: "Android开发手册"
date: 2015-03-18 09:12:39
updated: 2018-06-13 13:37:00
categories: system
---
本文搜集了一些自己经常用到的Android方面的奇淫技巧：

*   调试：打印日志的方式

        Log.v(String tag, String msg);  //verbose类型日志，颜色为黑色
    Log.d(String tag, String msg);  //debug日志，颜色为蓝色
    Log.i(String tag, String msg);  //information日志，颜色为绿色
    Log.w(String tag, String msg); //warn告警日志，颜色为橙色
    Log.e(String tag, String msg); //error错误日志，颜色肯定为红色

*   Toast提示框：

            import android.widget.Toast;
        Toast.makeText(this,"显示内容", Toast.LENGTH_SHORT).show();

    * 获取系统时间

          import    java.text.SimpleDateFormat;     




    SimpleDateFOrmat formatter = new SimpleDateFormat("yyyy年MM月日 HH:mm:ss");
    Date curDate = new Date(System.currentTimeMillis()); // 获取当前时间
    String str = formatter.formate(curDate);

*   获取当前地理位置

        public Location getLocation() \{
        LocationManager locManger = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        Location loc = locManger.getLastKnownLocation(LocationManager.GPS_PROVIDER);
        if (loc == null) \{
            loc = locManger.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
        \}
        return loc;
    \}

*   让APP变成系统应用，无法卸载：必须root后通过re管理器进入/app目录，把安装包放在那里然后重启会自动安装
    * 让APP开机自启动

          开机自启动
      <activity>
          <intent-filter>
              <action android:name="android.intent.action.BOOT_COMPLETED"/>
              <category android:name="android.intent.category.HOME" />
          </intent-filter>
      </activity>
      权限
      <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED"></uses-permission>

    * Android镜像下载慢的问题，使用[腾讯Bugly Android SDk 镜像](http://sunjiajia.com/2015/08/16/tencent-bugly-android-sdk-mirror/ "Link: http://sunjiajia.com/2015/08/16/tencent-bugly-android-sdk-mirror/" )
    * HTTP请求：
    * mainxml的设置  


        # 使程序不现实在最近程序列表中
    <activity  android:excludeFromRecents="true"></>




*   


###Android Activity
Activity生命周期的七个函数：  
**onStart()**：可以被用户看到的时候调用的方法  
**onRestart()**：从第二个返回第一个，因为第一个没被销毁  
**onResume()**：可以获得用户焦点的时候调用  
**onPause()**：从一个Activity换向另一个Activity时第一个会调用这个  
**onStop()**：当调完第二个时，第一个就调用这个，该Activity处于不可见时，而如果没有全部遮挡起来就不会调用第一个的onStop()方法了  
**onDestroy()**：如果点击返回，可能会调用这个，把第二个摧毁了    

---
title: "新建Android项目时避免继承ActionBarActivity并去掉titleBar"
date: 2014-09-02 10:02:54
categories: Android
---
大家都知道，在最新的SDK里新建项目时默认Activity是继承于ActionBarActivity而不是Activity，虽然这样做对于大多数用户是有好处
的(考虑到兼容性)，但许多用户都不习惯这样的做法，我们都喜欢更自由的方法，直接继承于Activity。

解决方法：  
![](http://7xnc86.com1.z0.glb.clouddn.com/android-unable.jpg)  

在新建项目时Theme选择None，这样就可以直接继承了Activity，但是光这样做还是有titleBar出现，此时我们就要修改style文件(位于val
ue-vX这几个文件夹中)，将

style中标签中的parent修改为parent="@android:style/Theme.Light.NoTitleBar"即可

---
title: "导入android项目：android.support.v7"
date: 2014-08-30 17:11:41
categories: Android
---
问题原因：在高版本安卓SDK里导入低版本的SDK时出现的错误

背景知识：Google为开发者提供了Android Support Library
Package来保证高版本的SDK开发能够向下兼容，所以提供了Android Support
v4/v7/v13等几个包来分别照顾安卓1.6以上、安卓2.1以上和安卓3.2以上的版本。

解决方案：

我们在安装SDK的时候其实这几个jar包都已经在目录中了，所以可以直接在系统SDK安装目录里面搜索android-
support即可找到对应的jar包，我的SDK目录里能收到一下内容：

android-support-v4.jar  
android-support-v13.jar  
android-support-v7-appcompat.jar  
android-support-v7-gridlayout.jar  
android-support-v7-mediarouter.jar

找到对应的路径后，在项目名称上点击右键->构建路径->配置构建路径，在库(L)里面选择添加外部JAR(X)，然后在那个路径下面选择该jar即可。

---
title: "导入android项目：Unable to resolve target 'android-14'"
date: 2014-08-30 16:57:50
categories: Android
---
这是因为Android SDK的API版本不一致所致，一般出现在把低版本的安卓项目导入高版本安卓项目所致，因为我的Eclipse默认是Android
4.2.2(API 17)，即android-17，而该项目是Android 4.0(API
14)编写的，所以导入的时候需要修改项目的属性，具体API对照表可直接打开Android SDK Manager里面  
![](http://7xnc86.com1.z0.glb.clouddn.com/android-unable.jpg)  
解决方案一：直接到该项目的工作目录下找到project.properties文件，修改



    # Project target.
    target=android-14

把其中的14改为默认的17即可。

解决方案二：安装android-14对应的SDK(即Android4.0)


handler是android中为了处理异步线程更新UI的问题而出现的一个工具。在android异步线程是不能够更新UI的，只能在主线程中更新UI。那么就要通过handle来更新。

handle不能直接写在Activity里，不然会报警告Handler Class Should be Static or Leaks Occur。应该这样写：
public class SampleActivity extends Activity {

  /**
*  Instances of static inner classes do not hold an implicit
*  reference to their outer class.
     */
    private static class MyHandler extends Handler {
      private final WeakReference<SampleActivity> mActivity;
    
      public MyHandler(SampleActivity activity) {
        mActivity = new WeakReference<SampleActivity>(activity);
      }
    
      @Override
      public void handleMessage(Message msg) {
        SampleActivity activity = mActivity.get();
        if (activity != null) {
          //
    switch(msg.what){
     case 产量：
      String str1 = msg.getData().getString("变量名");break;
      default: break;
    }
        }
      }
    }
    
    private final MyHandler mHandler = new MyHandler(this);
    
    /**
   * Instances of anonymous classes do not hold an implicit
   * reference to their outer class when they are "static".
     */
     private static final Runnable sRunnable = new Runnable() {
      @Override
      public void run() {

        Message msg = new Message();
     msg.what = 常量
     Bundle bundle = new Bundle();
     bundle.putString("变量名", "变量值");
     bundle.putString("变量名", "变量值");
     msg.setData(bundle);
     mHandler.sendMessage(bundle);
        }
     };

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);

    // Post a message and delay its execution for 10 minutes.
    mHandler.postDelayed(sRunnable, 60 * 10 * 1000);
    
    // Go back to the previous Activity.
    finish();
  }
}

来源： <http://www.jcodecraeer.com/a/anzhuokaifa/androidkaifa/2014/1106/1922.html>


package com.example.haofly.myapplication;

import android.app.Notification;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import android.util.Log;

/**
*  Created by haofly on 15/8/23.
    */
      public class LocalService extends Service{
    private IBinder binder = new LocalService.LocalBinder();

    @Override
    public IBinder onBind(Intent intent){
        return binder;
    }

    @Override
    public void onCreate(){
        Log.v("haofly", "create");
        int a = 1000;
        while(a > 0){
            Log.v("haofly", "success");
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            a = a-1;
        }
    }


    public class LocalBinder extends Binder {
        LocalService getService(){
            return LocalService.this;
        }
    }
    
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        return super.onStartCommand(intent, flags, startId);
    }

}



##### 扩展阅读

[仿B站](https://github.com/TeamNB/FakeBiliBili)