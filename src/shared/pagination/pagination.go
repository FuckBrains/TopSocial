package pagination
import (
	//"strconv"
)

type pagination struct {
	Per, Page, PrevPage, NextPage, LastPage, Count int
}

//var defaultPer = 20

func PaginateParams(per, page int) (perPage, offset int) {

	if(page == 0){
		page = 1
	}

	perPage = per
	offset = per * (page - 1)
	return perPage, offset
}

func (p pagination) HideFirstLink() bool {
	return p.Page <= 1
}

func (p pagination) HideLastLink() bool {
	return p.Page >= p.LastPage
}