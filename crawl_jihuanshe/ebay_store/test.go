package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
)

type Headers struct {
	Authorization           string
	X_EBAY_C_MARKETPLACE_ID string
	X_EBAY_C_ENDUSERCTX     string
}

var searchApi = "https://api.ebay.com/buy/browse/v1/item_summary/search?q=Pokemon&limit=200&filter=sellers:{pokecolor_official}"

var token = "v^1.1#i^1#p^3#f^0#I^3#r^0#t^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"
var ClientHeaders = Headers{Authorization: fmt.Sprintf("Bearer %v", token),
	X_EBAY_C_ENDUSERCTX:     "EBAY_US",
	X_EBAY_C_MARKETPLACE_ID: "affiliateCampaignId=<ePNCampaignId>,affiliateReferenceId=<referenceId>",
}

func main() {
	req, err := http.NewRequest("GET", searchApi, nil)
	if err != nil {
		log.Fatalln("创建请求出错")
	}
	Authorization := ClientHeaders.Authorization
	X_EBAY_C_MARKETPLACE_ID := ClientHeaders.X_EBAY_C_MARKETPLACE_ID
	X_EBAY_C_ENDUSERCTX := ClientHeaders.X_EBAY_C_ENDUSERCTX
	req.Header.Set("Authorization", Authorization)
	req.Header.Set("X_EBAY_C_MARKETPLACE_ID", X_EBAY_C_MARKETPLACE_ID)
	req.Header.Set("X_EBAY_C_ENDUSERCTX", X_EBAY_C_ENDUSERCTX)

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		log.Fatalln("发送请求/接收响应阶段出错")
	}
	defer resp.Body.Close()
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln("在读取resp_body阶段出错")
	}
	var dataMap map[string]interface{}
	err = json.Unmarshal(body, &dataMap)
	if err != nil {
		log.Fatalln("json反序列化阶段出错")
	}
	itemSummariesField := dataMap["itemSummaries"].([]interface{})
	for _, item := range itemSummariesField {
		itemMap := item.(map[string]interface{})
		itemIdField := itemMap["itemId"]
		titleField := itemMap["title"]
		fmt.Printf("itemId: %v,title: %v", itemIdField, titleField)
	}

}
