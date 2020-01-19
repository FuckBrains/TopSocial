package controller

import (
	"app/shared/conf"
	"net/http"
	"os"
	"strings"
)

// Static maps static files
func Static(w http.ResponseWriter, r *http.Request) {
	// Disable listing directories
	if strings.HasSuffix(r.URL.Path, "/") {
		Error404(w, r)
		return
	}
	w.Header().Set("Access-Control-Allow-Origin", "*")
	http.ServeFile(w, r, conf.GetInstance().Absolute_Path_ROOT+string(os.PathSeparator)+"cdn"+string(os.PathSeparator)+r.URL.Path[1:])
}
