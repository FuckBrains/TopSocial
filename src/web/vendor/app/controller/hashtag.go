package controller

import (
	"app/shared/view"
	"strconv"
	"topsocial/src/shared/stringhelpers"
	"strings"
	"encoding/json"
	"net/http"
	"github.com/julienschmidt/httprouter"
	"topsocial/src/shared/custom_type"
	"topsocial/src/shared/model"
	"log"
	"github.com/gorilla/context"
	"app/routelink"
	"time"
)




func RecentPopularHashtags(w http.ResponseWriter, r *http.Request) {
	// Get session
	var params httprouter.Params
	params = context.Get(r, "params").(httprouter.Params)
	spageNum := params.ByName("page")
	fromdatetimestamp := params.ByName("fromdate")
	pageNum, _ := strconv.Atoi(spageNum)

	if pageNum == 0 {
		pageNum = 1
	}
	fromDate := custom_type.NullTime{Valid:false}
	if(fromdatetimestamp != "1"){
		long,_ :=strconv.ParseInt(fromdatetimestamp, 10, 64)
		fromDate = custom_type.NullTime{Valid:true, Time: time.Unix(long,0)}
	}

	hashtags, err, isLastPage := model.RecentPopularHashtags(&fromDate, pageNum, 20)
	if err != nil {
		log.Println(err)
		hashtags = []model.Hashtag{}
	}

	// Display the view
	v := view.New(r)
	v.Vars["hashtags"] = hashtags
	v.Vars["pageNum"] = pageNum

	v.Vars["nextPageURL"] = ""
	v.Vars["previousPageURL"] = ""
	v.Vars["nextPageURLForJson"] = ""
	v.Vars["previousPageURLForJson"] = ""
	//urlBase := stringhelpers.FastConcat([]string{"/posts/", sort, "/", hashtag, "/"})
	v.Vars["thisPageURL"] = routelink.RecentHashtagsList("",1,pageNum) // stringhelpers.FastConcat([]string{urlBase, strconv.Itoa(pageNum)})
	if(!isLastPage){
		nextPage := pageNum + 1
		//next := strconv.Itoa(nextPage)
		v.Vars["nextPageURL"] = routelink.RecentHashtagsList("",1,nextPage) //stringhelpers.FastConcat([]string{urlBase, next})
		v.Vars["nextPageURLForJson"] = stringhelpers.FastConcat([]string{v.Vars["nextPageURL"].(string), "?type=json"})
	}

	previousPage := pageNum - 1
		if previousPage > 0 {
			//prev := strconv.Itoa(previousPage)
			v.Vars["previousPageURL"] = routelink.RecentHashtagsList("",1,previousPage) //stringhelpers.FastConcat([]string{urlBase, prev})
			v.Vars["previousPageURLForJson"] =  stringhelpers.FastConcat([]string{v.Vars["previousPageURL"].(string), "?type=json"})
		}

	if strings.ToLower(r.Header.Get("X-Requested-With")) == "xmlhttprequest" {
		//AJAX Request
		v.Name = "partial/hashtags"
		result := v.RenderSingle(w,true)
		finalResult := JsonResult{
			Response: result,
			Next_data_url: v.Vars["nextPageURLForJson"].(string),
			Prev_data_url: v.Vars["previousPageURLForJson"].(string),
		}
		//w.Header().Set("Content-Type", "application/json")

		json.NewEncoder(w).Encode(finalResult)
	} else {

		v.Name = "hashtag/list"


		v.Render(w)
	}

}