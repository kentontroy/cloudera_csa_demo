## High-Level Architecture for Demo

<img src="./images/cloudera_ssb_skillup.png" alt=""/><br>

## Install Cloudera Streaming Analytics (CSA) via Docker Compose

From Linux or Mac laptop/desktop:
```
export CSA_DOCKER_HOST=204.236.149.139
export PEM_FILE=${HOME}/Documents/Demos/creds/kdavis_pse_daily.pem

ssh -i ${PEM_FILE} ec2-user@${CSA_DOCKER_HOST}
```
Inside the EC2 host, configure environment and install dependneces
```
sudo yum update -y
sudo amazon-linux-extras install docker
sudo yum install -y jq
sudo service docker start
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
mkdir -p demo/dev/
sudo reboot
```
From Mac or Linux host, copy PEM file to EC2
```
scp -i ${PEM_FILE} ec2-user@${CSA_DOCKER_HOST}:/home/ec2-user/demo/dev/

ssh -i ${PEM_FILE} ec2-user@${CSA_DOCKER_HOST}
```
Inside the EC2 host, launch Docker instances
```
docker info
pip3 install docker-compose
cd demo/dev/
git clone https://github.com/kentontroy/cloudera_csa_demo
cd docker
export CML_DEMO_HOME=${PWD}
./jupyter.sh

docker-compose up -d --scale flink-taskmanager=2

docker images
REPOSITORY                                                 TAG          IMAGE ID       CREATED        SIZE
docker.repository.cloudera.com/csa/ssb-docker_console      1.6.0.0-ce   d1c19979f5a6   2 months ago   1.15GB
docker.repository.cloudera.com/csa/ssb-docker_snapper      1.6.0.0-ce   7fd4fb668e59   2 months ago   500MB
docker.repository.cloudera.com/csa/ssb-docker_sqlio        1.6.0.0-ce   4240d40117e0   2 months ago   1.08GB
docker.repository.cloudera.com/csa/ssb-docker_flink        1.6.0.0-ce   fe14195232c3   2 months ago   2.22GB
docker.repository.cloudera.com/csa/ssb-docker_zookeeper    1.6.0.0-ce   db44b3d523f9   2 months ago   441MB
docker.repository.cloudera.com/csa/ssb-docker_kafka        1.6.0.0-ce   231ddba4d185   2 months ago   480MB
docker.repository.cloudera.com/csa/ssb-docker_postgresql   1.6.0.0-ce   ecd73b2f255c   2 months ago   542MB
```

## Access the Streaming Console:
```
http:<CSA_DOCKER_HOST>:8000/

Default Credentials: admin/admin
```
