package conf

import (
	"sync"
	//"strings"
	//"path"
	//"runtime"
	"path/filepath"
	"strings"
	"os"
)

type singleton struct {
	CDNServer_UseHTTPS  bool
	CDNServer_HostName  string
	CDNServer_HTTPSPort int
	CDNServer_HTTPPort  int
	Absolute_Path_ROOT  string
	Base_Uri	    string
	IsDebug             bool
}

var instance *singleton
var once sync.Once

func GetInstance() *singleton {
	once.Do(func() {
		//Get Root Path
		//_, filename, _, ok := runtime.Caller(0)
		//if !ok {
		//	panic("No caller information")
		//}

		dir, _ := filepath.Abs(os.Getenv("GOPATH")+string(os.PathSeparator)+"src"+string(os.PathSeparator)+"topsocial"+string(os.PathSeparator)+"src")
		//dir, _ := filepath.Abs(".")

		instance = &singleton{
			//Absolute_Path_ROOT:strings.Replace(dir, "/web", "", 1),
			Absolute_Path_ROOT:strings.Replace(dir,"cdn","",1),
		}
	})
	return instance
}
