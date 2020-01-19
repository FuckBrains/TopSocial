package database

import (
	//"encoding/json"
	//"fmt"
	"log"
	//"time"
	"github.com/diegogub/aranGO"
	//"github.com/go-redis/redis"
	//"github.com/boltdb/bolt"
	//_ "github.com/go-sql-driver/mysql" // MySQL driver
	//"github.com/jmoiron/sqlx"
	//"gopkg.in/mgo.v2"
	"github.com/go-redis/redis"
	"time"
)

var (
	RedisDB *redis.Client

	ArangoDB *aranGO.Session

	// BoltDB wrapper
	//BoltDB *bolt.DB
	// Mongo wrapper
	//Mongo *mgo.Session
	// SQL wrapper
	//SQL *sqlx.DB
	// Database info
	databases Info
)

// Type is the type of database from a Type* constant
type Type string

const (
	TypeArangoDB Type = "ArangoDB"

	TypeRedis Type = "Redis"

	//// TypeBolt is BoltDB
	//TypeBolt Type = "Bolt"
	//// TypeMongoDB is MongoDB
	//TypeMongoDB Type = "MongoDB"
	//// TypeMySQL is MySQL
	//TypeMySQL Type = "MySQL"
)

// Info contains the database configurations
type Info struct {
	// Database type
	Type Type

	ArangoDB ArangoInfo


	RedisDB redis.Client

	//// MySQL info if used
	//MySQL MySQLInfo
	//// Bolt info if used
	//Bolt BoltInfo
	//// MongoDB info if used
	//MongoDB MongoDBInfo
}

type ArangoInfo struct {
	Host     	string	`json:"host"`
	Username     	string	`json:"user"`
	Password 	string	`json:"password"`
	Log      	bool	`json:"log"`
}

// MySQLInfo is the details for the database connection
//type MySQLInfo struct {
//	Username  string
//	Password  string
//	Name      string
//	Hostname  string
//	Port      int
//	Parameter string
//}

//// BoltInfo is the details for the database connection
//type BoltInfo struct {
//	Path string
//}
//
//// MongoDBInfo is the details for the database connection
//type MongoDBInfo struct {
//	URL      string
//	Database string
//}
const (
	DB_TopSocial string= "tscl"
)

//// DSN returns the Data Source Name
//func DSN(ci MySQLInfo) string {
//	// Example: root:@tcp(localhost:3306)/test
//	return ci.Username +
//		":" +
//		ci.Password +
//		"@tcp(" +
//		ci.Hostname +
//		":" +
//		fmt.Sprintf("%d", ci.Port) +
//		")/" +
//		ci.Name + ci.Parameter
//}

// Connect to the database
func Connect(d Info) {
	var err error

	// Store the config
	databases = d

	switch d.Type {
	case TypeArangoDB:
		for i := 1; i < 6;i++{
			if ArangoDB, err = aranGO.Connect(databases.ArangoDB.Host, databases.ArangoDB.Username, databases.ArangoDB.Password, false); err != nil {
				log.Println("ArangoDB  Driver Error", err)
				time.Sleep(10000* time.Millisecond)
			}
			if(err == nil){
				break
			}
		}


	case TypeRedis:
	RedisDB = redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password set
		DB:       0,  // use default DB
	})

	//case TypeMySQL:
	//	// Connect to MySQL
	//	if SQL, err = sqlx.Connect("mysql", DSN(d.MySQL)); err != nil {
	//		log.Println("SQL Driver Error", err)
	//	}
	//
	//	// Check if is alive
	//	if err = SQL.Ping(); err != nil {
	//		log.Println("Database Error", err)
	//	}
	//case TypeBolt:
	//	// Connect to Bolt
	//	if BoltDB, err = bolt.Open(d.Bolt.Path, 0600, nil); err != nil {
	//		log.Println("Bolt Driver Error", err)
	//	}
	//case TypeMongoDB:
	//	// Connect to MongoDB
	//	if Mongo, err = mgo.DialWithTimeout(d.MongoDB.URL, 5*time.Second); err != nil {
	//		log.Println("MongoDB Driver Error", err)
	//		return
	//	}
	//
	//	// Prevents these errors: read tcp 127.0.0.1:27017: i/o timeout
	//	Mongo.SetSocketTimeout(1 * time.Second)
	//
	//	// Check if is alive
	//	if err = Mongo.Ping(); err != nil {
	//		log.Println("Database Error", err)
	//	}
	default:
		log.Println("No registered database in config")
	}

	CreateCollections(d)
}


