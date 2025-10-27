from curl_cffi import requests
import json
import time
import random

# ========== HEADERS ==========
HEADERS = {
    "apollographql-client-name": "android",
    "apollographql-client-version": "4.51.0",
    "x-experiment-ids": "",
    "x-abtest-ids": "ab-hk-dynamic-postal-code-test-android.true,ab_0zi3v_all.neither,ab_12dul_all.neither,ab_12xvy_all.neither,ab_1e6kr_all.neither,ab_1sru6_android.neither,ab_1x09h_all.neither,ab_2dxd6_all.neither,ab_2l12n_all.neither,ab_3gx6w_android.true,ab_3ny27_all.neither,ab_3xk99_all.neither,ab_4229r_all.neither,ab_4bj0m_all.neither,ab_4nneg_all.neither,ab_5ztfi_android.true,ab_69ods_android.false,ab_6q41q_all.neither,ab_6q947_all.neither,ab_8imzw_all.neither,ab_8r25c_all.neither,ab_8u3xq_all.neither,ab_90r9o_all.neither,ab_95odv_all.neither,ab_9a2wj_all.neither,ab_9fn6j_all.neither,ab_9qwls_all.neither,ab_a1gsn_all.neither,ab_a1uoe_all.neither,ab_a4mxa_all.neither,ab_a6imz_android.variant2,ab_aa_continuous_all.android_b,ab_agzb4_all.neither,ab_amv0e_all.neither,ab_android_sell_faster_global_expansion.true,ab_b0lfl_all.neither,ab_b0tzh_all.neither,ab_bgmm0_all.neither,ab_browse_search_graphql_android.true,ab_bu42t_all.neither,ab_c9kg3_all.neither,ab_carpb_all.neither,ab_cb7zc_all.neither,ab_checkout_confirm_purchase_text_android.true,ab_checkout_review_order_verbiage_android.true,ab_d8yo9_all.neither,ab_discovery_color_filter_all.false,ab_drc_chk_sell_intra_zone_all_in_support_ios.neither,ab_drc_chk_sell_intra_zone_all_in_support_web.neither,ab_ef9vp_all.neither,ab_efozi_all.neither,ab_enable_paypal_bnpl_android.true,ab_eu_vat_android.true,ab_f0pga_all.neither,ab_f7l0q_all.neither,ab_fdg98_all.neither,ab_fu7pq_android.true,ab_g3zha_all.neither,ab_gbjhy_all.neither,ab_gdgws_all.neither,ab_ggc8y_android.true,ab_grabp_all.neither,ab_grbq0_all.neither,ab_gxdz2_android.neither,ab_h6ame_all.neither,ab_hist4_all.neither,ab_hs551_all.neither,ab_htirt_all.neither,ab_hzpar_all.neither,ab_i2y4k_android.true,ab_i7vz3_all.neither,ab_iq9hc_all.neither,ab_j67v4_all.neither,ab_jhuaj_all.neither,ab_jj4k0_all.neither,ab_jr638_all.neither,ab_k7h7d_all.neither,ab_knu9v_android.neither,ab_l3qx6_all.neither,ab_l88fy_all.neither,ab_lblnn_android.neither,ab_m1lzy_all.neither,ab_m6ocb_all.neither,ab_mhzc2_all.neither,ab_mi2jq_all.neither,ab_mk5q4_all.neither,ab_mngh0_all.neither,ab_moc6y_all.neither,ab_ncuqa_all.neither,ab_new_restock_pdp_android.true,ab_njs9e_all.neither,ab_oh5mh_all.neither,ab_oxct5_all.neither,ab_pqaqw_all.neither,ab_prcf4_all.neither,ab_price_changed_modal_android.variant,ab_qdhpu_all.neither,ab_qm42n_all.neither,ab_qzzhs_android.true,ab_r3tze_all.neither,ab_r8s3j_all.neither,ab_revert_all_ask_bids_sales_disclaimer_label_treatment_ios.neither,ab_ri9lk_all.neither,ab_rt6ez_all.neither,ab_rveai_android.true,ab_s6npw_all.neither,ab_saimx_all.neither,ab_sdbvc_all.neither,ab_seller_profile_redesign_android.true,ab_sw6qu_all.neither,ab_t963l_all.neither,ab_thz6x_all.neither,ab_ti621_all.neither,ab_tvtx0_all.neither,ab_u7fwy_all.neither,ab_uf50j_all.neither,ab_unkq0_android.true,ab_ut4nb_all.neither,ab_vaxcq_all.neither,ab_ve7g0_android.false,ab_vh3dz_all.neither,ab_w22q2_all.neither,ab_w5s5e_all.neither,ab_w8yox_all.neither,ab_wvioi_android.true,ab_wxcu9_all.neither,ab_x9ydr_android.true,ab_ybl3h_all.neither,ab_ycyfe_android.true,ab_yuqey_all.neither,ab_z5d2b_all.neither,ab_zbgo7_all.neither,ab_zcjc2_all.neither,ab_zfpmw_all.neither,ab_zjz5s_all.neither,ab_zk1ar_all.neither,ab_zksq0_all.neither,ab_zwxog_all.neither",
    "accept": "multipart/mixed;deferSpec=20220824, application/json",
    "x-api-key": "zWW9iZmfu02CDfd9bCWnZ29mKLgHC9AJ5kjUHvVq",
    "app-platform": "android",
    "app-version": "4.51.0",
    "accept-language": "zh-CN",
    "x-session-id": "a4f65211-9f65-4d5f-8fec-97632715c154",
    "x-stockx-session-id": "20fecd35-f680-4435-b8e0-9a0662059ffb",
    "x-drc-feature-localized-sizing": "true",
    "x-stockx-device-id": "bc95f2418c78c9a2",
    "user-agent": "Dalvik/2.1.0 (Linux; U; Android 12; ALN-AL00 Build/60095c0.0)",
    "x-device-id": "7a12-9699-a32e-6eb2",
    "x-px-vid": "980857b7-a7f5-11f0-b9b5-8acb3817969d",
    "x-px-os-version": "12",
    "x-px-uuid": "79e444b6-a8c2-11f0-baa4-2db168856a6e",
    "x-px-device-fp": "bc95f2418c78c9a2",
    "x-px-device-model": "ALN-AL00",
    "x-px-os": "Android",
    "x-px-hello": "BApWBwcHUQUeUgtQAR4CAlUDHlFSUgceAVdRAgULCwYFUgVW",
    "x-px-mobile-sdk-version": "3.2.1",
    "x-px-authorization": "3:de40b7ffd9083d6f01545ffa16585f0aaeefca83336acaf9485c614d1e054177:tuDnIhnbmCRSOXPEsK7DZ/MN1sK3++9Z08L3imUKaWaVt9TpWYhQl4+ncupd7bO1UE4zlnCVtLkicKA4HyrAyA==:1000:k2MycnkiR8T6+5GuW3eBJSW5j2f9AUcAqt7H2B8hmnbNBcUzjuNCYmccMLnjM3M5mliIcZykDghImLxTIy1hlzIxOhY6H9NiDS5kvvdd3oUuqjZnESL9lNOduSd2d9tOmNOv7MOBZ7csMLg6AR2UpfEeItQwNaF3Lfh06zp9skWIbV7stB/nLFoe/focnmTGfquUUnl9UJDlfeRBjmpC8AghtGyJmLfUASuUZDDbwSY=",
    "content-type": "application/json",
    "accept-encoding": "gzip"
}

