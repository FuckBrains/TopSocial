package model

import (
	"log"
	"strings"
	"topsocial/src/shared/stringhelpers"
	"topsocial/src/shared/database"
	"topsocial/src/shared/enum"
	"topsocial/src/shared/pagination"
	"topsocial/src/shared/custom_type"
)

// *****************************************************************************
// Note
// *****************************************************************************

// Note table contains the information for each note
type Post struct {
	Key               	string   `json:"_key,omitempty"`
	Date_Set          	float64  `json:"date_set,omitempty"`
	Date_LastModified 	float64  `json:"date_last_modif,omitempty"`

	Comments_Count    	int      `json:"comments_count,omitempty"`
	Likes_Count       	int64    `json:"likes_count,omitempty"`
	Title              	string   `json:"title,omitempty"`
	Body              	string   `json:"body,omitempty"`
	Hashtags          	[]string `json:"hashtags,omitempty"`
	Media_Type         	int	 `json:"media_type,omitempty"`
	Media_Url         	string   `json:"media_url,omitempty"`
	Media_Aspect_Ratio 	float64  `json:"media_aspect_ratio,omitempty"`
	Media_Width		float32  `json:"media_width,omitempty"`
	Media_Height		float32  `json:"media_height,omitempty"`
	Thumbnail		struct{
		Image_Url		string	 `json:"image_url,omitempty"`
		Image_Width		float64	 `json:"image_width,omitempty"`
		Image_Height		float64	 `json:"image_Height,omitempty"`
		Image_Aspect_Ratio	float64	 `json:"image_aspect_ratio,omitempty"`
	} `json:"thumbnail,omitempty"`
	Source_Date     	float64  `json:"source_date,omitempty"`
	Source_Owner_Title     	string   `json:"source_owner_title,omitempty"`
	Urls_Extracted   	[]struct{
		State		int	 `json:"state,omitempty"`
		Url		string	 `json:"url,omitempty"`
	}   `json:"urls_extracted,omitempty"`
	Seo_Dashed_Url     	string   `json:"seo_dashed_url,omitempty"`
	Owner_Id          	string   `json:"ownerid,omitempty"`
}



// NoteID returns the note id
func (u *Post) PostID() string {
	r := u.Key

	//switch database.ReadConfig().Type {
	//case database.TypeMySQL:
	//	r = fmt.Sprintf("%v", u.ID)
	//case database.TypeMongoDB:
	//	r = u.ObjectID.Hex()
	//case database.TypeBolt:
	//	r = u.ObjectID.Hex()
	//}

	return r
}

// NoteByID gets note by ID
func PostByID(_key string ) (Post, error) {
	var err error

	result := Post{}

	if database.CheckConnection() {
		vars := make(map[string]interface {})
		vars["postid"] =_key
		queryText :=
			`
		FOR i in Posts
		FILTER  i._key == @postid
		RETURN i
		`

		cursor, err := database.ExecuteQuery(database.DB_TopSocial, queryText, vars)
		if err != nil {
			return Post{}, err
		}

		cursor.FetchOne(&result)

	}

	//switch database.ReadConfig().Type {
	//case database.TypeMySQL:
	//	err = database.SQL.Get(&result, "SELECT id, content, user_id, created_at, updated_at, deleted FROM note WHERE id = ? AND user_id = ? LIMIT 1", noteID, userID)
	//case database.TypeMongoDB:
	//	if database.CheckConnection() {
	//		// Create a copy of mongo
	//		session := database.Mongo.Copy()
	//		defer session.Close()
	//		c := session.DB(database.ReadConfig().MongoDB.Database).C("note")
	//
	//		// Validate the object id
	//		if bson.IsObjectIdHex(noteID) {
	//			err = c.FindId(bson.ObjectIdHex(noteID)).One(&result)
	//			if result.UserID != bson.ObjectIdHex(userID) {
	//				result = Note{}
	//				err = ErrUnauthorized
	//			}
	//		} else {
	//			err = ErrNoResult
	//		}
	//	} else {
	//		err = ErrUnavailable
	//	}
	//case database.TypeBolt:
	//	err = database.View("note", userID+noteID, &result)
	//	if err != nil {
	//		err = ErrNoResult
	//	}
	//	if result.UserID != bson.ObjectIdHex(userID) {
	//		result = Note{}
	//		err = ErrUnauthorized
	//	}
	//default:
	//	err = ErrCode
	//}

	return result, standardizeError(err)
}