func CreateCollections(d Info)  {
	//var err error

	// Store the config
	databases = d

	switch d.Type {
	case TypeArangoDB:
		dbs,_ := ArangoDB.AvailableDBs()
		dbIsPresent := false
		for _, b := range dbs {
			if b == DB_TopSocial {
			    dbIsPresent = true
			}
		}

		if !dbIsPresent {
			users := []aranGO.User{
				{
					Username:databases.ArangoDB.Username,
					Password:databases.ArangoDB.Password,
					Active:true,
				},
			}
			ArangoDB.CreateDB(DB_TopSocial,users)
		}
		// create Collections test if exist
		collections := []string{
			"Posts",
			"Hashtags",
			"RecentPopularImagesCache",
			"RecentPopularVideosCache",
			"RecentPopularHashtagsCache",
		}
		for _, col := range collections  {

			if !ArangoDB.DB(DB_TopSocial).ColExist(col){
				// CollectionOptions has much more options, here we just define name , sync
				col := aranGO.NewCollectionOptions(col,true)
				ArangoDB.DB(DB_TopSocial).CreateCollection(col)
			}
		}

	default:
		log.Println("No registered database in config")
	}


}

func CreateIndexes(d Info)  {
	var err error

	// Store the config
	databases = d

	switch d.Type {
	case TypeArangoDB:

		if err = ArangoDB.DB(DB_TopSocial).Col("Posts").CreateFullText(2,"body"); err != nil {
			log.Println("ArangoDB Driver Error", err)
		}
	default:
		log.Println("No registered database in config")
	}


}

// Update makes a modification to Bolt
func UpdateDocument(dbName string, collectionName string, dataStruct interface{}) error {
	err := aranGO.Database{Name: dbName}.Col(collectionName).Save(dataStruct)
	return err

	//
	//
	//err := BoltDB.Update(func(tx *bolt.Tx) error {
	//	// Create the bucket
	//	bucket, e := tx.CreateBucketIfNotExists([]byte(bucketName))
	//	if e != nil {
	//		return e
	//	}
	//
	//	// Encode the record
	//	encodedRecord, e := json.Marshal(dataStruct)
	//	if e != nil {
	//		return e
	//	}
	//
	//	// Store the record
	//	if e = bucket.Put([]byte(key), encodedRecord); e != nil {
	//		return e
	//	}
	//	return nil
	//})
	//return err
}

// View retrieves a record in Bolt
func View(dbName string, collectionName string, key string, dataStruct interface{}) error {
	err := aranGO.Database{Name: dbName}.Col(collectionName).Get(key, dataStruct)
	return err

	//err := BoltDB.View(func(tx *bolt.Tx) error {
	//	// Get the bucket
	//	b := tx.Bucket([]byte(bucketName))
	//	if b == nil {
	//		return bolt.ErrBucketNotFound
	//	}
	//
	//	// Retrieve the record
	//	v := b.Get([]byte(key))
	//	if len(v) < 1 {
	//		return bolt.ErrInvalid
	//	}
	//
	//	// Decode the record
	//	e := json.Unmarshal(v, &dataStruct)
	//	if e != nil {
	//		return e
	//	}
	//
	//	return nil
	//})
	//
	//return err
}

// Delete removes a record from Bolt
func DeleteKey(dbName string, collectionName string, key string) error {
	err := aranGO.Database{Name: dbName}.Col(collectionName).Delete(key)
	return err

	//err := BoltDB.Update(func(tx *bolt.Tx) error {
	//	// Get the bucket
	//	b := tx.Bucket([]byte(bucketName))
	//	if b == nil {
	//		return bolt.ErrBucketNotFound
	//	}
	//
	//	return b.Delete([]byte(key))
	//})
	//return err
}

func ExecuteQuery(databaseName string, query string, vars map[string]interface{}) (*aranGO.Cursor, error) {
	q := aranGO.NewQuery(query)
	q.BindVars = vars
	c, err := ArangoDB.DB(databaseName).Execute(q)
	if err != nil {
		return c, err
	}
	return c, nil
}

// CheckConnection returns true if MongoDB is available
func CheckConnection() bool {
	if ArangoDB == nil {
		Connect(databases)
	}

	if ArangoDB != nil {
		return true
	}
	return false
	//
	//if Mongo == nil {
	//	Connect(databases)
	//}
	//
	//if Mongo != nil {
	//	return true
	//}
	//
	//return false
}

// ReadConfig returns the database information
func ReadConfig() Info {
	return databases
}
