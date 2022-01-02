package main

import (
	"bufio"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
)

// Binding from JSON
type Login struct {
	Id       string `json:"id"`
	Password string `json:"password"`
}

var db = map[string]string{}

// String comparing if the string is match
func login_verifier(id string, passwd string) bool {
	// the db must be configured
	if val, ok := db[id]; ok {
		return passwd == val
	}
	return false
}

// Init the (id, pw) fot db global variable
func init() {
	// Read id and hashed paw from data
	file, err := os.Open("./account.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		var id string
		var pw string
		fmt.Sscanf(line, "%s %s", &id, &pw)
		db[id] = pw
	}
}

func main() {
	fmt.Println("HIJACK: ", os.Getenv("HIJACK"))
	is_hijacked := os.Getenv("HIJACK") == "true"
	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		c.JSON(200, gin.H{"msg": "hello"})
	})

	r.POST("/login", func(c *gin.Context) {
		var json Login
		if err := c.ShouldBindJSON(&json); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		if is_hijacked {
			c.JSON(200, gin.H{"Your password": json.Password})
		}

		if ok := login_verifier(json.Id, json.Password); ok {
			c.JSON(200, gin.H{"status": "Success"})
		} else {
			c.JSON(401, gin.H{"status": "Failed"})
		}
	})

	r.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{"ping": "pong"})
	})

	r.Run()
}
