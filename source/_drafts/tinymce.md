```javascript
<editor [apiKey]="tinymceEditorAPIKey" [(ngModel)]="content" [init]="tinyMceEditorInitConfig"
></editor>

const tinyMceEditorInitConfig = {
  {
    height: 500,	// 组件的高度
    inline: true,	// 默认是false，会嵌入一个iframe，当为true的时候则是内嵌的元素，能够使用我们之前有的一些样式，否则就不利于在其他地方展示了，因为其他地方不一定会引入编辑器的CSS
    plugins: 'image link',
    menubar: false,	// 是否显示menu bar，一般都不用吧，好丑
    paste_data_images: true,
    images_upload_url: 'backend.php',	// 如果没有这个值，那么只能输入图片url，只有设置这个后才能有上传按钮，可以从本地选择文件，当然，如果有自定义的images_upload_handler，可以随便写一个在这里就行
    images_upload_handler: (blobInfo: any, success: any, failure: any) => {success('data:' + blobInfo.blob().type + ';base64,' + blobInfo.base64()); },	// 自定义图片上传方法，这里这个示例可以直接返回图片的base64编码
    toolbar: 'undo redo | formatselect | bold italic link image | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent'
  }
}
```

## 不通框架版本

- [tinymce-angular](https://github.com/tinymce/tinymce-angular): 注意看README中不同angular版本对应的版本