// NotesByUserID gets all notes for a user
func PostsByUserID(userID string) ([]Post, error) {
	var err error

	var result []Post

	if database.CheckConnection() {
		queryText := "FOR i in Users FILTER "
		//vars:= []struct {
		//    Obj  string
		//    Name string
		//}{
		//	{"user_key", userID},
		//}

		vars := make(map[string]interface {
		})

		cursor, err := database.ExecuteQuery(database.DB_TopSocial, queryText, vars)
		if err != nil {
			return []Post{}, err
		}

		for cursor.FetchOne(&result) {
			log.Println(result)
		}
	}

	//switch database.ReadConfig().Type {
	//case database.TypeMySQL:
	//	err = database.SQL.Select(&result, "SELECT id, content, user_id, created_at, updated_at, deleted FROM note WHERE user_id = ?", userID)
	//case database.TypeMongoDB:
	//	if database.CheckConnection() {
	//		// Create a copy of mongo
	//		session := database.Mongo.Copy()
	//		defer session.Close()
	//		c := session.DB(database.ReadConfig().MongoDB.Database).C("note")
	//
	//		// Validate the object id
	//		if bson.IsObjectIdHex(userID) {
	//			err = c.Find(bson.M{"user_id": bson.ObjectIdHex(userID)}).All(&result)
	//		} else {
	//			err = ErrNoResult
	//		}
	//	} else {
	//		err = ErrUnavailable
	//	}
	//case database.TypeBolt:
	//	// View retrieves a record set in Bolt
	//	err = database.BoltDB.View(func(tx *bolt.Tx) error {
	//		// Get the bucket
	//		b := tx.Bucket([]byte("note"))
	//		if b == nil {
	//			return bolt.ErrBucketNotFound
	//		}
	//
	//		// Get the iterator
	//		c := b.Cursor()
	//
	//		prefix := []byte(userID)
	//		for k, v := c.Seek(prefix); bytes.HasPrefix(k, prefix); k, v = c.Next() {
	//			var single Note
	//
	//			// Decode the record
	//			err := json.Unmarshal(v, &single)
	//			if err != nil {
	//				log.Println(err)
	//				continue
	//			}
	//
	//			result = append(result, single)
	//		}
	//
	//		return nil
	//	})
	//default:
	//	err = ErrCode
	//}

	return result, standardizeError(err)
}

func PostsSearch(sort string,pageNum int, hashTag ,q string) ([]Post, error, bool) {
	var err error
	var pageSize =20
	var result []Post

	if database.CheckConnection() {
		limit, skip := pagination.PaginateParams(pageSize,pageNum)
		vars := make(map[string]interface {})

		sortQuery :=""
		switch sort {
			case enum.RecentPosts:
				sortQuery += ` SORT i.source_date desc `
			case enum.PopularPosts:
				sortQuery += ` SORT (i.likes_count + i.comments_count), i.source_date desc `
			default:
				sortQuery += ` SORT i.source_date desc `
		}


		vars["limit"] = limit
		vars["skip"] = skip

		collection:=" Posts "
		filterQuery :=""
		filterParts := []string{}
		hashTag = strings.TrimSpace(hashTag)
		if hashTag != "" && len(hashTag) > 0 && hashTag != enum.AllHashtags {
			filterParts = append(filterParts,` FILTER @hashtag IN  i.hashtags `)
			vars["hashtag"] = hashTag
		}

		searchString:=strings.TrimSpace(q)
		if searchString!= "" && len(searchString) > 0  {
			words:=strings.Split(searchString," ")
			fultextParams := strings.Join(words,",|")
			collection = "FULLTEXT('Posts','body', @q)"
			vars["q"] = fultextParams
		}

		filterQuery = stringhelpers.FastConcat(filterParts)

		queryParts := []string{
			" FOR i in  ",
			collection,
			filterQuery,
			sortQuery,
			" LIMIT @skip, @limit RETURN i ",
		}
		queryText :=stringhelpers.FastConcat(queryParts)


		cursor, err := database.ExecuteQuery(database.DB_TopSocial, queryText, vars)
		if err != nil {
			return []Post{}, err, true
		}

		cursor.FetchBatch(&result)
	}
	return result, standardizeError(err), len(result) < pageSize
}

