如果不想tolltip超过边界，可以设置bounds的值为self(原声js可以设置为.ql-editor)，默认是body上面的


quill不支持编辑或添加div等tag，可以使用https://summernote.org/来代替，不过这个也仅支持body



插图图片并顺边设置大小

```
editor.insertEmbed(editor.range?.index ?? 0, 'image', typeof data === 'string' ? image : {image}, Quill.sources.USER);
editor.formatText(editor.range?.index ?? 0, 1, 'width', '600');‘
我要是不在下面编辑一下，双向绑定的变量就获取不到这个600的styling

 editor.insertText(editor.range?.index ?? 0, '\n', Quill.sources.USER);
```

居然默认不支持给图片变更大小，可以使用这个很久没维护的库https://github.com/kensnyder/quill-image-resize-module





api居然这么简单https://quilljs.com/docs/api/#deletetext，连getContents都只能获取到一个看不懂的delta



## 初始化

```javascript
import Quill from 'quill';
import ImageResize from 'quill-image-resize-module';	// image resize功能

const BaseImageFormat = Quill.import('formats/image');
const ImageFormatAttributesList = ['alt', 'height', 'width', 'style'];	// 允许image的某些dom属性，如果没有添加，会造成image resize后的一些style丢失

class ImageFormat extends BaseImageFormat {
  domNode: any;

  static formats(domNode): any {
    return ImageFormatAttributesList.reduce((formats, attribute) => {
      if (domNode.hasAttribute(attribute)) {
        formats[attribute] = domNode.getAttribute(attribute);
      }
      return formats;
    }, {});
  }

  format(name, value): void {
    if (ImageFormatAttributesList.indexOf(name) > -1) {
      if (value) {
        this.domNode.setAttribute(name, value);
      } else {
        this.domNode.removeAttribute(name);
      }
    } else {
      super.format(name, value);
    }
  }
}

Quill.register(ImageFormat, true);
Quill.register('modules/imageResize', ImageResize);
```

## 配置

```javascript
const modules = {
  toolbar: [
    ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
    ['blockquote', 'code-block'],

    [{ 'header': 1 }, { 'header': 2 }],               // custom button values
    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
    [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
    [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
    [{ 'direction': 'rtl' }],                         // text direction

    [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

    [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
    [{ 'font': [] }],
    [{ 'align': [] }],

    ['clean'],                                         // remove formatting button

    ['link', 'image', 'video']                         // link and image, video
  ],
  imageResize: {}, 	// 支持图片resize
};
```

## Troubleshooting

- **image inline style丢失**: 在保存的时候可以，但是重新展示的时候又没有了，默认quill不会展示inline style，如果需要，可以参考上面的`ImageFormatAttributesList`
