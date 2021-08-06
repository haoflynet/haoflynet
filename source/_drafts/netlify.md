nextjs的rewrites在netlify中不起作用，我们需要新建_redirects规则文件，并且将该文件复制到out目录下，这个复制可以借助copyfiles来完成，加到next export后面去即可

```shell
/ /signin
```

