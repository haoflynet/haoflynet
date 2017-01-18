---
title: "Kubernetets 教程"
date: 2017-01-16 14:26:00
categories: tools
---
# Kubernetes手册

Kubernetes 是 Google 团队发起并维护的基于Docker的开源容器集群管理系统，它不仅支持常见的云平台，而且支持内部数据中心。

## 基本概念

- 节点: 一个节点就是一个运行Kubernetes中的主机，每个节点都有一些必要的服务以运行容器组，并且他们都可以通过主节点来管理。
- 操作对象
  - pod(容器组): 一个Pod对应于由若干容器组成的一个容器组，同个组内的容器共享一个存储卷(Volume)。
    - pos-states(容器组生命周期): 包括所有容器状态集合，包括容器组件状态类型，容器组生命周期，事件，重启策略，以及replication controllers。
    - volumes(卷): 一个卷就是一个目录，容器对其有访问权限
    - labels(标签): 用来连接一组对象，比如容器组。标签可以用来被组织和选择自对象。
    - 节点状态
      - 主机IP
      - 节点周期: Pending, Runing, Terminated
      - 节点状态
  - service: 一个Kubernetes服务是容器组逻辑的高级抽象，同时也对外提供访问容器组的策略
  - replication Controller: 负责指定数量的pod在同一时间一起运行
- 功能组件
  - master
    - apiserver: 整个系统的对外接口，提供一套RESTful的Kubernetes API，供客户端和其他组件调用
    - scheduler: 负责对资源进行调度，分配某个pod到某个节点上
    - controller-manager: 负责管理控制器，包括endpoint-controller(刷新服务和pod的关联信息)和replication-controllere(维护某个pod的复制为配置的数值)
    - Etcd: 作为数据后端和消息中间件
  - slave
    - kubelet
    - proxy