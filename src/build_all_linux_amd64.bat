set GOOS=linux
set GOARCH=amd64
go build -o topsocial web\main.go
go build -o topsocialcdn cdn\cdn.go
go build -o aggregate_agent shared\services\aggregate_agent.go
