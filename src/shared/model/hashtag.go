package model

import (

	"topsocial/src/shared/database"
	"topsocial/src/shared/stringhelpers"
	"topsocial/src/shared/custom_type"
	"topsocial/src/shared/pagination"

	//"log"
	"strings"
	//"log"
)

type Hashtag struct {
	Hashtag               	string   `json:"hashtag,omitempty"`
	Rank	          	float64  `json:"rank,omitempty"`
}


func HashtagsSearch(fromDate *custom_type.NullTime, q string) ([]Hashtag, error) {
	var err error
	var result []Hashtag

	if database.CheckConnection() {
		vars := make(map[string]interface {})

		vars["limit"] = 5
		vars["q"] = q

		filterQuery :=""
		filterParts := []string{}
		if fromDate.Valid {
			filterParts = append(filterParts,` i.source_date > @fromdate `)
			vars["fromdate"] = fromDate.Time.Unix()
		}

		searchString:=strings.TrimSpace(q)
		searchString = strings.Replace(searchString," ","\\_",1)
		if searchString!= "" && len(searchString) > 0  {
			filterParts = append(filterParts, ` i.hashtag LIKE @q  `)
			vars["q"] = "%" + searchString + "%"
		}


		if len(filterParts) > 0 {
			filterQuery = " FILTER "+ stringhelpers.FastConcat(filterParts)
		}




		queryParts := []string{
			`
			FOR i IN Hashtags `,
			filterQuery,
			`
			LIMIT @limit RETURN i
			`,
		}
		queryText :=stringhelpers.FastConcat(queryParts)

		//log.Println(queryText)
		cursor, err := database.ExecuteQuery(database.DB_TopSocial, queryText, vars)
		if err != nil {
			return []Hashtag{}, err
		}

		cursor.FetchBatch(&result)
	}
	return result, standardizeError(err)
}



func RecentPopularHashtags(fromDate *custom_type.NullTime, pageNum int,pageSize int)  ([]Hashtag, error, bool){
	var err error
	var result []Hashtag

	if database.CheckConnection() {
		limit, skip := pagination.PaginateParams(pageSize,pageNum)
		vars := make(map[string]interface {})

		vars["limit"] = limit
		vars["skip"] = skip

		filterQuery :=""
		filterParts := []string{}
		if fromDate.Valid {
			filterParts = append(filterParts,` i.source_date > @fromdate `)
			vars["fromdate"] = fromDate.Time.Unix()
		}
		if len(filterParts) > 0 {
			filterQuery = " FILTER "+ stringhelpers.FastConcat(filterParts)
		}


		queryParts := []string{
			`
			FOR i IN RecentPopularHashtagsCache `,
			filterQuery,
			`
			LIMIT @skip, @limit RETURN i
			`,
		}
		queryText :=stringhelpers.FastConcat(queryParts)


		cursor, err := database.ExecuteQuery(database.DB_TopSocial, queryText, vars)
		if err != nil {
			return []Hashtag{}, err,true
		}

		cursor.FetchBatch(&result)
	}
	return result, standardizeError(err) , len(result) < pageSize
}

func UpdateTotalHashtags() error{
	var err error
	if database.CheckConnection() {
		vars := make(map[string]interface {})

		//vars["limit"] = limit
		//
		////filterQuery :=""
		//filterParts := []string{}
		//if fromDate.Valid {
		//	filterParts = append(filterParts,` i.source_date > @fromdate `)
		//	vars["fromdate"] = fromDate.Time.Unix()
		//}
		//if len(filterParts) > 0 {
		//	filterQuery = " FILTER "+ stringhelpers.FastConcat(filterParts)
		//}

		queryParts := []string{
			`
			    FOR p IN Posts
			    FOR t in p.hashtags
			    COLLECT groupedTag = t INTO g

			    LET dates = (FOR tt IN g
			    COLLECT daydate = CEIL(tt.p.source_date_tehran/1000000)
			    AGGREGATE totalday = LENGTH(1)
			    return {day: daydate, totaldacy:totalday  } )

			    UPSERT { hashtag: groupedTag  }
			    INSERT { hashtag: groupedTag , dates: dates , count: COUNT(g) }
			    UPDATE { hashtag: groupedTag , dates: dates , count: COUNT(g) } IN Hashtags
  			 `,

		}

		queryText :=stringhelpers.FastConcat(queryParts)


		_, err := database.ExecuteQuery(database.DB_TopSocial, queryText, vars)
		if err != nil {
			return err
		}

	}
	return  err
}

func UpdateRecentPopularHashtags(fromDate custom_type.NullTime, limit int)  error{
	var err error
	//var result []Hashtag

	if database.CheckConnection() {
		vars := make(map[string]interface {})

		vars["limit"] = limit

		filterQuery :=""
		filterParts := []string{}
		if fromDate.Valid {
			filterParts = append(filterParts,` i.source_date > @fromdate `)
			vars["fromdate"] = fromDate.Time.Unix()
		}
		if len(filterParts) > 0 {
			filterQuery = " FILTER "+ stringhelpers.FastConcat(filterParts)
		}


		queryParts := []string{
			`
			LET timestamp = DATE_NOW()
			FOR i in Posts
			`,
			filterQuery,
			`
			FOR tag in i.hashtags
				LET tagandrank = {
				"hash":tag,
				"rank":(i.comments_count+i.likes_count),
				"coef":(((DATE_NOW()/1000)-i.source_date)/10080)
				}
			    COLLECT hashtag = tagandrank.hash
			    AGGREGATE rank = SUM(tagandrank.rank)
			SORT rank DESC
			LIMIT @limit
			UPSERT { hashtag : hashtag }
			INSERT { hashtag : hashtag, rank:rank, timestamp : timestamp }
			UPDATE { rank:rank, timestamp : timestamp } IN RecentPopularHashtagsCache
			`,
		}
		queryText :=stringhelpers.FastConcat(queryParts)
		//log.Fatal(queryText)
		_, err := database.ExecuteQuery(database.DB_TopSocial, queryText, vars)
		if err != nil {
			return err
		}

	}
	return standardizeError(err)
}

func RemoveOldRecentPopularHashtags() error {
	var err error
	if database.CheckConnection() {
		vars := make(map[string]interface {})

		//vars["limit"] = limit
		//
		////filterQuery :=""
		//filterParts := []string{}
		//if fromDate.Valid {
		//	filterParts = append(filterParts,` i.source_date > @fromdate `)
		//	vars["fromdate"] = fromDate.Time.Unix()
		//}
		//if len(filterParts) > 0 {
		//	filterQuery = " FILTER "+ stringhelpers.FastConcat(filterParts)
		//}

		queryParts := []string{
			`
			FOR xx IN RecentPopularHashtagsCache
			COLLECT AGGREGATE max = MAX(xx.timestamp)
			FOR r In RecentPopularHashtagsCache
			FILTER r.timestamp != max
			REMOVE {_key:r._key} IN RecentPopularHashtagsCache`,

		}

		queryText :=stringhelpers.FastConcat(queryParts)


		_, err := database.ExecuteQuery(database.DB_TopSocial, queryText, vars)
		if err != nil {
			return err
		}

	}
	return standardizeError(err)
}