func RecentPopularPosts(fromDate *custom_type.NullTime, pageNum int,pageSize int, mediaType int)([]Post, error, bool)  {
	var err error
	var result []Post

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
		collectionName :=""
		if mediaType != 0 {
			switch mediaType {
			case enum.PostType_Video:
				collectionName = " RecentPopularVideosCache "
				break;
			default:
				collectionName = " RecentPopularImagesCache "
			}
			//filterParts = append(filterParts,` i.media_type == @mediatype `)
			//vars["mediatype"] = mediaType
		}

		if len(filterParts) > 0 {
			filterQuery = " FILTER " + stringhelpers.FastConcat(filterParts)
		}

		queryParts := []string{
			`
			FOR i IN `,
			collectionName,
			filterQuery,
			`
			LIMIT @skip, @limit RETURN i
			`,
		}
		queryText :=stringhelpers.FastConcat(queryParts)
		//log.Println(queryText)

		cursor, err := database.ExecuteQuery(database.DB_TopSocial, queryText, vars)
		if err != nil {
			return []Post{}, err, true
		}

		cursor.FetchBatch(&result)
	}
	return result, standardizeError(err), len(result) < pageSize
}



func UpdateRecentPopularPosts(fromDate custom_type.NullTime, limit int, mediaType []int,destnationCollection string) error  {
	var err error
	//var result []Post

	if database.CheckConnection() {
		vars := make(map[string]interface {})

		vars["limit"] = limit

		filterQuery :=""
		filterParts := []string{}
		if fromDate.Valid {
			filterParts = append(filterParts,` p.source_date > @fromdate `)
			vars["fromdate"] = fromDate.Time.Unix()
		}
		if len(mediaType) > 0 {
			filterParts = append(filterParts,` p.media_type IN @mediatype `)
			vars["mediatype"] = mediaType
		}

		if len(filterParts) > 0 {
			filterQuery = " FILTER "+ strings.Join(filterParts," and ")
		}



		queryParts := []string{
			`
			LET timestamp = DATE_NOW()
			FOR p IN Posts
			`,
			filterQuery,
			`
			SORT  FLOOR(p.source_date_tehran/1000000) DESC ,(p.likes_count + p.comments_count) DESC
			LIMIT @limit
			UPSERT { _key : p._key }
			INSERT MERGE(p,{timestamp:timestamp})
			UPDATE {p,timestamp} IN
			`,
			destnationCollection,
		}
		queryText :=stringhelpers.FastConcat(queryParts)
		//log.Fatal(queryText)

		_, err := database.ExecuteQuery(database.DB_TopSocial, queryText, vars)
		if err != nil {
			return err
		}

		//cursor.FetchBatch(&result)
	}
	return  standardizeError(err)
}


func RemoveOldRecentPopularPosts(destnationCollection string) error {
	var err error
	if database.CheckConnection() {
		vars := make(map[string]interface {})

		//vars["limit"] = limit

		//filterQuery :=""
		//filterParts := []string{}
		//if fromDate.Valid {
		//	filterParts = append(filterParts,` p.source_date > @fromdate `)
		//	vars["fromdate"] = fromDate.Unix()
		//}
		//if len(filterParts) > 0 {
		//	filterQuery = " FILTER "+ stringhelpers.FastConcat(filterParts)
		//}


		queryParts := []string{
			`
			FOR xx IN `,
			destnationCollection,
			`
			COLLECT AGGREGATE max = MAX(xx.timestamp)
			FOR r In `,
			destnationCollection,
			`
			FILTER r.timestamp != max
			REMOVE {_key:r._key} IN `,
			destnationCollection,

		}
		queryText :=stringhelpers.FastConcat(queryParts)

		_, err := database.ExecuteQuery(database.DB_TopSocial, queryText, vars)
		if err != nil {
			return err
		}

	}
	return standardizeError(err)
}







