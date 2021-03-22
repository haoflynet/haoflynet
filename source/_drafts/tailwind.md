laravel转tailwind的工具https://github.com/awssat/tailwindo，不大好用



Important: true最好设置上



添加自定义的类

```css
@layer utilities {
  .filter-grayscale {
    filter: grayscale(100%);
  }
  
  @variants dark {
    .filter-none {
      filter: none;
    }
		.filter-grayscale(100%);
  }
}

可以这样使用
<div class="filter-grayscale dark:filter-none"></div>
```

