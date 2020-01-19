package plugin

import (
	"html/template"
	"log"

	"app/shared/cdnserver"
	"app/shared/view"
	"os"
	//"strconv"
	"strconv"

	"app/shared/localize"
	"app/shared/datehandler"

	"topsocial/src/shared/stringhelpers"
)

// TagHelper returns a template.FuncMap
// * JS returns JavaScript tag
// * CSS returns stylesheet tag
// * LINK returns hyperlink tag
func TagHelper(v view.View, cdnServer cdnserver.Server) template.FuncMap {
	f := make(template.FuncMap)

	f["JS"] = func(s string) template.HTML {
		_, err := v.AssetTimePath("cdn" + string(os.PathSeparator) + s)

		if err != nil {
			log.Println("JS Error:", err)
			return template.HTML("<!-- JS Error: " + s + " -->")
		}

		return template.HTML(`<script type="text/javascript" src="` + cdnServer.AbsoluteURL + "/" + s + `"></script>`)
	}

	f["CSS"] = func(s string) template.HTML {
		_, err := v.AssetTimePath("cdn" + string(os.PathSeparator) + s)

		if err != nil {
			log.Println("CSS Error:", err)
			return template.HTML("<!-- CSS Error: " + s + " -->")
		}

		return template.HTML(`<link rel="stylesheet" type="text/css" href="` + cdnServer.AbsoluteURL + "/" + s + `" />`)
	}

	f["LINK"] = func(path, name string) template.HTML {
		return template.HTML(`<a href="` + v.PrependBaseURI(path) + `">` + name + `</a>`)
	}

	f["ABSURL"] = func(path string) template.HTML {
		return template.HTML(cdnserver.AbsoluteUrl(path))
	}

	f["DEVIDE"] = func(first,second float64) template.HTML {
		return template.HTML(strconv.FormatFloat(first / second,'f', 6, 64))
	}

	f["ABSTRACT"] = func(text string, chars int) template.HTML {

		tosubstring := chars
		if len(text) < chars{
			tosubstring = len(text)
		}
		return template.HTML(stringhelpers.FastConcat([]string{text[0:tosubstring]," ..."}))
	}

	f["TIMEAGO"] = func(epochDate float64) string {

		return datehandler.TimeAgo(epochDate)
	}


	f["T"] =  localize.GetInstance().TranslateFunc



	//func(first,second float64)  i18n.TranslateFunc {
	//	return localize.GetInstance().TranslateFunc
	//}

	return f
}


