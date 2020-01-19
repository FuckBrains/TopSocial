package main

import (
	"app/route"
	"app/shared/cdnserver"
	"app/shared/email"
	"app/shared/recaptcha"
	"app/shared/server"
	"app/shared/session"
	"app/shared/view"
	"app/shared/view/plugin"
	"encoding/json"
	"log"
	"os"
	//"path"
	"runtime"
	//"strings"
	"github.com/nicksnyder/go-i18n/i18n"
	"topsocial/src/shared/database"
	"topsocial/src/shared/jsonconfig"
	"topsocial/src/shared/conf"
	"app/routelink"

)

// *****************************************************************************
// Application Logic
// *****************************************************************************

func init() {

	// Verbose logging with file name and line number
	log.SetFlags(log.Lshortfile)

	// Use all CPU cores
	runtime.GOMAXPROCS(runtime.NumCPU())
}

func main() {

	//***********Debug/Release**************\\


	conf.GetInstance().IsDebug = false



	var configFileName = "config.json"
	if conf.GetInstance().IsDebug {
		configFileName = "config.debug.json"
	}

	////Get Root Path
	//_, filename, _, ok := runtime.Caller(0)
	//if !ok {
	//	panic("No caller information")
	//}
	//conf.GetInstance().Absolute_Path_ROOT = strings.Replace(path.Dir(filename), "/web", "", 1)


	osSeparator := string(os.PathSeparator)
	i18n.MustLoadTranslationFile(conf.GetInstance().Absolute_Path_ROOT + osSeparator+"config"+osSeparator+"i18n"+osSeparator+"fa-IR.all.json")
	i18n.MustLoadTranslationFile(conf.GetInstance().Absolute_Path_ROOT + osSeparator+"config"+osSeparator+"i18n"+osSeparator+"fa-IR.relativedate.json")


	// Load the configuration file
	jsonconfig.Load(conf.GetInstance().Absolute_Path_ROOT+osSeparator+"config"+osSeparator+configFileName, config)

	// Configure the session cookie store
	session.Configure(config.Session)

	// Connect to database
	database.Connect(config.Database)
	database.CreateIndexes(config.Database)

	// Configure the Google reCAPTCHA prior to loading view plugins
	recaptcha.Configure(config.Recaptcha)

	//Prepare CDN Absolute URL
	if config.CDNServer.UseHTTPS {
		config.CDNServer.AbsoluteURL = cdnserver.HttpsAddress(config.CDNServer, true)
	} else {
		config.CDNServer.AbsoluteURL = cdnserver.HttpAddress(config.CDNServer, true)
	}

	// Setup the views
	view.Configure(config.View)
	view.LoadTemplates(config.Template.Root, config.Template.Children,config.Template.SingleTemplates)
	view.LoadPlugins(
		plugin.TagHelper(config.View, config.CDNServer),
		routelink.LinkHelper(config.View),
		plugin.NoEscape(),
		plugin.PrettyTime(),
		recaptcha.Plugin(),
		)
	conf.GetInstance().Base_Uri = config.View.BaseURI
	conf.GetInstance().CDNServer_UseHTTPS = config.CDNServer.UseHTTPS
	conf.GetInstance().CDNServer_HTTPPort = config.CDNServer.HTTPPort
	conf.GetInstance().CDNServer_HTTPSPort = config.CDNServer.HTTPSPort
	conf.GetInstance().CDNServer_HostName = config.CDNServer.Hostname

	// Start the listener

	server.Run(route.LoadHTTP(), route.LoadHTTPS(), config.Server)

}

// *****************************************************************************
// Application Settings
// *****************************************************************************

// config the settings variable
var config = &configuration{}

// configuration contains the application settings
type configuration struct {
	Database  database.Info    `json:"Database"`
	Email     email.SMTPInfo   `json:"Email"`
	Recaptcha recaptcha.Info   `json:"Recaptcha"`
	Server    server.Server    `json:"Server"`
	CDNServer cdnserver.Server `json:"CDNServer"`
	Session   session.Session  `json:"Session"`
	Template  view.Template    `json:"Template"`
	View      view.View        `json:"View"`
}

// ParseJSON unmarshals bytes to structs
func (c *configuration) ParseJSON(b []byte) error {
	return json.Unmarshal(b, &c)
}
