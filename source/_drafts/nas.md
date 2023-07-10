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

Glance

```shell
docker run -d --restart="always" -p 61208-61209:61208-61209 -e GLANCES_OPT="-w" -v /var/run/docker.sock:/var/run/docker.sock:ro --pid host docker.io/nicolargo/glances
```

### Jellyfin多媒体管理(电影/音乐)

- 官网提供免费的和web颜值一样的TV app

```shell
sudo mkdir -p /srv/jellyfin/{config,cache}
sudo docker run -d -v /srv/jellyfin/config:/config -v /srv/jellyfin/cache:/cache -v /media:/media --net=host jellyfin/jellyfin:latest
```

## Glance

- 用docker方式部署无法获取正确的网卡信息

```shell
sudo docker run -d --restart="always" -e GLANCES_OPT="-w" -v /var/run/docker.sock:/var/run/docker.sock:ro --pid host --network host --name glances nicolargo/glances

sudo docker exec -it glances sh
vi /etc/glances.conf	# 修改network下的show，仅展示自己想要的网卡，不然太多了
```

### Stable diffusion

- 它的Docker基本都是基于CUDA(英伟达显卡平台)的，所以只能直接搞，不用docker了

```dockerfile
git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
cd stable-diffusion-webui
sudo apt install wget git python3 python3-venv

python3 -m venv venv
vim webui-user.sh	# 修改install_dir为当前目录

./webui.sh
docker run --restart unless-stopped -p 8080:8080 -v /media/share/diffusion-datadirextensions:/app/stable-diffusion-webui/extensions -v /media/share/diffusion-datadir/models:/app/stable-diffusion-webui/models -v /media/share/diffusion-datadir/outputs:/app/stable-diffusion-webui/outputs -v /media/share/diffusion-datadir/localizations:/app/stable-diffusion-webui/localizations --name stable-diffusion-webui -d universonic/stable-diffusion-webui
```

#### Samba

```shell
sudo docker run -it --name samba -p 445:445 -v /media/share:/mount -e USER="hao;fly" -e SHARE="usershare;/mount/;yes;no;no;hao" -d dperson/samba
```
