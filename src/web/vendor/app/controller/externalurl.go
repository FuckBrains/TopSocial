package controller

import (
	"github.com/julienschmidt/httprouter"
	"github.com/gorilla/context"
	"net/http"
	"app/shared/view"
	"topsocial/src/shared/model"
	"strconv"
)

func LoadExternalUrl(w http.ResponseWriter, r *http.Request)  {
	var params httprouter.Params
	params = context.Get(r, "params").(httprouter.Params)
	_key := params.ByName("id")



	post,err:= model.PostByID(_key)
	if(err != nil) {

	}

	urlIndexStr := params.ByName("index")
	urlIndex ,err := strconv.Atoi(urlIndexStr)

	v := view.New(r)
	v.Name = "externalurl/iframed"
	v.Vars["url_to_iframe"] = post.Urls_Extracted[urlIndex].Url
	v.Vars["title"] = post.Title

	v.Render(w)
}