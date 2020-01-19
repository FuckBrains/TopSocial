package controller

import (
	//"fmt"
	"log"
	"net/http"


	//"app/shared/session"
	"app/shared/view"

	"github.com/gorilla/context"
	////"github.com/josephspurrier/csrfbanana"
	////"github.com/julienschmidt/httprouter"
	//"github.com/julienschmidt/httprouter"
	//"strconv"
	"github.com/julienschmidt/httprouter"
	"strconv"

	"strings"
	"encoding/json"
	"topsocial/src/shared/stringhelpers"
	"topsocial/src/shared/model"
	"topsocial/src/shared/custom_type"
	"app/routelink"
	"time"
	"topsocial/src/shared/enum"
	"app/shared/localize"
)


type JsonResult struct  {
	Response	string
	Next_data_url	string
	Prev_data_url	string

}

// NotepadReadGET displays the notes in the post
func PostListGET(w http.ResponseWriter, r *http.Request) {

	// Get session
	var params httprouter.Params
	params = context.Get(r, "params").(httprouter.Params)
	sort := params.ByName("sort")
	hashtag := params.ByName("hashtag")
	spageNum := params.ByName("page")
	pageNum, _ := strconv.Atoi(spageNum)

	if pageNum == 0 {
		pageNum = 1
	}

	posts, err, isLastPage := model.PostsSearch(sort, pageNum, hashtag,"")
	if err != nil {
		log.Println(err)
		posts = []model.Post{}
	}

	// Display the view
	v := view.New(r)
	v.Vars["posts"] = posts
	v.Vars["pageNum"] = pageNum

	v.Vars["nextPageURL"] = ""
	v.Vars["previousPageURL"] = ""
	v.Vars["nextPageURLForJson"] = ""
	v.Vars["previousPageURLForJson"] = ""

	urlBase := stringhelpers.FastConcat([]string{"/posts/", sort, "/", hashtag, "/"})

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
		v.Name = "partial/posts"
		result := v.RenderSingle(w,true)
		finalResult := JsonResult{
			Response: result,
			Next_data_url: v.Vars["nextPageURLForJson"].(string),
			Prev_data_url: v.Vars["previousPageURLForJson"].(string),
		}
		//w.Header().Set("Content-Type", "application/json")

		json.NewEncoder(w).Encode(finalResult)
	} else {

		v.Name = "post/list"
		v.Vars["pagetitle"] = stringhelpers.FastConcat([]string{localize.GetInstance().TranslateFunc("posts_" + sort) , " " ,   hashtag})

		v.Render(w)
	}



}




func PostDetailGet(w http.ResponseWriter, r *http.Request)  {
	var params httprouter.Params
	params = context.Get(r, "params").(httprouter.Params)
	_key := params.ByName("id")

	post,err:= model.PostByID(_key)
	if(err != nil) {
	}

	v := view.New(r)
	//ccc := post.Urls_Extracted[0]
	//println(ccc.Url)
	v.Name = "post/postdetail"
	v.Vars["post"] = post
	v.Vars["media_padding_top"] = 60
	if post.Media_Aspect_Ratio < 0.8{
		v.Vars["media_padding_top"] = 100 / post.Media_Aspect_Ratio
	}

	v.Render(w)
}



