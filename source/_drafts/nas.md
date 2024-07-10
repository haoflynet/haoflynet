## 软件推荐

### Docker管理面板

```shell
sudo docker run -d -p 8000:8000 -p 9443:9443 --name portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce:latest
```

### Dashy 首页dashboard

```shell
sudo mkdir /srv/dashy
sudo docker run -d -p 4000:80 --name my-dashboard --restart=always lissy93/dashy:latest
```

#### Glance

- 用docker方式部署无法获取正确的网卡信息

```shell
docker run -d --restart="always" -p 61208-61209:61208-61209 -e GLANCES_OPT="-w" -v /var/run/docker.sock:/var/run/docker.sock:ro --pid host docker.io/nicolargo/glances
sudo docker run -d --restart="always" -e GLANCES_OPT="-w" -v /var/run/docker.sock:/var/run/docker.sock:ro --pid host --network host --name glances nicolargo/glances

sudo docker exec -it glances sh
vi /etc/glances.conf	# 修改network下的show，仅展示自己想要的网卡，不然太多了
```

### Jellyfin多媒体管理(电影/音乐)

- 官网提供免费的和web颜值一样的TV app
- 不要用docker安装，因为无法满足各式各样的挂载需求以及硬解码需求

```shell
sudo mkdir -p /srv/jellyfin/{config,cache}
sudo docker run -d -v /srv/jellyfin/config:/config -v /srv/jellyfin/cache:/cache -v /media:/media --net=host jellyfin/jellyfin:latest
```

### Alist 网盘挂载



### ~~Stable diffusion~~

- 性能要求太高，不适合nas

#### Samba

```shell
sudo docker run -it --name samba -p 445:445 -v /media/share:/mount -e USER="hao;fly" -e SHARE="usershare;/mount/;yes;no;no;hao" -d dperson/samba
```
