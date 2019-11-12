# Mô hình setup Wordpress web server + HA


**Số lượng server** : 4
Bao gồm: 
* 1 HAProxy Loadbalancer
* 2 webserver
* 1 db

web1: 103.107.182.45

web2: 103.107.182.199

ha: 103.107.182.185

db: 103.107.182.182

**HAProxy được cấu hình bởi:**
* `haproxy.cfg` cấu hình trên HAProxy LB
* `ha.yaml` playbook của HAProxy

**Webserver được cấu hình sử dùng 3 file:**
* `wp-config.php` cấu hình Wordpress
* `000-defalt.conf` cấu hình virtual host 
* `web.yaml` playbook của Web Servers
         
**Database được cấu hình bởi:**
* `db.yaml` playbook của Database Server
