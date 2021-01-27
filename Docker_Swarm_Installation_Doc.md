# DOCKER SWARM INSTALLATION DOCUMENTATION

**<h3>WHY DOCKER?</h3>**
- Triển khai kiến trúc Microservices.
- Khi xây dựng ứng dụng và cần scale một cách linh hoạt.
- Khi bạn muốn không tốn khá nhiều thời gian để config máy local và server cùng một môi trường để chạy được ứng dụng. Bạn chỉ cần build 1 lần chạy ở nhiều nơi mà thôi.
- Sản phẩm của công ty bạn cần một cách tiếp cận mới về xây dựng, đẩy lên server, thực thi ứng dụng một cách nhanh chóng dễ dàng.

**<h3>DOCKER MAIN CONCEPTS</h3>**
- *<u>Docker:</u>* là open source platform để dev, shipping và run các App. Docker cho phép tách các App khỏi cơ sở hạ tầng để có thể phân phối một cách nhanh chóng.Docker giúp quản lý cơ sở hạ tầng giống như quản lý các ứng dụng. Docker giảm đáng kể độ trễ giữa việc viết code và run code trong production environment.
- *<u>Containers</u>* cho phép lập trình viên đóng gói một ứng dụng với tất cả các phần cần thiết, chẳng hạn như thư viện và các phụ thuộc khác, và gói tất cả ra dưới dạng một package. Bằng cách đó, nhờ vào container, ứng dụng sẽ chạy trên mọi máy khác bất kể mọi cài đặt tùy chỉnh mà máy có thể có khác với máy được sử dụng để code.
- *<u>Image</u>* Một Image là một khuôn mẫu để tạo một container. Thường thì image sẽ có sẵn với những tùy chỉnh thêm. Ví dụ khi build 1 image dựa trên image Centos có sẵn để chạy Nginx và những tùy chỉnh, cấu hình để ứng dụng web chạy.Một image có thể được build riêng hoặc sử dụng những image được chia sẽ từ cộng đồng Docker Hub và chúng được build dựa trên những chỉ dẫn của Dockerfile.
- *<u>Dockerfile</u>*: là một tập tin bao gồm các chỉ dẫn để build một image.
- *<u>Docker Engine</u>* : thành phần chính của Docker, như một công cụ để đóng gói ứng dụng.
- *<u>Docker Hub</u>*: "Kho" chứa những public image của Docker được cộng đồng push lên. Để sử dụng các image đó chỉ cần pull về.

**<h3>DOCKER FUNCTION</h3>**

