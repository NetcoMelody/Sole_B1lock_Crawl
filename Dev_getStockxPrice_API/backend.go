package main

import (
	"bufio"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"log"
	"os"
	"os/exec"

	"github.com/gin-gonic/gin"
)

func generateRandomHash() (string, error) {
	randomBytes := make([]byte, 8)
	_, err := rand.Read(randomBytes)
	if err != nil {
		return "", err
	}
	hash := sha256.Sum256(randomBytes)

	fullHash := hex.EncodeToString(hash[:])
	return fullHash[:4], nil
}

type Payload struct {
	UserName  string `json:"UserName"`
	ProductId string `json:"ProductId"`
}

func postHandle(c *gin.Context) {
	var reqBody Payload
	if c.GetHeader("Authorization") != "Bearer intraAllowPass" {
		c.JSON(401, gin.H{
			"message": fmt.Sprintf("脚本出错: %s", "认证未通过"),
		})
	} else {
		err := c.ShouldBindBodyWithJSON(&reqBody)
		if err != nil {
			c.JSON(400, gin.H{
				"message": fmt.Sprintf("脚本出错: %s", "请求体构建失败"),
			})
		}
		hashHex, err := generateRandomHash()
		if err != nil {
			c.JSON(501, gin.H{
				"message": fmt.Sprintf("脚本出错: %s", "hash生成失败"),
			})
		}

		cmd := exec.Command("D:/Multi-Tech-Project/.venv/Scripts/python.exe", "D:/Multi-Tech-Project/StockX_crawl/productPrice_main.py", reqBody.ProductId, reqBody.UserName, hashHex)

		stdout, err := cmd.StdoutPipe()
		if err != nil {
			log.Fatalf("无法创建 stdout 管道: %v", err)
		}
		stderr, err := cmd.StderrPipe()
		if err != nil {
			log.Fatalf("无法创建 stderr 管道: %v", err)
		}

		if err := cmd.Start(); err != nil {
			log.Fatalf("启动 Python 脚本失败: %v", err)
		}
		go func() {
			scanner := bufio.NewScanner(stdout)
			for scanner.Scan() {
				line := scanner.Text()
				log.Printf("[Python stdout] %s", line)
			}
		}()

		go func() {
			scanner := bufio.NewScanner(stderr)
			for scanner.Scan() {
				line := scanner.Text()
				log.Printf("[Python stderr] %s", line)
			}
		}()


		err = cmd.Wait()
		if err != nil {
			log.Printf("Python 脚本执行失败: %v", err)
			c.JSON(400, gin.H{"message": "脚本出错: py进程执行失败"})
			return
		}

		log.Println("Python 脚本执行完成")

		filename := "D:/Multi-Tech-Project/Dev_getStockxPrice_API/Response_json/" + reqBody.UserName + "-" + hashHex + "-data.json"
		fmt.Println(filename)
		data, err := os.ReadFile(filename)

		if err != nil {
			c.JSON(400, gin.H{
				"message": fmt.Sprintf("脚本出错: %s", "json数据读取失败"),
			})
		} else {
			c.Data(200, "application/json; charset=utf-8", data)
		}
	}
}

func main() {
	r := gin.Default()

	r.POST("/api/get_stockX_price/", postHandle)
	err := r.Run(":45678")
	if err != nil {
		log.Fatalln("HTTP服务启动阶段出错")
	}
}
