from curl_cffi import requests
import json
import time
import random

def main(sku):
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
        "operationName": "Suggestions",
        "variables": {
            "query": sku,
            "sort": {},
            "staticRanking": False,
            "browseFlow": "SEARCH_TYPEAHEAD",
            "adsEnabled": False,
            "market": "CN"
        },
        "query": """query Suggestions($category: String, $query: String, $sort: BrowseSortInput, $staticRanking: Boolean, $browseFlow: BrowseFlow, $adsEnabled: Boolean, $market: String, $country: String) {
      browse(
        experiments: {
          staticRanking: { enabled: $staticRanking }
          ads: { enabled: $adsEnabled }
        }
        category: $category
        query: $query
        sort: $sort
        flow: $browseFlow
        market: $market
      ) {
        categories {
          id
          name
          count
        }
        results {
          edges {
            objectId
            adIdentifier
            isAd
            adInventoryId
            adServiceLevel
            node {
              __typename
              ... on Product {
                __typename
                ...BrowseProductFragment
                market {
                  __typename
                  ...BrowseMarketFragment
                }
              }
              ... on Variant {
                id
                product {
                  __typename
                  ...BrowseProductFragment
                }
                market {
                  __typename
                  ...BrowseMarketFragment
                }
                sizeChart {
                  baseSize
                  baseType
                  displayOptions {
                    size
                    type
                  }
                }
              }
            }
          }
        }
      }
    }
    
    fragment BrowseProductFragment on Product {
      id
      name
      title
      productCategory
      primaryCategory
      primaryTitle
      secondaryTitle
      listingType
      media {
        thumbUrl
      }
      variants {
        id
        hidden
      }
      brands {
        default {
          name
        }
      }
    }
    
    fragment BrowseMarketFragment on Market {
      currencyCode
      salesInformation {
        lastSale
        salesThisPeriod
        volatility
        pricePremium
      }
      deadStock {
        sold
        averagePrice
      }
      state(country: $country, market: $market) {
        askServiceLevels {
          expressExpedited {
            count
            lowest {
              amount
            }
          }
          expressStandard {
            count
            lowest {
              amount
            }
          }
          standard {
            count
            lowest {
              amount
            }
          }
        }
        lowestAsk {
          amount
          updatedAt
        }
        highestBid {
          amount
          updatedAt
        }
      }
      skuUuid
    }"""
    }

    print("🚀 Sending Suggestions request...")
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


