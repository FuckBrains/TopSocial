package conf

import (
	"sync"
	"path/filepath"
	"strings"
)

type singleton struct {
	Absolute_URL_ROOT string
	Absolute_Path_ROOT string
	IsDebug           bool
}

var instance *singleton
var once sync.Once

func GetInstance() *singleton {
	once.Do(func() {
		dir, _ := filepath.Abs(".")
		instance = &singleton{
			Absolute_Path_ROOT:strings.Replace(dir,"cdn","",1) ,
		}
	})
	return instance
}
