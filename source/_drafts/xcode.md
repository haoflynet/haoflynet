---
title: "Xcode开发手册"
date: 2018-06-05 21:32:00
updated: 2018-06-05 09:36
categories: Mac
---

## 图标

App需要提供图标的规格为`40/588/60/80/87/120/160/180/1024`，另外，如果最好是将png图片转换为jpg，因为默认会把png不存在的地方背景设置为黑色。准备好图标素材以后，直接在`xcode`里面的`Images.xcassets`将图标拖入即可。

## TroubleShooting

- **Signing for "xxx" requires a development team. Select a development team in the project editor.**解决方法: 点击项目名->targets->General->Signing，选择自己的Team，选择后重新构建，如果仍然出现该错误，那么可以重启一下xcode或者更新一下xcode多次尝试。

