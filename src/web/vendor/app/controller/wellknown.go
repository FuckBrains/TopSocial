package controller

import (
	"net/http"
	"strings"
	"topsocial/src/shared/conf"
	"os"
)

// Static maps static files
func Wellknown(w http.ResponseWriter, r *http.Request) {
	// Disable listing directories
	if strings.HasSuffix(r.URL.Path, "/") {
		Error404(w, r)
		return
	}
	//http.ServeFile(w, r, r.URL.Path[1:])
	file := strings.Replace(r.URL.Path,"/.well-known","",1)
	http.ServeFile(w, r, conf.GetInstance().Absolute_Path_ROOT+string(os.PathSeparator)+"web"+string(os.PathSeparator)+".well-known"+string(os.PathSeparator)+file)
}
