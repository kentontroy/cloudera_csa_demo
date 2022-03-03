<img src="./images/cloudera_ssb_skillup.png" alt=""/><br>

## Install Cloudera Streaming Analytics (CSA) via Docker Compose
```
export CSA_DOCKER_HOST=204.236.149.139
export CSA_DOCKER_COMPOSE=/Users/kdavis/Development/csa/docker-compose.yml
export PEM_FILE=${HOME}/Documents/Demos/creds/kdavis_pse_daily.pem

ssh -i ${PEM_FILE} ec2-user@${CSA_DOCKER_HOST}

sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
sudo reboot

ssh -i ${PEM_FILE} ec2-user@${CSA_DOCKER_HOST}

docker info
pip3 install docker-compose
mkdir -p demo/dev/docker

scp -i ${PEM_FILE} ${CSA_DOCKER_COMPOSE} ec2-user@${CSA_DOCKER_HOST}:/home/ec2-user/demo/dev/docker

ssh -i ${PEM_FILE} ec2-user@${CSA_DOCKER_HOST}
cd demo/dev/docker
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

Access the Streaming Console:
http:<CSA_DOCKER_HOST>:8000/

Default Credentials: admin/admin

```
## Install Go for use with Apache Beam and the Flink Runner
```
export GOPATH=$HOME/go/pkg/mod/
export GOROOT=/usr/local/go
export GOBIN=${GOROOT}/bin
export PATH=$PATH:${GOBIN}

go get github.com/apache/beam/sdks/v2/go/pkg/beam@latest
ls -al ${GOPATH}/github.com/apache/beam/sdks/v2@v2.36.0/go/pkg/beam

mkdir wordcount
cd wordcount
go mod init pse.cloudera.com/wordcount
go build wordCount.go

mkdir demo
cd demo
go mod init pse.cloudera.com/demo

go mod edit -replace pse.cloudera.com/wordcount=../wordcount
go mod tidy
go build demoWordCount.go
go run demoWordCount.go \
  --inputFile "shakespeare.txt" \
  --outputFile "wordCount.out"

go build demoWordCountAdvanced.go
go run demoWordCountAdvanced.go \
  --outputFile "wordCount.out"
 
```
