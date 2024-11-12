---
title: "Java Spring手册"
date: 2024-08-13 09:32:00
categories: 编程之路
---

## Troubleshooting

- **saveAndFlush后触发了额外的更新**: 场景是这样的，在一个新的对象saveAndFlush之后，去更新另外一个不同的对象，结果之前这个对象又被触发了一次更新。原因是使用了自定义的Convert

  ```java
    @Column(name = "received_timestamp")
    @Convert(converter = ZonedDateTimeConverter.class)	// 在第一个对象上使用了自定义的convert，这样在save的时候没问题，但是flush的时候重新从数据库获取该字段之后又会将其格式转换一下，这样entitymanager会认为这个字段在flush之后又被更新了，从而在其他对象更新的时候触发了级联更新
    private ZonedDateTime receivedTimestamp;
  ```

  