package controller

import (
	"strconv"
	"strings"
	"encoding/json"
	"log"
	"app/shared/view"
	"net/http"
	"github.com/julienschmidt/httprouter"
	"github.com/gorilla/context"
	"topsocial/src/shared/stringhelpers"
	"topsocial/src/shared/model"
	"topsocial/src/shared/custom_type"
	"app/shared/localize"
)

func SearchGET(w http.ResponseWriter, r *http.Request) {

	// Get session
	var params httprouter.Params
	params = context.Get(r, "params").(httprouter.Params)
	sort := params.ByName("sort")
	q := params.ByName("q")
	spageNum := params.ByName("page")
	pageNum, _ := strconv.Atoi(spageNum)

	if pageNum == 0 {
		pageNum = 1
	}

	posts, err, isLastPage := model.PostsSearch(sort, pageNum, "",q)
	if err != nil {
		log.Println(err)
		posts = []model.Post{}
	}
	fromDate  :=custom_type.NullTime{Valid:false}
	hashtags, err := model.HashtagsSearch(&fromDate,q)
	if err != nil {
		log.Println(err)
		hashtags = []model.Hashtag{}
	}

	// Display the view
	v := view.New(r)
	v.Vars["posts"] = posts
	v.Vars["hashtags"] = hashtags
	v.Vars["pageNum"] = pageNum

	v.Vars["nextPageURL"] = ""
	v.Vars["previousPageURL"] = ""
	v.Vars["nextPageURLForJson"] = ""
	v.Vars["previousPageURLForJson"] = ""
	urlBase := stringhelpers.FastConcat([]string{"/search/", sort, "/", q, "/"})
	v.Vars["thisPageURL"] = stringhelpers.FastConcat([]string{urlBase, strconv.Itoa(pageNum)})
	if(!isLastPage){


		//Next and previous page urls for infinite scroll SEO


		nextPage := pageNum + 1
		next := strconv.Itoa(nextPage)
		v.Vars["nextPageURL"] = stringhelpers.FastConcat([]string{urlBase, next})
		v.Vars["nextPageURLForJson"] = stringhelpers.FastConcat([]string{v.Vars["nextPageURL"].(string), "?type=json"})
	}

	previousPage := pageNum - 1
		if previousPage > 0 {
			prev := strconv.Itoa(previousPage)
			v.Vars["previousPageURL"] = stringhelpers.FastConcat([]string{urlBase, prev})
			v.Vars["previousPageURLForJson"] =  stringhelpers.FastConcat([]string{v.Vars["previousPageURL"].(string), "?type=json"})
		}

	if strings.ToLower(r.Header.Get("X-Requested-With")) == "xmlhttprequest" {
		//AJAX Request
		v.Name = "partial/search"
		result := v.RenderSingle(w,true)
		finalResult := JsonResult{
			Response: result,
			Next_data_url: v.Vars["nextPageURLForJson"].(string),
			Prev_data_url: v.Vars["previousPageURLForJson"].(string),
		}
		//w.Header().Set("Content-Type", "application/json")

		json.NewEncoder(w).Encode(finalResult)
	} else {

		v.Name = "search/list"
		v.Vars["pagetitle"] = stringhelpers.FastConcat([]string{localize.GetInstance().TranslateFunc("search") , " : " ,   q})

		v.Render(w)
	}

}