- Hoạt động của Docker cơ bản được thể hiện qua hình sau: 

    ![](https://github.com/dung3197/Git_Pub/blob/master/Pics/basic_function.png)

- Tác vụ: 
    - Build: Tạo một dockerfile chứa code và sẽ được build tại máy tính đã cài đặt Docker Engine. Sau khi build ta sẽ có được Container, trong Container này chứa ứng dụng kèm bộ thư viện của chúng ta.
    - Push: Khi build xong Container, push Container này lên cloud.
    - Pull và Run: Khi một máy tính khác muốn sử dụng Container đã được build thì cần thực hiện pull Container đó về và Run. Máy pull về cũng phải có Docker Engine.

**<h3>DOCKER SWARM INSTALLATION AND SETUP</h3>**
**<i>Docker Swamp là gì ?</i>**
 - Docker Swarm là một công cụ phân cụm riêng cho các Docker containers có thể được sử dụng để quản lý một cụm(cluster) các nút(node) Docker. Docker Swarm cho phép thêm hoặc bớt containers khi nhu cầu thay đổi. Docker Swarm bao gồm hai thành phần chính là Manager node và Worker node. 
    - Manager node được sử dụng để xử lý các tác vụ quản lý cluster chẳng hạn như:
        - Duy trì trạng thái cụm
        - Lập lịch dịch vụ và phục vụ các API HTTP endpoints. 
    - Worker node là một ví dụ Docker Engine có thể được sử dụng để thực thi container. 
    - Swarm Manager cho phép bạn tạo một manager instance chính và nhiều bản sao trong trường hợp phiên bản chính bị lỗi. 
    - Có thể triển khai manager node và worker node ở chế độ Swarm của Docker Engine.
> Hướng dẫn này chỉ dẫn từng bước cài đặt và cấu hình triển khai Docker Swarm trên ba node chạy Centos 7.

**<i><u>Prerequisite for Installation</u></i>**
>OS: Centos7

>IP 3 nodes:
 - Worker1: 10.19.2.59
 - Manager: 10.19.2.60
 - Worker2: 10.19.2.61

**<i>Installation and Setup</i>**
- Bước 1: Sửa file `/etc/host` trên cả 3 máy để các node có thể giao tiếp với nhau qua host name: 

    ![](https://github.com/dung3197/Git_Pub/blob/master/Pics/hosts.png)
- Bước 2: Chạy lệnh trên ba máy để set hostname tương ứng với file `/etc/hosts`:
    - Trên node manager: `hostnamectl set-hostname managernode`
    - Trên node worker1: `hostnamectl set-hostname workernode1`
    - Trên node worker2: `hostnamectl set-hostname workernode2`
- Bước 3: Cài đặt Docker Engine:
     >Mặc định phiên bản mới nhất của Docker Community Edition không có sẵn trong repository của Centos 7, nên Docker CE repo cần được thêm vào hệ thống. Chạy lệnh sau trên cả ba node để thêm: `wget https://download.docker.com/linux/centos/docker-ce.repo -O /etc/yum.repos.d/docker.repo` 

    >Khi Docker CE repo đã được thêm xong, chạy lệnh sau để cài đặt Docker CE: `yum install docker-ce –y`
- Bước 4: Start Service và Enable để nó được Start lúc boot, chạy lần lượt hai lệnh:`systemctl start docker` và `systemctl enable docker`.
- Bước 5: Cấu hình tường lửa trên cả 3 node để có thể cho phép những port cần thiết hoạt động ổn định phục vụ giao tiếp lẫn nhau trong cụm:
    - `firewall-cmd --permanent --add-port=2376/tcp`
    - `firewall-cmd --permanent --add-port=2377/tcp`
    - `firewall-cmd --permanent --add-port=7946/tcp`
    - `firewall-cmd --permanent --add-port=80/tcp`
    - `firewall-cmd --permanent --add-port=7946/udp`
    - `firewall-cmd --permanent --add-port=4789/udp`
- BƯớc 6: Reload lại cấu hình tường lửa để nó áp dụng được các thay đổi: `firewall-cmd --reload` và `systemctl restart docker`
- Bước 7: Tạo một Swarm trên node manager bằng lệnh "docker swarm init". Lệnh này sẽ biến node hiện tại của bạn thành manager node và quảng bá địa chỉ IP của nó: `docker swarm init --advertise-addr 10.19.2.60`. 
=> Kết quả trả về của câu lệnh sẽ gồm giá trị token, ví dụ như `--token SWMTKN-1-3793hvb71g0a6ubkgq8zgk9w99hlusajtmj5aqr3n2wrhzzf8z-1s38lymnir13hhso1qxt5pqru`. *Cần lưu ý copy lại đoạn giá trị token này để phục vụ join các node worker vào cluster sau này*.
- Bước 8: Join các node worker vào cluster bằng lệnh: `docker swarm join --token SWMTKN-1-3793hvb71g0a6ubkgq8zgk9w99hlusajtmj5aqr3n2wrhzzf8z-1s38lymnir13hhso1qxt5pqru 10.19.2.60:2377` (thay giá trị token trong ví dụ bằng giá trị token bạn thu được).

- Bước 9: Sau đó kiểm tra xem các node đã (active)lên chưa với: `docker node ls`
![](https://github.com/dung3197/Git_Pub/blob/master/Pics/nodes.png)
=> Bất kỳ khi nào quên giá trị token, chúng ta đều có thể lấy lại được bằng cách chạy lệnh trên node manager: `docker swarm join-token manager -q`

- Bước 10: Swarm Cluster lúc này đã sẵn sàng. Ta thử triển khai Web Server Service trên ba container bằng cách chạy lệnh trên node manager: `docker service create -p 80:80 --name webservice --replicas 3 httpd`
    > Lệnh trên sẽ tạo một service với tên webservice và các container sẽ được khởi tạo từ docker image “httpd”. Container được triển khai trên các node Managernode, Workernode1 và Workernode2. Có thể liệt kê và kiểm tra trạng thái của dịch vụ bằng lệnh: `docker service ls`

**<i><u>Container-Self Healing</u></i>**
>Một trong những tính năng quan trọng của swarm mode Docker là Container tự phục hồi. Nếu bất kỳ Container nào gặp sự cố, Container đó sẽ tự động khởi động lại trên cùng một node hoặc trên một node khác. Để kiểm tra tính năng tự phục hồi Container, hãy xóa Container khỏi workernode và xem liệu Container mới có được khởi chạy hay không. Trước khi bắt đầu, ta sẽ cần ID Container để xóa. Có thể liệt kê ID Container bằng cách chạy lệnh sau trên Workernode: `docker ps`

>Thử xóa Container với ID 9b01b0a55cb7 bằng lệnh: `docker rm 9b01b0a55cb7 -f`. Sau đó kiểm tra xem một Container mới có được start hay chưa với: `docker service ps webservice`. 

> Kết quả mong muốn nên giống với ví dụ sau:

|ID|NAME|IMAGE|NODE|DESIRED STATE|CURRENT STATE|ERROR|PORTS|
|--|----|-----|----|-------------|-------------|-----|-----|
|z1spatkk1jj7|webservice.1|httpd:latest|workernode2|Running|Preparing 29 seconds ago|||                                   
|xsa5wb0eg2ln|\_ webservice.1|httpd:latest|workernode2|Shutdown|Failed 30 seconds ago|"task: non-zero exit (137)"||
