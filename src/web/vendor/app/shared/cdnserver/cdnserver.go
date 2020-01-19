package cdnserver

import (

	"fmt"
	"topsocial/src/shared/conf"
)

// Server stores the hostname and port number
type Server struct {
	Hostname    string `json:"Hostname"`  // Server name
	UseHTTP     bool   `json:"UseHTTP"`   // Listen on HTTP
	UseHTTPS    bool   `json:"UseHTTPS"`  // Listen on HTTPS
	HTTPPort    int    `json:"HTTPPort"`  // HTTP port
	HTTPSPort   int    `json:"HTTPSPort"` // HTTPS port
	CertFile    string `json:"CertFile"`  // HTTPS certificate
	KeyFile     string `json:"KeyFile"`   // HTTPS private key
	AbsoluteURL string
}

// httpAddress returns the HTTP address
func HttpAddress(s Server, isAbs bool) string {
	var protocol string
	if isAbs {
		protocol = GetProtocol(s.UseHTTPS)
	}
	if s.Hostname == ""{
		return protocol + "127.0.0.1:" + fmt.Sprintf("%d", s.HTTPPort)
	}else{
		return protocol + s.Hostname
	}

}

// httpsAddress returns the HTTPS address
func HttpsAddress(s Server, isAbs bool) string {
	var protocol string
	if isAbs {
		protocol = GetProtocol(s.UseHTTPS)
	}
	if s.Hostname == ""{
		return protocol + "127.0.0.1:" + fmt.Sprintf("%d", s.HTTPSPort)
	}else{
		return protocol + s.Hostname
	}

}

func GetProtocol(isHttps bool) string {
	var protocol = "http://"
	if isHttps {
		protocol = "https://"
	}
	return protocol
}
func GetPort(isHttps bool) int {
	var port = conf.GetInstance().CDNServer_HTTPPort
	if isHttps {
		port = conf.GetInstance().CDNServer_HTTPSPort
	}
	return port
}

func AbsoluteUrl(url string) string {
	s := conf.GetInstance()
	if(s.CDNServer_HostName == ""){
		return GetProtocol(s.CDNServer_UseHTTPS) + "127.0.0.1:" + fmt.Sprintf("%d", GetPort(s.CDNServer_UseHTTPS)) + url
	} else{
		return GetProtocol(s.CDNServer_UseHTTPS) + s.CDNServer_HostName + url
	}

}
