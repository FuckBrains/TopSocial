package main

import (

	"topsocial/src/shared/model"
	"topsocial/src/shared/custom_type"
	"topsocial/src/shared/enum"
	"log"
	"time"
	"topsocial/src/shared/database"
	"os"
	"topsocial/src/shared/jsonconfig"
	"topsocial/src/shared/conf"

	"encoding/json"
)

func main() {

	conf.GetInstance().IsDebug = false
	var configFileName = "config.json"
	if conf.GetInstance().IsDebug {
		configFileName = "config.debug.json"
	}

	// Load the configuration file
	jsonconfig.Load(conf.GetInstance().Absolute_Path_ROOT+string(os.PathSeparator)+"config"+string(os.PathSeparator)+configFileName, config)

	// Connect to database
	database.Connect(config.Database)


	fromDate:= custom_type.NullTime{Valid:true,Time:time.Now().AddDate(0,0,-100)}
	err :=  model.UpdateRecentPopularPosts(fromDate,100,[]int{enum.PostType_Image},"RecentPopularImagesCache")
	if err !=nil{
		log.Fatal(err.Error())
	}else{
		log.Println("RecentPopularImagesCache updated successfully...")
	}
	err = model.RemoveOldRecentPopularPosts("RecentPopularImagesCache")
	if err !=nil{
		log.Fatal(err.Error())
	}else{
		log.Println("RecentPopularImagesCache olds removed  successfully...")
	}


	err = model.UpdateRecentPopularPosts(fromDate,100,[]int{enum.PostType_Video},"RecentPopularVideosCache")
	if err !=nil{
		log.Fatal(err.Error())
	}else{
		log.Println("RecentPopularVideosCache updated successfully...")
	}
	err = model.RemoveOldRecentPopularPosts("RecentPopularVideosCache")
	if err !=nil{
		log.Fatal(err.Error())
	}else{
		log.Println("RecentPopularVideosCache olds removed  successfully...")
	}


	err = model.UpdateRecentPopularHashtags(fromDate,100)
	if err !=nil{
		log.Fatal(err.Error())
	}else{
		log.Println("UpdateRecentPopularHashtags completed successfully...")
	}
	err = model.RemoveOldRecentPopularHashtags()
	if err !=nil{
		log.Fatal(err.Error())
	}else{
		log.Println("RemoveOldRecentPopularHashtags completed successfully...")
	}


	//err = model.UpdateTotalHashtags()
	//if err !=nil{
	//	log.Fatal(err.Error())
	//}else{
	//	log.Println("UpdateTotalHashtags completed successfully...")
	//}


}


// config the settings variable
var config = &configuration{}

// configuration contains the application settings
type configuration struct {
	Database  database.Info    `json:"Database"`
}

// ParseJSON unmarshals bytes to structs
func (c *configuration) ParseJSON(b []byte) error {
	return json.Unmarshal(b, &c)
}