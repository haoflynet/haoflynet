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

### Jellyfin多媒体管理(电影/音乐)

```shell
sudo mkdir -p /srv/jellyfin/{config,cache}
sudo docker run -d -v /srv/jellyfin/config:/config -v /srv/jellyfin/cache:/cache -v /media:/media --net=host jellyfin/jellyfin:latest
```

