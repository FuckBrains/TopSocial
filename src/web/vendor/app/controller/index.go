package controller

import (
	"net/http"

	"app/shared/session"
	"app/shared/view"
	"topsocial/src/shared/model"
	"topsocial/src/shared/enum"
	"topsocial/src/shared/custom_type"
)

// IndexGET displays the home page
func IndexGET(w http.ResponseWriter, r *http.Request) {
	// Get session
	session := session.Instance(r)
	// Display the view
	v := view.New(r)
	fromDate := custom_type.NullTime{Valid:false}
	v.Vars["bannerposts"],_,_ = model.RecentPopularPosts(&fromDate, 1, 10, enum.PostType_Image)
	fromdate := custom_type.NullTime{ Valid:false}
	v.Vars["popularhashtags"],_,_ = model.RecentPopularHashtags(&fromdate, 1, 40)
	if session.Values["id"] != nil {
		v.Name = "index/auth"
		v.Vars["first_name"] = session.Values["first_name"]
		v.Render(w)
	} else {

		v.Name = "index/anon"
		v.Render(w)
		return
	}
}
