package main

import (
	"app/route"
	"app/shared/conf"
	"app/shared/jsonconfig"
	"app/shared/server"
	"encoding/json"
	"os"
)

func main() {
	//***********Debug/Release**************\\
	conf.GetInstance().IsDebug = true

	//_, filename, _, ok := runtime.Caller(0)
	//if !ok {
	//	panic("No caller information")
	//}
	//conf.GetInstance().Absolute_URL_ROOT = strings.Replace(path.Dir(filename), string(os.PathSeparator)+"cdn", "", 1)

	var configFileName = "config.json"
	if conf.GetInstance().IsDebug {
		configFileName = "config.debug.json"
	}

	// Load the configuration file
	jsonconfig.Load(conf.GetInstance().Absolute_Path_ROOT +string(os.PathSeparator)+"config"+string(os.PathSeparator)+configFileName, config)

	// Start the listener
	server.Run(route.LoadHTTP(), route.LoadHTTPS(), config.Server)

}

// config the settings variable
var config = &configuration{}

// configuration contains the application settings
type configuration struct {
	Server server.Server `json:"CDNServer"`
}

// ParseJSON unmarshals bytes to structs
func (c *configuration) ParseJSON(b []byte) error {
	return json.Unmarshal(b, &c)
}
