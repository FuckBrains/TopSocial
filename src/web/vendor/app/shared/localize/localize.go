package localize

import (
	"github.com/nicksnyder/go-i18n/i18n"
	"sync"
	"fmt"
	"log"
)


var culture = "fa-IR"
var instance *singleton
var once sync.Once

func GetInstance() *singleton {
	once.Do(func() {
		transFunc,err := GetTranslateFunction()
		if err == nil{
			instance = &singleton{
			culture:culture,
			TranslateFunc:transFunc,
			}
		}else{
			log.Fatal("Language Files Read Error!")
		}

	})
	return instance
}




type singleton struct {
	TranslateFunc i18n.TranslateFunc
	culture       string
}

func GetTranslateFunction()  (i18n.TranslateFunc,error) {
	T, err := i18n.Tfunc(culture)
	if err != nil{
		fmt.Println(err.Error())
		return  nil, err
	}
	return T, nil
}