// NoteCreate creates a note
func PostCreate(content string, userID string) error {
	var err error

	//now := time.Now()

	//switch database.ReadConfig().Type {
	//case database.TypeMySQL:
	//	_, err = database.SQL.Exec("INSERT INTO note (content, user_id) VALUES (?,?)", content, userID)
	//case database.TypeMongoDB:
	//	if database.CheckConnection() {
	//		// Create a copy of mongo
	//		session := database.Mongo.Copy()
	//		defer session.Close()
	//		c := session.DB(database.ReadConfig().MongoDB.Database).C("note")
	//
	//		note := &Note{
	//			ObjectID:  bson.NewObjectId(),
	//			Content:   content,
	//			UserID:    bson.ObjectIdHex(userID),
	//			CreatedAt: now,
	//			UpdatedAt: now,
	//			Deleted:   0,
	//		}
	//		err = c.Insert(note)
	//	} else {
	//		err = ErrUnavailable
	//	}
	//case database.TypeBolt:
	//	note := &Note{
	//		ObjectID:  bson.NewObjectId(),
	//		Content:   content,
	//		UserID:    bson.ObjectIdHex(userID),
	//		CreatedAt: now,
	//		UpdatedAt: now,
	//		Deleted:   0,
	//	}
	//
	//	err = database.Update("note", userID+note.ObjectID.Hex(), &note)
	//default:
	//	err = ErrCode
	//}

	return standardizeError(err)
}

// NoteUpdate updates a note
func PostUpdate(content string, userID string, noteID string) error {
	var err error

	//now := time.Now()
	//
	//switch database.ReadConfig().Type {
	//case database.TypeMySQL:
	//	_, err = database.SQL.Exec("UPDATE note SET content=? WHERE id = ? AND user_id = ? LIMIT 1", content, noteID, userID)
	//case database.TypeMongoDB:
	//	if database.CheckConnection() {
	//		// Create a copy of mongo
	//		session := database.Mongo.Copy()
	//		defer session.Close()
	//		c := session.DB(database.ReadConfig().MongoDB.Database).C("note")
	//		var note Note
	//		note, err = NoteByID(userID, noteID)
	//		if err == nil {
	//			// Confirm the owner is attempting to modify the note
	//			if note.UserID.Hex() == userID {
	//				note.UpdatedAt = now
	//				note.Content = content
	//				err = c.UpdateId(bson.ObjectIdHex(noteID), &note)
	//			} else {
	//				err = ErrUnauthorized
	//			}
	//		}
	//	} else {
	//		err = ErrUnavailable
	//	}
	//case database.TypeBolt:
	//	var note Note
	//	note, err = NoteByID(userID, noteID)
	//	if err == nil {
	//		// Confirm the owner is attempting to modify the note
	//		if note.UserID.Hex() == userID {
	//			note.UpdatedAt = now
	//			note.Content = content
	//			err = database.Update("note", userID+note.ObjectID.Hex(), &note)
	//		} else {
	//			err = ErrUnauthorized
	//		}
	//	}
	//default:
	//	err = ErrCode
	//}

	return standardizeError(err)
}

// NoteDelete deletes a note
func PostDelete(userID string, noteID string) error {
	var err error

	//switch database.ReadConfig().Type {
	//case database.TypeMySQL:
	//	_, err = database.SQL.Exec("DELETE FROM note WHERE id = ? AND user_id = ?", noteID, userID)
	//case database.TypeMongoDB:
	//	if database.CheckConnection() {
	//		// Create a copy of mongo
	//		session := database.Mongo.Copy()
	//		defer session.Close()
	//		c := session.DB(database.ReadConfig().MongoDB.Database).C("note")
	//
	//		var note Note
	//		note, err = NoteByID(userID, noteID)
	//		if err == nil {
	//			// Confirm the owner is attempting to modify the note
	//			if note.UserID.Hex() == userID {
	//				err = c.RemoveId(bson.ObjectIdHex(noteID))
	//			} else {
	//				err = ErrUnauthorized
	//			}
	//		}
	//	} else {
	//		err = ErrUnavailable
	//	}
	//case database.TypeBolt:
	//	var note Note
	//	note, err = NoteByID(userID, noteID)
	//	if err == nil {
	//		// Confirm the owner is attempting to modify the note
	//		if note.UserID.Hex() == userID {
	//			err = database.Delete("note", userID+note.ObjectID.Hex())
	//		} else {
	//			err = ErrUnauthorized
	//		}
	//	}
	//default:
	//	err = ErrCode
	//}

	return standardizeError(err)
}
