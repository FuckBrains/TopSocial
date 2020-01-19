package stringhelpers
import (
    "bytes"
    //"strings"
    //"testing"
)


func FastConcat(val []string) string{
	if len(val) == 0 {
		return  ""
	}

	var buffer bytes.Buffer
	for i :=0 ; i < len(val);i++{
		buffer.WriteString(val[i])
	}
	return  buffer.String()

	//See later:     http://stackoverflow.com/questions/1760757/how-to-efficiently-concatenate-strings-in-go
}
