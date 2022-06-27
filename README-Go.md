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
