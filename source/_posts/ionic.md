---
title: "ionic 教程"
date: 2016-07-27 22:52:39
categories: frontend
---
# ionic

函数传递参数

```javascript
import {NavParams} from "ionic-angular";

export class Profile {
  private person;
  constructor(public params:NavParams) {
    this.person = CONTRIBUTORS[params.get('num')];	// 参数是以字典形式传进来的
  }
}

# 在外部
openProfilePage(num) {
  this.nav.push(Profile, {num: num});
}
```