# ========== JSON PAYLOAD ==========
JSON_DATA = {
    "operationName": "UnifiedProductQuery",
    "variables": {
        "id": "aafa5e04-6509-4ff2-90aa-8742ec9fd6d5",
        "currency": "USD",
        "marketName": "CN",
        "countryCode": "CN",
        "includeFamilies": True
    },
    "query": """
    query UnifiedProductQuery(
        $id: String!,
        $currency: CurrencyCode,
        $marketName: String,
        $countryCode: String!,
        $includeFamilies: Boolean!
    ) {
        product(id: $id) {
            # 基础信息（来自 Product）
            id uuid brand styleId model title primaryCategory productCategory
            condition listingType description media { imageUrl smallImageUrl }
            traits { name value } taxInformation { code }
            
            # 尺码相关（来自 SizeSelector）
            sizeAllDescriptor sizeDescriptor
            defaultSizeConversion { name type }
            availableSizeConversions { name type }
            
            # 变体 + 市场价格（合并）
            variants {
                id hidden sortOrder
                traits { size sizeDescriptor }
                group { id shortCode }
                sizeChart { displayOptions { size type } }
                market(currencyCode: $currency) {
                    state(country: $countryCode, market: $marketName) {
                        lowestAsk { amount }
                        highestBid { amount }
                        askServiceLevels {
                            expressExpedited { count lowest { amount } }
                            expressStandard { count lowest { amount } }
                            standard { count lowest { amount } }
                        }
                    }
                }
            }

            # 全局市场数据
            market(currencyCode: $currency) {
                currencyCode
                state(country: $countryCode) {
                    lowestAsk { amount }
                    highestBid { amount }
                }
            }

            # 其他 Product 字段
            returnEligible(market: $marketName)
            resellNoFee { eligibilityDays enabled }
            favorite
            lockBuying lockSelling

            # families（按需包含）
            families @include(if: $includeFamilies) {
                design {
                    id type
                    members {
                        edges {
                            node {
                                id title
                                media { smallImageUrl }
                            }
                        }
                    }
                }
            }
        }
    }
    """
}
# ========== MAIN ==========
if __name__ == "__main__":
    print("🚀 Sending Suggestions request to StockX (query: DR5415-100)...")
    try:
        resp = requests.post(
            "https://gateway.stockx.com/api/graphql",
            headers=HEADERS,
            json=JSON_DATA,
            # impersonate="chrome120",  # 模拟现代浏览器指纹（绕过部分 bot 检测）
            timeout=15
        )
        print(f"✅ Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("❌ Response:", resp.text[:500])
    except Exception as e:
        print("💥 Error:", e)

# D:\Project\pyproject\.venv\Scripts\python.exe D:\Project\pyproject\StockX_crawl\test.py
# 🚀 Sending Suggestions request to StockX (query: DR5415-100)...
# ✅ Status: 200
# {
#   "data": {
#     "product": {
#       "id": "aafa5e04-6509-4ff2-90aa-8742ec9fd6d5",
#       "uuid": "aafa5e04-6509-4ff2-90aa-8742ec9fd6d5",
#       "brand": "Jordan",
#       "styleId": "DQ9293-018",
#       "model": "Jordan 23/7",
#       "title": "Jordan 23/7 Football Grey White Orange Blaze Pine Green (PS)",
#       "primaryCategory": "Air Jordan",
#       "productCategory": "sneakers",
#       "condition": "全新",
#       "listingType": "STANDARD",
#       "description": "",
#       "media": {
#         "imageUrl": "https://images.stockx.com/images/Air-Jordan-23-7-Football-Grey-White-Orange-Blaze-Pine-Green-PS.jpg?fit=fill&bg=FFFFFF&w=700&h=500&fm=webp&auto=compress&q=90&dpr=2&trim=color&updated_at=1729142748",
#         "smallImageUrl": "https://images.stockx.com/images/Air-Jordan-23-7-Football-Grey-White-Orange-Blaze-Pine-Green-PS.jpg?fit=fill&bg=FFFFFF&w=300&h=214&fm=webp&auto=compress&q=90&dpr=2&trim=color&updated_at=1729142748"
#       },
#       "traits": [
#         {
#           "name": "Style",
#           "value": "DQ9293-018"
#         },
#         {
#           "name": "Colorway",
#           "value": "Football Grey/White/Orange Blaze/Pine Green"
#         },
#         {
#           "name": "Retail Price",
#           "value": "65"
#         },
#         {
#           "name": "Release Date",
#           "value": "2024-05-30"
#         },
#         {
#           "name": "Featured",
#           "value": "false"
#         },
#         {
#           "name": "Requester",
#           "value": "Andrew H"
#         },
#         {
#           "name": "Uploaded By",
#           "value": "MB"
#         }
#       ],
#       "taxInformation": {
#         "code": "PC040500"
#       },
#       "sizeAllDescriptor": "All",
#       "sizeDescriptor": "Size",
#       "defaultSizeConversion": {
#         "name": "US",
#         "type": "us"
#       },
#       "availableSizeConversions": [
#         {
#           "name": "US",
#           "type": "us"
#         },
#         {
#           "name": "UK",
#           "type": "uk"
#         },
#         {
#           "name": "CM",
#           "type": "cm"
#         },
#         {
#           "name": "KR",
#           "type": "kr"
#         },
#         {
#           "name": "EU",
#           "type": "eu"
#         }
#       ],
#       "variants": [
#         {
#           "id": "b32f53db-f477-4a73-b672-40a392fe8d4b",
#           "hidden": false,
#           "sortOrder": 0,
#           "traits": {
#             "size": "10.5C",
#             "sizeDescriptor": null
#           },
#           "group": null,
#           "sizeChart": {
#             "displayOptions": [
#               {
#                 "size": "US 10.5C",
#                 "type": "us"
#               },
#               {
#                 "size": "UK 10",
#                 "type": "uk"
#               },
#               {
#                 "size": "CM 16.5",
#                 "type": "cm"
#               },
#               {
#                 "size": "KR 165",
#                 "type": "kr"
#               },
#               {
#                 "size": "EU 27.5",
#                 "type": "eu"
#               }
#             ]
#           },
#           "market": {
#             "state": {
#               "lowestAsk": null,
#               "highestBid": null,
#               "askServiceLevels": {
#                 "expressExpedited": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "expressStandard": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "standard": {
#                   "count": 0,
#                   "lowest": null
#                 }
#               }
#             }
#           }
#         },
#         {
#           "id": "5ffda273-efce-4526-a2b5-96e186cbdf27",
#           "hidden": false,
#           "sortOrder": 1,
#           "traits": {
#             "size": "11C",
#             "sizeDescriptor": null
#           },
#           "group": null,
#           "sizeChart": {
#             "displayOptions": [
#               {
#                 "size": "US 11C",
#                 "type": "us"
#               },
#               {
#                 "size": "UK 10.5",
#                 "type": "uk"
#               },
#               {
#                 "size": "CM 17",
#                 "type": "cm"
#               },
#               {
#                 "size": "KR 170",
#                 "type": "kr"
#               },
#               {
#                 "size": "EU 28",
#                 "type": "eu"
#               }
#             ]
#           },
#           "market": {
#             "state": {
#               "lowestAsk": {
#                 "amount": 50
#               },
#               "highestBid": null,
#               "askServiceLevels": {
#                 "expressExpedited": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "expressStandard": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "standard": {
#                   "count": 2,
#                   "lowest": {
#                     "amount": 50
#                   }
#                 }
#               }
#             }
#           }
#         },
#         {
#           "id": "032cc4ab-cd16-4e18-8e63-04b7aa0eb823",
#           "hidden": false,
#           "sortOrder": 2,
#           "traits": {
#             "size": "11.5C",
#             "sizeDescriptor": null
#           },
#           "group": null,
#           "sizeChart": {
#             "displayOptions": [
#               {
#                 "size": "US 11.5C",
#                 "type": "us"
#               },
#               {
#                 "size": "UK 11",
#                 "type": "uk"
#               },
#               {
#                 "size": "CM 17.5",
#                 "type": "cm"
#               },
#               {
#                 "size": "KR 175",
#                 "type": "kr"
#               },
#               {
#                 "size": "EU 28.5",
#                 "type": "eu"
#               }
#             ]
#           },
#           "market": {
#             "state": {
#               "lowestAsk": null,
#               "highestBid": null,
#               "askServiceLevels": {
#                 "expressExpedited": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "expressStandard": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "standard": {
#                   "count": 0,
#                   "lowest": null
#                 }
#               }
#             }
#           }
#         },
#         {
#           "id": "5552458d-e8ae-4d3d-a361-8cf8d7fad86b",
#           "hidden": false,
#           "sortOrder": 3,
#           "traits": {
#             "size": "12C",
#             "sizeDescriptor": null
#           },
#           "group": null,
#           "sizeChart": {
#             "displayOptions": [
#               {
#                 "size": "US 12C",
#                 "type": "us"
#               },
#               {
#                 "size": "UK 11.5",
#                 "type": "uk"
#               },
#               {
#                 "size": "CM 18",
#                 "type": "cm"
#               },
#               {
#                 "size": "KR 180",
#                 "type": "kr"
#               },
#               {
#                 "size": "EU 29.5",
#                 "type": "eu"
#               }
#             ]
#           },
#           "market": {
#             "state": {
#               "lowestAsk": {
#                 "amount": 86
#               },
#               "highestBid": null,
#               "askServiceLevels": {
#                 "expressExpedited": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "expressStandard": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "standard": {
#                   "count": 1,
#                   "lowest": {
#                     "amount": 86
#                   }
#                 }
#               }
#             }
#           }
#         },
#         {
#           "id": "c0be0518-51e2-4b88-a358-04ed17e7580f",
#           "hidden": false,
#           "sortOrder": 4,
#           "traits": {
#             "size": "12.5C",
#             "sizeDescriptor": null
#           },
#           "group": null,
#           "sizeChart": {
#             "displayOptions": [
#               {
#                 "size": "US 12.5C",
#                 "type": "us"
#               },
#               {
#                 "size": "UK 12",
#                 "type": "uk"
#               },
#               {
#                 "size": "CM 18.5",
#                 "type": "cm"
#               },
#               {
#                 "size": "KR 185",
#                 "type": "kr"
#               },
#               {
#                 "size": "EU 30",
#                 "type": "eu"
#               }
#             ]
#           },
#           "market": {
#             "state": {
#               "lowestAsk": null,
#               "highestBid": null,
#               "askServiceLevels": {
#                 "expressExpedited": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "expressStandard": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "standard": {
#                   "count": 0,
#                   "lowest": null
#                 }
#               }
#             }
#           }
#         },
#         {
#           "id": "b923a43e-aa80-48e2-a602-7a64151732bb",
#           "hidden": false,
#           "sortOrder": 5,
#           "traits": {
#             "size": "13C",
#             "sizeDescriptor": null
#           },
#           "group": null,
#           "sizeChart": {
#             "displayOptions": [
#               {
#                 "size": "US 13C",
#                 "type": "us"
#               },
#               {
#                 "size": "UK 12.5",
#                 "type": "uk"
#               },
#               {
#                 "size": "CM 19",
#                 "type": "cm"
#               },
#               {
#                 "size": "KR 190",
#                 "type": "kr"
#               },
#               {
#                 "size": "EU 31",
#                 "type": "eu"
#               }
#             ]
#           },
#           "market": {
#             "state": {
#               "lowestAsk": {
#                 "amount": 63
#               },
#               "highestBid": null,
#               "askServiceLevels": {
#                 "expressExpedited": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "expressStandard": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "standard": {
#                   "count": 1,
#                   "lowest": {
#                     "amount": 63
#                   }
#                 }
#               }
#             }
#           }
#         },
#         {
#           "id": "90f59f3b-6acf-43f3-a155-29b11c841a84",
#           "hidden": false,
#           "sortOrder": 6,
#           "traits": {
#             "size": "13.5C",
#             "sizeDescriptor": null
#           },
#           "group": null,
#           "sizeChart": {
#             "displayOptions": [
#               {
#                 "size": "US 13.5C",
#                 "type": "us"
#               },
#               {
#                 "size": "UK 13",
#                 "type": "uk"
#               },
#               {
#                 "size": "CM 19.5",
#                 "type": "cm"
#               },
#               {
#                 "size": "KR 195",
#                 "type": "kr"
#               },
#               {
#                 "size": "EU 31.5",
#                 "type": "eu"
#               }
#             ]
#           },
#           "market": {
#             "state": {
#               "lowestAsk": null,
#               "highestBid": null,
#               "askServiceLevels": {
#                 "expressExpedited": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "expressStandard": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "standard": {
#                   "count": 0,
#                   "lowest": null
#                 }
#               }
#             }
#           }
#         },
#         {
#           "id": "98d6bda2-90dc-4bb8-97b5-30b2385fecad",
#           "hidden": false,
#           "sortOrder": 7,
#           "traits": {
#             "size": "1Y",
#             "sizeDescriptor": null
#           },
#           "group": null,
#           "sizeChart": {
#             "displayOptions": [
#               {
#                 "size": "US 1Y",
#                 "type": "us"
#               },
#               {
#                 "size": "UK 13.5",
#                 "type": "uk"
#               },
#               {
#                 "size": "CM 20",
#                 "type": "cm"
#               },
#               {
#                 "size": "KR 200",
#                 "type": "kr"
#               },
#               {
#                 "size": "EU 32",
#                 "type": "eu"
#               }
#             ]
#           },
#           "market": {
#             "state": {
#               "lowestAsk": {
#                 "amount": 50
#               },
#               "highestBid": null,
#               "askServiceLevels": {
#                 "expressExpedited": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "expressStandard": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "standard": {
#                   "count": 1,
#                   "lowest": {
#                     "amount": 50
#                   }
#                 }
#               }
#             }
#           }
#         },
#         {
#           "id": "f966b83a-88f5-4ac4-903b-702e561e515a",
#           "hidden": false,
#           "sortOrder": 8,
#           "traits": {
#             "size": "1.5Y",
#             "sizeDescriptor": null
#           },
#           "group": null,
#           "sizeChart": {
#             "displayOptions": [
#               {
#                 "size": "US 1.5Y",
#                 "type": "us"
#               },
#               {
#                 "size": "UK 1",
#                 "type": "uk"
#               },
#               {
#                 "size": "CM 20.5",
#                 "type": "cm"
#               },
#               {
#                 "size": "KR 205",
#                 "type": "kr"
#               },
#               {
#                 "size": "EU 33",
#                 "type": "eu"
#               }
#             ]
#           },
#           "market": {
#             "state": {
#               "lowestAsk": null,
#               "highestBid": null,
#               "askServiceLevels": {
#                 "expressExpedited": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "expressStandard": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "standard": {
#                   "count": 0,
#                   "lowest": null
#                 }
#               }
#             }
#           }
#         },
#         {
#           "id": "dd832285-9f8e-4a47-9d43-8d53eea234ca",
#           "hidden": false,
#           "sortOrder": 9,
#           "traits": {
#             "size": "2Y",
#             "sizeDescriptor": null
#           },
#           "group": null,
#           "sizeChart": {
#             "displayOptions": [
#               {
#                 "size": "US 2Y",
#                 "type": "us"
#               },
#               {
#                 "size": "UK 1.5",
#                 "type": "uk"
#               },
#               {
#                 "size": "CM 21",
#                 "type": "cm"
#               },
#               {
#                 "size": "KR 210",
#                 "type": "kr"
#               },
#               {
#                 "size": "EU 33.5",
#                 "type": "eu"
#               }
#             ]
#           },
#           "market": {
#             "state": {
#               "lowestAsk": {
#                 "amount": 48
#               },
#               "highestBid": null,
#               "askServiceLevels": {
#                 "expressExpedited": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "expressStandard": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "standard": {
#                   "count": 2,
#                   "lowest": {
#                     "amount": 48
#                   }
#                 }
#               }
#             }
#           }
#         },
#         {
#           "id": "1b5f7716-dbaf-4c2b-b612-0a34048c8cfc",
#           "hidden": false,
#           "sortOrder": 10,
#           "traits": {
#             "size": "2.5Y",
#             "sizeDescriptor": null
#           },
#           "group": null,
#           "sizeChart": {
#             "displayOptions": [
#               {
#                 "size": "US 2.5Y",
#                 "type": "us"
#               },
#               {
#                 "size": "UK 2",
#                 "type": "uk"
#               },
#               {
#                 "size": "CM 21.5",
#                 "type": "cm"
#               },
#               {
#                 "size": "KR 215",
#                 "type": "kr"
#               },
#               {
#                 "size": "EU 34",
#                 "type": "eu"
#               }
#             ]
#           },
#           "market": {
#             "state": {
#               "lowestAsk": null,
#               "highestBid": null,
#               "askServiceLevels": {
#                 "expressExpedited": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "expressStandard": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "standard": {
#                   "count": 0,
#                   "lowest": null
#                 }
#               }
#             }
#           }
#         },
#         {
#           "id": "68340a02-144c-447f-ab23-1fde4f46e8fa",
#           "hidden": false,
#           "sortOrder": 11,
#           "traits": {
#             "size": "3Y",
#             "sizeDescriptor": null
#           },
#           "group": null,
#           "sizeChart": {
#             "displayOptions": [
#               {
#                 "size": "US 3Y",
#                 "type": "us"
#               },
#               {
#                 "size": "UK 2.5",
#                 "type": "uk"
#               },
#               {
#                 "size": "CM 22",
#                 "type": "cm"
#               },
#               {
#                 "size": "KR 220",
#                 "type": "kr"
#               },
#               {
#                 "size": "EU 35",
#                 "type": "eu"
#               }
#             ]
#           },
#           "market": {
#             "state": {
#               "lowestAsk": {
#                 "amount": 38
#               },
#               "highestBid": null,
#               "askServiceLevels": {
#                 "expressExpedited": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "expressStandard": {
#                   "count": 0,
#                   "lowest": null
#                 },
#                 "standard": {
#                   "count": 2,
#                   "lowest": {
#                     "amount": 38
#                   }
#                 }
#               }
#             }
#           }
#         }
#       ],
#       "market": {
#         "currencyCode": "USD",
#         "state": {
#           "lowestAsk": {
#             "amount": 38
#           },
#           "highestBid": null
#         }
#       },
#       "returnEligible": false,
#       "resellNoFee": {
#         "eligibilityDays": 90,
#         "enabled": true
#       },
#       "favorite": null,
#       "lockBuying": false,
#       "lockSelling": false,
#       "families": null
#     }
#   }
# }
#
# 进程已结束，退出代码为 0