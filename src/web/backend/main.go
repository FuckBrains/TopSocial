package main

import (
	"github.com/kataras/iris"
	//"gopkg.in/olivere/elastic.v3"
	//"github.com/iris-contrib/middleware/logger"
	"./routes"
	"github.com/kataras/go-template/html"
)

func main() {
	iris.UseTemplate(html.New(html.Config{Layout: "layout.html"})).Directory("../frontend/templates", ".html")
	iris.Static("/public", "../frontend/public", 1)
	//iris.Use(logger.New())

	// set the custom errors
	iris.OnError(iris.StatusNotFound, func(ctx *iris.Context) {
		ctx.Render("errors/404.html", iris.Map{"Title": iris.StatusText(iris.StatusNotFound)})
	})

	iris.OnError(iris.StatusInternalServerError, func(ctx *iris.Context) {
		ctx.Render("errors/500.html", nil, iris.RenderOptions{"layout": iris.NoLayout})
	})

	//DbMain()
	// register the routes & the public API
	registerRoutes()
	//registerAPI()

	iris.Listen(":8080")
	//api := iris.New()
	//api.Get("/hi", hi)
	//api.Listen(":8080")
}

func registerRoutes() {
	// register index using a 'Handler'
	iris.Handle("GET", "/", routes.Index())

	//// this is other way to declare a route
	//// using a 'HandlerFunc'
	//iris.Get("/about", routes.About)
	//
	//// Dynamic route
	//
	//iris.Get("/profile/:username", routes.Profile)("user-profile")
	//// user-profile is the custom,optional, route's Name: with this we can use the {{ url "user-profile" $username}} inside userlist.html
	//
	//iris.Get("/all", routes.UserList)
}

//func hi(ctx *iris.Context) {
//	client, err := elastic.NewClient()
//	if err != nil {
//		// Handle error
//		panic(err)
//	}
//
//	esversion, err := client.ElasticsearchVersion("http://127.0.0.1:9200")
//	if err != nil {
//		// Handle error
//		panic(err)
//	}
//	ctx.Write("Hi %s", esversion)
//}
