package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strconv"
	"strings"

	"github.com/go-gota/gota/dataframe"
	"github.com/go-gota/gota/series"
)

type BrowseGetitemHeader struct {
	Authorization           string
	X_EBAY_C_MARKETPLACE_ID string
	X_EBAY_C_ENDUSERCTX     string
}

var browserGetItemApi = "https://api.ebay.com/buy/browse/v1/item/{v1|listing_id|variation_id}"

var token = "v^1.1#i^1#I^3#p^3#r^0#f^0#t^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"

var ClientBrowseGetItemHeaders = BrowseGetitemHeader{
	Authorization:           fmt.Sprintf("Bearer %v", token),
	X_EBAY_C_ENDUSERCTX:     "EBAY_US",
	X_EBAY_C_MARKETPLACE_ID: "affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>",
}

func browserGetItems(itemId string) (float64, string, string, string, string, string) {
	fmt.Println(itemId)
	getItemId := strings.Split(itemId, "|")[1]
	browserGetItemApi_usable := strings.ReplaceAll(browserGetItemApi, "{v1|listing_id|variation_id}", itemId)
	req, err := http.NewRequest("GET", browserGetItemApi_usable, nil)
	if err != nil {
		log.Fatalln("阶段二创建请求出错")
	}
	Authorization := ClientBrowseGetItemHeaders.Authorization
	X_EBAY_C_MARKETPLACE_ID := ClientBrowseGetItemHeaders.X_EBAY_C_MARKETPLACE_ID
	X_EBAY_C_ENDUSERCTX := ClientBrowseGetItemHeaders.X_EBAY_C_ENDUSERCTX
	req.Header.Set("Authorization", Authorization)
	req.Header.Set("X_EBAY_C_MARKETPLACE_ID", X_EBAY_C_MARKETPLACE_ID)
	req.Header.Set("X_EBAY_C_ENDUSERCTX", X_EBAY_C_ENDUSERCTX)
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		log.Fatalln("阶段二发送请求/接收响应阶段出错")
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln("阶段二读取body阶段出错")
	}
	var dataMap map[string]interface{}
	err = json.Unmarshal(body, &dataMap)
	if err != nil {
		log.Fatalln("阶段二json反序列化出错")
	}
	usPriceMap := dataMap["price"].(map[string]interface{})
	usPriceValue := usPriceMap["value"].(string)
	usPriceValueFloat, err := strconv.ParseFloat(usPriceValue, 2)
	if err != nil {
		log.Fatalln("阶段二字符转浮点转换失败")
	}
	var usPriceValueNow float64
	marketingPriceMap, ok := dataMap["marketingPrice"]
	if ok {
		marketingPriceMap := marketingPriceMap.(map[string]interface{})
		discountAmoutMap := marketingPriceMap["discountAmount"].(map[string]interface{})
		discountAmoutValue := discountAmoutMap["value"].(string)
		discountAmoutValueFloat, err := strconv.ParseFloat(discountAmoutValue, 2)
		if err != nil {
			log.Fatalln("转换失败")
		}
		usPriceValueNow = usPriceValueFloat - discountAmoutValueFloat
	} else {
		usPriceValueNow = usPriceValueFloat
	}

	localizedAspects := dataMap["localizedAspects"].([]interface{})
	var cardName string
	var cardNumber string
	var cardLanguage string

	for _, item := range localizedAspects {
		mapInfo := item.(map[string]interface{})
		name := mapInfo["name"].(string)
		if name == "Card Name" {
			cardName = mapInfo["value"].(string)
		}
		if name == "Card Number" {
			cardNumber = mapInfo["value"].(string)
			log.Println("进来了")
		}
		if name == "Language" {
			cardLanguage = mapInfo["value"].(string)
		}
	}
	title := dataMap["title"].(string)
	log.Printf("CardTitle:%s,CardName:%s,CardNumber:%s,CardLanguage:%s,CardPrice:%v", title, cardName, cardNumber, cardLanguage, usPriceValueNow)
	return usPriceValueNow, cardName, cardNumber, getItemId, cardLanguage, title

}

func main() {
	arg := os.Args[1]

	itemCodeSlice := strings.Split(arg, ",")
	cardNameSlice := make([]string, 0)
	cardNumberSlice := make([]string, 0)
	cardPriceSlice := make([]float64, 0)
	cardItemIdSlice := make([]string, 0)
	cardLanguageSlice := make([]string, 0)
	cardTitleSlice := make([]string, 0)
	log.Println(itemCodeSlice)
	for _, itemcode := range itemCodeSlice {
		var cardNumber string
		var cardName string
		var getItemId string
		var cardLanguage string
		var title string
		usPriceValueNow, cardName, cardNumber, getItemId, cardLanguage, title := browserGetItems(itemcode)
		if cardNumber == "" {
			continue
		}
		cardNumber = "'" + cardNumber
		log.Println("cardNumber:", cardNumber)
		cardNameSlice = append(cardNameSlice, cardName)
		cardNumberSlice = append(cardNumberSlice, cardNumber)
		cardPriceSlice = append(cardPriceSlice, usPriceValueNow)
		cardItemIdSlice = append(cardItemIdSlice, getItemId)
		cardLanguageSlice = append(cardLanguageSlice, cardLanguage)
		cardTitleSlice = append(cardTitleSlice, title)
	}
	cardTitleSeries := series.New(cardTitleSlice, series.String, "CardTitle")
	cardItemIdSeries := series.New(cardItemIdSlice, series.String, "ItemId")
	cardNameSeries := series.New(cardNameSlice, series.String, "CardName")
	cardNumberSeries := series.New(cardNumberSlice, series.String, "CardNumber")
	cardPriceSeries := series.New(cardPriceSlice, series.Float, "CardPrice-US")
	cardLanguageSeries := series.New(cardLanguageSlice, series.String, "CardLanguage")

	df := dataframe.New(cardTitleSeries, cardItemIdSeries, cardNameSeries, cardNumberSeries, cardPriceSeries, cardLanguageSeries)
	log.Println(df)
	file, err := os.OpenFile("Pokemon.csv", os.O_CREATE, 0755)
	if err != nil {
		log.Fatalln("创建文件时出错")
	}
	defer file.Close()
	err = df.WriteCSV(file)
	log.Println(df)
	if err != nil {
		log.Fatalln("写入CSV时出错:", err)
	}
	log.Println("ebay_csv初始文件生成完毕")

	//cmd := exec.Command("D:/KarosProject/.venv/Scripts/python.exe", "D:/KarosProject/ebay_pokemon/card_match_with_api.py")
	//// 创建管道
	//stdout, err := cmd.StdoutPipe()
	//if err != nil {
	//	log.Fatalf("无法创建 stdout 管道: %v", err)
	//}
	//
	//stderr, err := cmd.StderrPipe()
	//if err != nil {
	//	log.Fatalf("无法创建 stderr 管道: %v", err)
	//}
	//
	//if err := cmd.Start(); err != nil {
	//	log.Fatalf("启动 Python 脚本失败: %v", err)
	//}
	//
	//go func() {
	//	scanner := bufio.NewScanner(stdout)
	//	for scanner.Scan() {
	//		line := scanner.Text()
	//		log.Printf("[Python stdout] %s", line)
	//	}
	//}()
	//go func() {
	//	scanner := bufio.NewScanner(stderr)
	//	for scanner.Scan() {
	//		line := scanner.Text()
	//		log.Printf("[Python stderr] %s", line)
	//	}
	//}()
	//err = cmd.Wait()
	//if err != nil {
	//	log.Fatalln("py脚本运行出错")
	//}
	//log.Println("Python 脚本执行完成")

}