# 响应内容
# D:\Project\pyproject\.venv\Scripts\python.exe D:\Project\pyproject\StockX_crawl\browser_product.py
# {
#   "data": {
#     "browse": {
#       "categories": [
#         {
#           "id": "sneakers",
#           "name": null,
#           "count": 5
#         }
#       ],
#       "results": {
#         "edges": [
#           {
#             "objectId": "aafa5e04-6509-4ff2-90aa-8742ec9fd6d5",
#             "adIdentifier": null,
#             "isAd": false,
#             "adInventoryId": null,
#             "adServiceLevel": null,
#             "node": {
#               "__typename": "Product",
#               "id": "aafa5e04-6509-4ff2-90aa-8742ec9fd6d5",
#               "name": "Football Grey White Orange Blaze Pine Green (PS)",
#               "title": "Jordan 23/7 Football Grey White Orange Blaze Pine Green (PS)",
#               "productCategory": "sneakers",
#               "primaryCategory": "Air Jordan",
#               "primaryTitle": "Jordan 23/7",
#               "secondaryTitle": "Football Grey White Orange Blaze Pine Green (PS)",
#               "listingType": "STANDARD",
#               "media": {
#                 "thumbUrl": "https://images.stockx.com/images/Air-Jordan-23-7-Football-Grey-White-Orange-Blaze-Pine-Green-PS.jpg?fit=fill&bg=FFFFFF&w=140&h=100&fm=webp&auto=compress&q=90&dpr=2&trim=color&updated_at=1729142748"
#               },
#               "variants": [
#                 {
#                   "id": "b32f53db-f477-4a73-b672-40a392fe8d4b",
#                   "hidden": false
#                 },
#                 {
#                   "id": "5ffda273-efce-4526-a2b5-96e186cbdf27",
#                   "hidden": false
#                 },
#                 {
#                   "id": "032cc4ab-cd16-4e18-8e63-04b7aa0eb823",
#                   "hidden": false
#                 },
#                 {
#                   "id": "5552458d-e8ae-4d3d-a361-8cf8d7fad86b",
#                   "hidden": false
#                 },
#                 {
#                   "id": "c0be0518-51e2-4b88-a358-04ed17e7580f",
#                   "hidden": false
#                 },
#                 {
#                   "id": "b923a43e-aa80-48e2-a602-7a64151732bb",
#                   "hidden": false
#                 },
#                 {
#                   "id": "90f59f3b-6acf-43f3-a155-29b11c841a84",
#                   "hidden": false
#                 },
#                 {
#                   "id": "98d6bda2-90dc-4bb8-97b5-30b2385fecad",
#                   "hidden": false
#                 },
#                 {
#                   "id": "f966b83a-88f5-4ac4-903b-702e561e515a",
#                   "hidden": false
#                 },
#                 {
#                   "id": "dd832285-9f8e-4a47-9d43-8d53eea234ca",
#                   "hidden": false
#                 },
#                 {
#                   "id": "1b5f7716-dbaf-4c2b-b612-0a34048c8cfc",
#                   "hidden": false
#                 },
#                 {
#                   "id": "68340a02-144c-447f-ab23-1fde4f46e8fa",
#                   "hidden": false
#                 }
#               ],
#               "brands": {
#                 "default": {
#                   "name": "Jordan"
#                 }
#               },
#               "market": {
#                 "__typename": "Market",
#                 "currencyCode": "USD",
#                 "salesInformation": {
#                   "lastSale": 69,
#                   "salesThisPeriod": 1,
#                   "volatility": 0,
#                   "pricePremium": 0
#                 },
#                 "deadStock": {
#                   "sold": 1,
#                   "averagePrice": 69
#                 },
#                 "state": {
#                   "askServiceLevels": {
#                     "expressExpedited": {
#                       "count": 0,
#                       "lowest": null
#                     },
#                     "expressStandard": {
#                       "count": 0,
#                       "lowest": null
#                     },
#                     "standard": {
#                       "count": 9,
#                       "lowest": {
#                         "amount": 38
#                       }
#                     }
#                   },
#                   "lowestAsk": {
#                     "amount": 38,
#                     "updatedAt": "2025-10-14T01:48:03Z"
#                   },
#                   "highestBid": null
#                 },
#                 "skuUuid": null
#               }
#             }
#           },
#           {
#             "objectId": "14d8fdf8-e7e5-4c7d-998b-6f6b17615677",
#             "adIdentifier": null,
#             "isAd": false,
#             "adInventoryId": null,
#             "adServiceLevel": null,
#             "node": {
#               "__typename": "Product",
#               "id": "14d8fdf8-e7e5-4c7d-998b-6f6b17615677",
#               "name": "Black White Metallic Gold (PS)",
#               "title": "Jordan 23/7 Black White Metallic Gold (PS)",
#               "productCategory": "sneakers",
#               "primaryCategory": "Air Jordan",
#               "primaryTitle": "Jordan 23/7",
#               "secondaryTitle": "Black White Metallic Gold (PS)",
#               "listingType": "STANDARD",
#               "media": {
#                 "thumbUrl": "https://images.stockx.com/images/Air-Jordan-23-7-Black-White-Metallic-Gold-PS.jpg?fit=fill&bg=FFFFFF&w=140&h=100&fm=webp&auto=compress&q=90&dpr=2&trim=color&updated_at=1729147015"
#               },
#               "variants": [
#                 {
#                   "id": "512b2292-d178-431b-ab1e-10a53264c08f",
#                   "hidden": false
#                 },
#                 {
#                   "id": "b0fb7661-2f15-4992-8f66-55df204db4a3",
#                   "hidden": false
#                 },
#                 {
#                   "id": "eac1d534-71f9-4296-ba77-1f01c9dae29c",
#                   "hidden": false
#                 },
#                 {
#                   "id": "82dc9881-773d-4e50-b158-b38b5d19f8cf",
#                   "hidden": false
#                 },
#                 {
#                   "id": "a48eff18-9678-4353-884d-57927da1222a",
#                   "hidden": false
#                 },
#                 {
#                   "id": "c4fb9807-1d0b-4eab-b265-f3f7135693fb",
#                   "hidden": false
#                 },
#                 {
#                   "id": "bbab87a6-49f5-49a5-916c-a3438965a7e6",
#                   "hidden": false
#                 },
#                 {
#                   "id": "5c721533-731e-4e20-b863-683c5460c19c",
#                   "hidden": false
#                 },
#                 {
#                   "id": "0dfe2676-807e-4e81-a3a9-9ceb6a0d6e58",
#                   "hidden": false
#                 },
#                 {
#                   "id": "649b4ee3-6b4b-4c99-ab43-6fad17b0a3eb",
#                   "hidden": false
#                 },
#                 {
#                   "id": "bb181a28-cab0-4243-afa4-e6ae33126a59",
#                   "hidden": false
#                 },
#                 {
#                   "id": "eb03206c-d9e9-4a4d-8876-f803902aaf4b",
#                   "hidden": false
#                 }
#               ],
#               "brands": {
#                 "default": {
#                   "name": "Jordan"
#                 }
#               },
#               "market": {
#                 "__typename": "Market",
#                 "currencyCode": "USD",
#                 "salesInformation": {
#                   "lastSale": 165,
#                   "salesThisPeriod": 0,
#                   "volatility": 0,
#                   "pricePremium": 0
#                 },
#                 "deadStock": {
#                   "sold": 1,
#                   "averagePrice": 165
#                 },
#                 "state": {
#                   "askServiceLevels": {
#                     "expressExpedited": {
#                       "count": 0,
#                       "lowest": null
#                     },
#                     "expressStandard": {
#                       "count": 0,
#                       "lowest": null
#                     },
#                     "standard": {
#                       "count": 18,
#                       "lowest": {
#                         "amount": 44
#                       }
#                     }
#                   },
#                   "lowestAsk": {
#                     "amount": 44,
#                     "updatedAt": "2025-10-11T00:01:24Z"
#                   },
#                   "highestBid": null
#                 },
#                 "skuUuid": null
#               }
#             }
#           },
#           {
#             "objectId": "365a9a8d-ebf6-4542-bb9d-a83ba3038513",
#             "adIdentifier": null,
#             "isAd": false,
#             "adInventoryId": null,
#             "adServiceLevel": null,
#             "node": {
#               "__typename": "Product",
#               "id": "365a9a8d-ebf6-4542-bb9d-a83ba3038513",
#               "name": "Football Grey White Orange Blaze Pine Green (TD)",
#               "title": "Jordan 23/7 Football Grey White Orange Blaze Pine Green (TD)",
#               "productCategory": "sneakers",
#               "primaryCategory": "Air Jordan",
#               "primaryTitle": "Jordan 23/7",
#               "secondaryTitle": "Football Grey White Orange Blaze Pine Green (TD)",
#               "listingType": "STANDARD",
#               "media": {
#                 "thumbUrl": "https://images.stockx.com/images/Air-Jordan-23-7-Football-Grey-White-Orange-Blaze-Pine-Green-TD.jpg?fit=fill&bg=FFFFFF&w=140&h=100&fm=webp&auto=compress&q=90&dpr=2&trim=color&updated_at=1729142950"
#               },
#               "variants": [
#                 {
#                   "id": "4993dece-0ae6-40dd-92c7-a6308f01f4fe",
#                   "hidden": false
#                 },
#                 {
#                   "id": "9567b21e-42b1-4baf-a035-e593c0f6a00a",
#                   "hidden": false
#                 },
#                 {
#                   "id": "d990997c-aa82-4e13-819d-804ac494ac99",
#                   "hidden": false
#                 },
#                 {
#                   "id": "e81e990a-2d08-4bd8-836c-f641cc4745f9",
#                   "hidden": false
#                 },
#                 {
#                   "id": "1e339972-d30c-43ab-904d-9930e3831253",
#                   "hidden": false
#                 },
#                 {
#                   "id": "d4fc1b52-47df-406d-a6bc-4c8dcf906ae6",
#                   "hidden": false
#                 },
#                 {
#                   "id": "fe8a589f-34db-4c9c-8411-f4425323823b",
#                   "hidden": false
#                 },
#                 {
#                   "id": "a65cdaa8-3ac0-4669-9ab2-bf59b4987520",
#                   "hidden": false
#                 },
#                 {
#                   "id": "939d425d-7199-455e-bad1-e531af04d590",
#                   "hidden": false
#                 }
#               ],
#               "brands": {
#                 "default": {
#                   "name": "Jordan"
#                 }
#               },
#               "market": {
#                 "__typename": "Market",
#                 "currencyCode": "USD",
#                 "salesInformation": {
#                   "lastSale": 73,
#                   "salesThisPeriod": 0,
#                   "volatility": 0.338362,
#                   "pricePremium": 0.327
#                 },
#                 "deadStock": {
#                   "sold": 4,
#                   "averagePrice": 90
#                 },
#                 "state": {
#                   "askServiceLevels": {
#                     "expressExpedited": {
#                       "count": 0,
#                       "lowest": null
#                     },
#                     "expressStandard": {
#                       "count": 0,
#                       "lowest": null
#                     },
#                     "standard": {
#                       "count": 12,
#                       "lowest": {
#                         "amount": 30
#                       }
#                     }
#                   },
#                   "lowestAsk": {
#                     "amount": 30,
#                     "updatedAt": "2025-09-25T15:40:32Z"
#                   },
#                   "highestBid": null
#                 },
#                 "skuUuid": null
#               }
#             }
#           },
#           {
#             "objectId": "0ab0051c-b7d9-462f-882c-a4b42014762e",
#             "adIdentifier": null,
#             "isAd": false,
#             "adInventoryId": null,
#             "adServiceLevel": null,
#             "node": {
#               "__typename": "Product",
#               "id": "0ab0051c-b7d9-462f-882c-a4b42014762e",
#               "name": "Wolf Grey White Black Volt",
#               "title": "Nike Downshifter 12 Wolf Grey White Black Volt",
#               "productCategory": "sneakers",
#               "primaryCategory": "Nike Other",
#               "primaryTitle": "Nike Downshifter 12",
#               "secondaryTitle": "Wolf Grey White Black Volt",
#               "listingType": "STANDARD",
#               "media": {
#                 "thumbUrl": "https://stockx-assets.imgix.net/media/Product-Placeholder-Default-20210415.jpg?fit=fill&bg=FFFFFF&w=140&h=100&fm=webp&auto=compress&q=90&dpr=2&trim=color"
#               },
#               "variants": [
#                 {
#                   "id": "bfdb3bc3-1a8e-49df-8099-3bf46675c4ec",
#                   "hidden": false
#                 },
#                 {
#                   "id": "1f1fc939-79e0-460c-a059-443e00330b28",
#                   "hidden": false
#                 },
#                 {
#                   "id": "91480c83-f45c-4b42-b779-5bdb8490ad6c",
#                   "hidden": false
#                 },
#                 {
#                   "id": "a879c51f-1818-4824-b112-9491033a7080",
#                   "hidden": false
#                 },
#                 {
#                   "id": "a6bc583b-62b3-43be-a395-92db4afff02e",
#                   "hidden": false
#                 },
#                 {
#                   "id": "ca1b6bd8-cb12-48e4-9602-f89f56aabe96",
#                   "hidden": false
#                 },
#                 {
#                   "id": "8df04e7c-e0aa-4855-ac2a-2b2731b638ae",
#                   "hidden": false
#                 },
#                 {
#                   "id": "38f210a2-4611-489c-95e7-bd3b10f563d2",
#                   "hidden": false
#                 },
#                 {
#                   "id": "b3273813-2bfa-4fe6-9c49-58d529d61268",
#                   "hidden": false
#                 },
#                 {
#                   "id": "5b3ad62c-9a74-4bf2-bad3-8cda3633cb1c",
#                   "hidden": false
#                 },
#                 {
#                   "id": "1d2b3e58-b127-40f4-85a8-e9f2ab66ca8d",
#                   "hidden": false
#                 },
#                 {
#                   "id": "44f0d111-b44a-47c3-bf75-ba2d5f7e257f",
#                   "hidden": false
#                 },
#                 {
#                   "id": "67085d94-ebcb-4434-98d8-8ea19568c4f9",
#                   "hidden": false
#                 },
#                 {
#                   "id": "f3fab61b-482d-4249-9897-98f0a6825ac0",
#                   "hidden": false
#                 },
#                 {
#                   "id": "2a7aac39-4ef0-478b-85fc-b526a4ae9336",
#                   "hidden": false
#                 },
#                 {
#                   "id": "2e674173-81ba-4986-8a4a-7eafa406d042",
#                   "hidden": false
#                 },
#                 {
#                   "id": "3f4b4c59-78dc-4286-9a85-adff49ff5d24",
#                   "hidden": false
#                 }
#               ],
#               "brands": {
#                 "default": {
#                   "name": "Nike"
#                 }
#               },
#               "market": {
#                 "__typename": "Market",
#                 "currencyCode": "USD",
#                 "salesInformation": {
#                   "lastSale": 0,
#                   "salesThisPeriod": 0,
#                   "volatility": 0,
#                   "pricePremium": 0
#                 },
#                 "deadStock": {
#                   "sold": 0,
#                   "averagePrice": 0
#                 },
#                 "state": {
#                   "askServiceLevels": {
#                     "expressExpedited": {
#                       "count": 0,
#                       "lowest": null
#                     },
#                     "expressStandard": {
#                       "count": 0,
#                       "lowest": null
#                     },
#                     "standard": {
#                       "count": 30,
#                       "lowest": {
#                         "amount": 56
#                       }
#                     }
#                   },
#                   "lowestAsk": {
#                     "amount": 56,
#                     "updatedAt": "2025-10-02T21:41:02Z"
#                   },
#                   "highestBid": null
#                 },
#                 "skuUuid": null
#               }
#             }
#           },
#           {
#             "objectId": "d1226205-6a69-4094-9607-e1bcd5892828",
#             "adIdentifier": null,
#             "isAd": false,
#             "adInventoryId": null,
#             "adServiceLevel": null,
#             "node": {
#               "__typename": "Product",
#               "id": "d1226205-6a69-4094-9607-e1bcd5892828",
#               "name": "Black White Metallic Gold (TD)",
#               "title": "Jordan 23/7 Black White Metallic Gold (TD)",
#               "productCategory": "sneakers",
#               "primaryCategory": "Air Jordan",
#               "primaryTitle": "Jordan 23/7",
#               "secondaryTitle": "Black White Metallic Gold (TD)",
#               "listingType": "STANDARD",
#               "media": {
#                 "thumbUrl": "https://images.stockx.com/images/Air-Jordan-23-7-Black-White-Metallic-Gold-TD.jpg?fit=fill&bg=FFFFFF&w=140&h=100&fm=webp&auto=compress&q=90&dpr=2&trim=color&updated_at=1729143144"
#               },
#               "variants": [
#                 {
#                   "id": "e07bb79b-e2fa-42dd-b83a-53f6b790826a",
#                   "hidden": false
#                 },
#                 {
#                   "id": "a0419fbe-dcc0-4573-b464-291ae93c4e50",
#                   "hidden": false
#                 },
#                 {
#                   "id": "4a1139bb-7ae5-44ca-8d8a-c0bef6bc9248",
#                   "hidden": false
#                 },
#                 {
#                   "id": "1dfdc970-44a9-48d0-a386-021d17e4b1ee",
#                   "hidden": false
#                 },
#                 {
#                   "id": "0d77e24b-ebe6-4c6b-a71a-3abefce6f8d6",
#                   "hidden": false
#                 },
#                 {
#                   "id": "65da8409-900d-4ffe-93ba-0c62d8ba7ac9",
#                   "hidden": false
#                 },
#                 {
#                   "id": "925fc067-2e56-4a1e-b0f6-d4de7e638944",
#                   "hidden": false
#                 },
#                 {
#                   "id": "8b80efdc-1623-4bdb-b8b8-0192419f1839",
#                   "hidden": false
#                 },
#                 {
#                   "id": "88dfa9eb-2bd9-483f-a166-123b733c0872",
#                   "hidden": false
#                 }
#               ],
#               "brands": {
#                 "default": {
#                   "name": "Jordan"
#                 }
#               },
#               "market": {
#                 "__typename": "Market",
#                 "currencyCode": "USD",
#                 "salesInformation": {
#                   "lastSale": 86,
#                   "salesThisPeriod": 0,
#                   "volatility": 0,
#                   "pricePremium": 0
#                 },
#                 "deadStock": {
#                   "sold": 1,
#                   "averagePrice": 85
#                 },
#                 "state": {
#                   "askServiceLevels": {
#                     "expressExpedited": {
#                       "count": 0,
#                       "lowest": null
#                     },
#                     "expressStandard": {
#                       "count": 0,
#                       "lowest": null
#                     },
#                     "standard": {
#                       "count": 28,
#                       "lowest": {
#                         "amount": 34
#                       }
#                     }
#                   },
#                   "lowestAsk": {
#                     "amount": 34,
#                     "updatedAt": "2025-10-14T05:06:24Z"
#                   },
#                   "highestBid": null
#                 },
#                 "skuUuid": null
#               }
#             }
#           }
#         ]
#       }
#     }
#   }
# }
