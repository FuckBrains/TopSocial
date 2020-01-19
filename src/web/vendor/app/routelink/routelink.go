package routelink

import (

	"app/shared/view"
	"strconv"
	"strings"
	"html/template"

	"topsocial/src/shared/stringhelpers"
	"topsocial/src/shared/conf"
)



func LinkHelper(v view.View) template.FuncMap{
	f := make(template.FuncMap)


	f["URL_PostList"] = func(sort, hashtag string , page int) template.HTML {
		return template.HTML(PostList(v.BaseURI,sort, hashtag, page))
	}

	f["URL_PostDetail"] = func(id,seourlparam string) template.HTML {
		return template.HTML(PostDetail(v.BaseURI,id,seourlparam))
	}

	f["URL_PostExternalUrl"] = func(id string, index int) template.HTML {
		return template.HTML(PostExternalUrl("http://www.topsocial.com/" ,id,index))
	}

	f["URL_RecentPostList"] = func(fromdate int64, mediatype int, page int) template.HTML {
		return template.HTML(RecentPostList(v.BaseURI, fromdate, mediatype, page))
	}

	f["URL_RecentHashtagsList"] = func( fromdate int64, page int) template.HTML {
		return template.HTML(RecentHashtagsList(v.BaseURI, fromdate, page))
	}

	f["URL_Search"] = func( q string, page int) template.HTML {
		return template.HTML(Search(v.BaseURI, q, page))
	}



	return f

}

func PostList(baseUri,sort, hashtag string , page int) string{
	if(baseUri == "") {
		baseUri = conf.GetInstance().Base_Uri
	}
	if page == 0 {
		page = 1
	}
	if len(strings.Trim(hashtag,"")) == 0 {
		hashtag = "all"
	}

	return stringhelpers.FastConcat([]string{baseUri,"posts/",sort,"/",hashtag,"/", strconv.Itoa(page)})
}

func RecentPostList(baseUri string, fromdate int64, mediatype, page int) string{
	if(baseUri == "") {
		baseUri = conf.GetInstance().Base_Uri
	}
	if page == 0 {
		page = 1
	}

	return stringhelpers.FastConcat([]string{baseUri,"recentpopularposts/",strconv.FormatInt(fromdate,10),"/",strconv.Itoa(mediatype),"/", strconv.Itoa(page)})
}

func RecentHashtagsList(baseUri string, fromdate int64, page int) string{
	if(baseUri == "") {
		baseUri = conf.GetInstance().Base_Uri
	}
	if page == 0 {
		page = 1
	}

	return stringhelpers.FastConcat([]string{baseUri,"recentpopularhashtags/",strconv.FormatInt(fromdate,10),"/", strconv.Itoa(page)})
}




func PostDetail(baseUri, id , seourlparam string) string{
	if(baseUri == "") {
		baseUri = conf.GetInstance().Base_Uri
	}
	return stringhelpers.FastConcat([]string{baseUri,"post/",seourlparam,"/",id})
}

func PostExternalUrl(baseUri, id  string, index int) string{
	if(baseUri == "") {
		baseUri = conf.GetInstance().Base_Uri
	}
	strIndex := strconv.Itoa(index)
	return stringhelpers.FastConcat([]string{baseUri,"postexturl/",id,"/",strIndex})
}


func Search(baseUri, q string, page int) string{
	if(baseUri == "") {
		baseUri = conf.GetInstance().Base_Uri
	}
	return stringhelpers.FastConcat([]string{baseUri,"search/",q,"/",strconv.Itoa(page)})
}