func RecentPopularPosts(w http.ResponseWriter, r *http.Request) {
	// Get session
	var params httprouter.Params
	params = context.Get(r, "params").(httprouter.Params)
	spageNum := params.ByName("page")
	mediaType , _:= strconv.Atoi(params.ByName("mediatype"))
	fromdatetimestamp := params.ByName("fromdate")
	pageNum, _ := strconv.Atoi(spageNum)

	if pageNum == 0 {
		pageNum = 1
	}
	fromDate := custom_type.NullTime{Valid:false}
	fromdatetimestamplong,_ :=strconv.ParseInt(fromdatetimestamp, 10, 64)
	if(fromdatetimestamp != "1"){

		fromDate = custom_type.NullTime{Valid:true, Time: time.Unix(fromdatetimestamplong,0)}
	}

	pageSize:= 10
	if mediaType == enum.PostType_Video{
		pageSize = 4
	}
	posts, err, isLastPage := model.RecentPopularPosts(&fromDate, pageNum, pageSize, mediaType)
	if err != nil {
		log.Println(err)
		posts = []model.Post{}
	}

	// Display the view
	v := view.New(r)
	v.Vars["posts"] = posts
	v.Vars["pageNum"] = pageNum
	v.Vars["fromdate"] = fromdatetimestamplong
	v.Vars["mediatype"] = mediaType

	v.Vars["nextPageURL"] = ""
	v.Vars["previousPageURL"] = ""
	v.Vars["nextPageURLForJson"] = ""
	v.Vars["previousPageURLForJson"] = ""
	//urlBase := stringhelpers.FastConcat([]string{"/posts/", sort, "/", hashtag, "/"})
	v.Vars["thisPageURL"] = routelink.RecentPostList("",1,mediaType,pageNum) // stringhelpers.FastConcat([]string{urlBase, strconv.Itoa(pageNum)})
	if(!isLastPage){
		nextPage := pageNum + 1
		//next := strconv.Itoa(nextPage)
		v.Vars["nextPageURL"] = routelink.RecentPostList("",1,mediaType,nextPage) //stringhelpers.FastConcat([]string{urlBase, next})
		v.Vars["nextPageURLForJson"] = stringhelpers.FastConcat([]string{v.Vars["nextPageURL"].(string), "?type=json"})
	}

	previousPage := pageNum - 1
		if previousPage > 0 {
			//prev := strconv.Itoa(previousPage)
			v.Vars["previousPageURL"] = routelink.RecentPostList("",1,mediaType,previousPage) //stringhelpers.FastConcat([]string{urlBase, prev})
			v.Vars["previousPageURLForJson"] =  stringhelpers.FastConcat([]string{v.Vars["previousPageURL"].(string), "?type=json"})
		}

	if strings.ToLower(r.Header.Get("X-Requested-With")) == "xmlhttprequest" {
		//AJAX Request
		v.Name = "partial/postshorizontal"
		if mediaType == enum.PostType_Video{
			v.Name = "partial/postsvertical"
		}

		result:=""
		if (len(posts) > 0) {
			result = v.RenderSingle(w,true)
		}

		finalResult := JsonResult{
			Response: result,
			Next_data_url: v.Vars["nextPageURLForJson"].(string),
			Prev_data_url: v.Vars["previousPageURLForJson"].(string),
		}
		//w.Header().Set("Content-Type", "application/json")

		json.NewEncoder(w).Encode(finalResult)
	} else {

		v.Name = "post/list"


		v.Render(w)
	}

}

// NotepadReadGET displays the notes in the post
//func PostReadGET(w http.ResponseWriter, r *http.Request) {
//	// Get session
//	sess := session.Instance(r)
//
//	userID := fmt.Sprintf("%s", sess.Values["id"])
//
//	notes, err := model.PostsByUserID(userID)
//	if err != nil {
//		log.Println(err)
//		notes = []model.Post{}
//	}
//
//	// Display the view
//	v := view.New(r)
//	v.Name = "post/read"
//	v.Vars["first_name"] = sess.Values["first_name"]
//	v.Vars["notes"] = notes
//	v.Render(w)
//}

//// NotepadCreateGET displays the note creation page
//func NotepadCreateGET(w http.ResponseWriter, r *http.Request) {
//	// Get session
//	sess := session.Instance(r)
//
//	// Display the view
//	v := view.New(r)
//	v.Name = "post/create"
//	v.Vars["token"] = csrfbanana.Token(w, r, sess)
//	v.Render(w)
//}
//
//// NotepadCreatePOST handles the note creation form submission
//func NotepadCreatePOST(w http.ResponseWriter, r *http.Request) {
//	// Get session
//	sess := session.Instance(r)
//
//	// Validate with required fields
//	if validate, missingField := view.Validate(r, []string{"note"}); !validate {
//		sess.AddFlash(view.Flash{"Field missing: " + missingField, view.FlashError})
//		sess.Save(r, w)
//		NotepadCreateGET(w, r)
//		return
//	}
//
//	// Get form values
//	content := r.FormValue("note")
//
//	userID := fmt.Sprintf("%s", sess.Values["id"])
//
//	// Get database result
//	err := model.PostCreate(content, userID)
//	// Will only error if there is a problem with the query
//	if err != nil {
//		log.Println(err)
//		sess.AddFlash(view.Flash{"An error occurred on the server. Please try again later.", view.FlashError})
//		sess.Save(r, w)
//	} else {
//		sess.AddFlash(view.Flash{"Note added!", view.FlashSuccess})
//		sess.Save(r, w)
//		http.Redirect(w, r, "/post", http.StatusFound)
//		return
//	}
//
//	// Display the same page
//	NotepadCreateGET(w, r)
//}
//
//// NotepadUpdateGET displays the note update page
//func NotepadUpdateGET(w http.ResponseWriter, r *http.Request) {
//	// Get session
//	sess := session.Instance(r)
//
//	// Get the note id
//	var params httprouter.Params
//	params = context.Get(r, "params").(httprouter.Params)
//	noteID := params.ByName("id")
//
//	userID := fmt.Sprintf("%s", sess.Values["id"])
//
//	// Get the note
//	note, err := model.PostByID(userID, noteID)
//	if err != nil { // If the note doesn't exist
//		log.Println(err)
//		sess.AddFlash(view.Flash{"An error occurred on the server. Please try again later.", view.FlashError})
//		sess.Save(r, w)
//		http.Redirect(w, r, "/post", http.StatusFound)
//		return
//	}
//
//	// Display the view
//	v := view.New(r)
//	v.Name = "post/update"
//	v.Vars["token"] = csrfbanana.Token(w, r, sess)
//	v.Vars["note"] = note.Content
//	v.Render(w)
//}
//
//// NotepadUpdatePOST handles the note update form submission
//func NotepadUpdatePOST(w http.ResponseWriter, r *http.Request) {
//	// Get session
//	sess := session.Instance(r)
//
//	// Validate with required fields
//	if validate, missingField := view.Validate(r, []string{"note"}); !validate {
//		sess.AddFlash(view.Flash{"Field missing: " + missingField, view.FlashError})
//		sess.Save(r, w)
//		NotepadUpdateGET(w, r)
//		return
//	}
//
//	// Get form values
//	content := r.FormValue("note")
//
//	userID := fmt.Sprintf("%s", sess.Values["id"])
//
//	var params httprouter.Params
//	params = context.Get(r, "params").(httprouter.Params)
//	noteID := params.ByName("id")
//
//	// Get database result
//	err := model.PostUpdate(content, userID, noteID)
//	// Will only error if there is a problem with the query
//	if err != nil {
//		log.Println(err)
//		sess.AddFlash(view.Flash{"An error occurred on the server. Please try again later.", view.FlashError})
//		sess.Save(r, w)
//	} else {
//		sess.AddFlash(view.Flash{"Note updated!", view.FlashSuccess})
//		sess.Save(r, w)
//		http.Redirect(w, r, "/post", http.StatusFound)
//		return
//	}
//
//	// Display the same page
//	NotepadUpdateGET(w, r)
//}
//
//// NotepadDeleteGET handles the note deletion
//func NotepadDeleteGET(w http.ResponseWriter, r *http.Request) {
//	// Get session
//	sess := session.Instance(r)
//
//	userID := fmt.Sprintf("%s", sess.Values["id"])
//
//	var params httprouter.Params
//	params = context.Get(r, "params").(httprouter.Params)
//	noteID := params.ByName("id")
//
//	// Get database result
//	err := model.PostDelete(userID, noteID)
//	// Will only error if there is a problem with the query
//	if err != nil {
//		log.Println(err)
//		sess.AddFlash(view.Flash{"An error occurred on the server. Please try again later.", view.FlashError})
//		sess.Save(r, w)
//	} else {
//		sess.AddFlash(view.Flash{"Note deleted!", view.FlashSuccess})
//		sess.Save(r, w)
//	}
//
//	http.Redirect(w, r, "/post", http.StatusFound)
//	return
//}
