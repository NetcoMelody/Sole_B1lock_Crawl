from curl_cffi import requests
import json
import time
import random

async def main(product_id):
    # ========== HEADERS ==========
    HEADERS = {
        "apollographql-client-name": "android",
        "apollographql-client-version": "4.51.0",
        "x-experiment-ids": "4980315829895168,5893473518026752,5548951601479680,4615034602061824,5082413463306240,5863863821336576,5700777599893504,4688922412646400,5947474053758976,5073745673256960,5316781546733568,6734671449751552,5939764506198016,4595064792743936,6274405352144896,4823711411666944,5842018163032064,6657892711202816",
        "x-abtest-ids": "ab-hk-dynamic-postal-code-test-android.true,ab_0zi3v_all.neither,ab_12dul_all.neither,ab_12xvy_all.neither,ab_1e6kr_all.neither,ab_1sru6_android.neither,ab_1x09h_all.neither,ab_2dxd6_all.neither,ab_2l12n_all.neither,ab_3gx6w_android.true,ab_3ny27_all.neither,ab_3xk99_all.neither,ab_4229r_all.neither,ab_4bj0m_all.neither,ab_4nneg_all.neither,ab_5ztfi_android.true,ab_69ods_android.false,ab_6q41q_all.neither,ab_6q947_all.neither,ab_8imzw_all.neither,ab_8r25c_all.neither,ab_8u3xq_all.neither,ab_90r9o_all.neither,ab_95odv_all.neither,ab_9a2wj_all.neither,ab_9fn6j_all.neither,ab_9qwls_all.neither,ab_a1gsn_all.neither,ab_a1uoe_all.neither,ab_a4mxa_all.neither,ab_a6imz_android.variant2,ab_aa_continuous_all.android_b,ab_agzb4_all.neither,ab_amv0e_all.neither,ab_android_sell_faster_global_expansion.true,ab_b0lfl_all.neither,ab_b0tzh_all.neither,ab_bgmm0_all.neither,ab_browse_search_graphql_android.true,ab_bu42t_all.neither,ab_c9kg3_all.neither,ab_carpb_all.neither,ab_cb7zc_all.neither,ab_checkout_confirm_purchase_text_android.true,ab_checkout_review_order_verbiage_android.true,ab_d8yo9_all.neither,ab_discovery_color_filter_all.false,ab_drc_chk_sell_intra_zone_all_in_support_ios.neither,ab_drc_chk_sell_intra_zone_all_in_support_web.neither,ab_ef9vp_all.neither,ab_efozi_all.neither,ab_enable_paypal_bnpl_android.true,ab_eu_vat_android.true,ab_f0pga_all.neither,ab_f7l0q_all.neither,ab_fdg98_all.neither,ab_fu7pq_android.true,ab_g3zha_all.neither,ab_gbjhy_all.neither,ab_gdgws_all.neither,ab_ggc8y_android.true,ab_grabp_all.neither,ab_grbq0_all.neither,ab_gxdz2_android.neither,ab_h6ame_all.neither,ab_hist4_all.neither,ab_hs551_all.neither,ab_htirt_all.neither,ab_hzpar_all.neither,ab_i2y4k_android.true,ab_i7vz3_all.neither,ab_iq9hc_all.neither,ab_j67v4_all.neither,ab_jhuaj_all.neither,ab_jj4k0_all.neither,ab_jr638_all.neither,ab_k7h7d_all.neither,ab_knu9v_android.neither,ab_l3qx6_all.neither,ab_l88fy_all.neither,ab_lblnn_android.neither,ab_m1lzy_all.neither,ab_m6ocb_all.neither,ab_mhzc2_all.neither,ab_mi2jq_all.neither,ab_mk5q4_all.neither,ab_mngh0_all.neither,ab_moc6y_all.neither,ab_ncuqa_all.neither,ab_new_restock_pdp_android.true,ab_njs9e_all.neither,ab_oh5mh_all.neither,ab_oxct5_all.neither,ab_pqaqw_all.neither,ab_prcf4_all.neither,ab_price_changed_modal_android.variant,ab_qdhpu_all.neither,ab_qm42n_all.neither,ab_qzzhs_android.true,ab_r3tze_all.neither,ab_r8s3j_all.neither,ab_revert_all_ask_bids_sales_disclaimer_label_treatment_ios.neither,ab_ri9lk_all.neither,ab_rt6ez_all.neither,ab_rveai_android.true,ab_s6npw_all.neither,ab_saimx_all.neither,ab_sdbvc_all.neither,ab_seller_profile_redesign_android.true,ab_sw6qu_all.neither,ab_t963l_all.neither,ab_thz6x_all.neither,ab_ti621_all.neither,ab_tvtx0_all.neither,ab_u7fwy_all.neither,ab_uf50j_all.neither,ab_unkq0_android.true,ab_ut4nb_all.neither,ab_vaxcq_all.neither,ab_ve7g0_android.false,ab_vh3dz_all.neither,ab_w22q2_all.neither,ab_w5s5e_all.neither,ab_w8yox_all.neither,ab_wvioi_android.true,ab_wxcu9_all.neither,ab_x9ydr_android.true,ab_ybl3h_all.neither,ab_ycyfe_android.true,ab_yuqey_all.neither,ab_z5d2b_all.neither,ab_zbgo7_all.neither,ab_zcjc2_all.neither,ab_zfpmw_all.neither,ab_zjz5s_all.neither,ab_zk1ar_all.neither,ab_zksq0_all.neither,ab_zwxog_all.neither",
        "accept": "multipart/mixed;deferSpec=20220824, application/json",
        "x-api-key": "zWW9iZmfu02CDfd9bCWnZ29mKLgHC9AJ5kjUHvVq",
        "app-platform": "android",
        "app-version": "4.51.0",
        "accept-language": "zh-CN",
        "x-session-id": "69b90a6a-70ae-464f-b054-5f015e7c8c6d",
        "x-stockx-session-id": "71294c90-a654-42a0-a781-e8b48975b672",
        "x-drc-feature-localized-sizing": "true",
        "x-stockx-device-id": "bc95f2418c78c9a2",
        "user-agent": "Dalvik/2.1.0 (Linux; U; Android 12; ALN-AL00 Build/60095c0.0)",
        "x-device-id": "7a12-9699-a32e-6eb2",
        "x-px-vid": "980857b7-a7f5-11f0-b9b5-8acb3817969d",
        "x-px-os-version": "12",
        "x-px-uuid": "e3ba0908-aa2f-11f0-8c5a-7fffd28a30ff",
        "x-px-device-fp": "bc95f2418c78c9a2",
        "x-px-device-model": "ALN-AL00",
        "x-px-os": "Android",
        "x-px-hello": "VgBRUgMKAwseUlIBVR4CAlUDHgtQBlIeBFVVVVcBC1IAA1VV",
        "x-px-mobile-sdk-version": "3.2.1",
        "x-px-authorization": "3:e62fdc2cb6caf4653b8c4594ba29c8bf3d63501ee5e90b5d07da2a6727a873ba:8LtQjWDk9z6R/B2zy4Cb08pjrLg5i/ZlBs7aShXaNNEraF5RaejGk4EcEWkl7o4ee0GAiZV/wfsPXbUVNJbW0A==:1000:XOPN0rKOzbVaDgkAb0t/0Vw9/0Zi5oM4NuLIejrJmPwWPdvuN8QQdvrUQ4YiLGp2SVmLaubF/YqOO8LInzkTQ2M3yUFopp47PY64NfzAYXvKyQo6voy6Aub1lPMhMe0MDydCVo2I4PC/YiK0bFPDoOY1ImMTzejFBftHXwQgB2NZ0gcBZvkoRijWOnsNdOYb/ChdkMRqg0dE1QoBP1ZhCZ4b4Zc9McFyYoTvQVw7XcI=",
        "content-type": "application/json",
        "accept-encoding": "gzip"
    }

    # ========== JSON PAYLOAD ==========
    JSON_DATA = {
        "operationName": "SizeDisplayOptionsOnly",
        "variables": {
            "id": product_id
        },
        "query": """
        query SizeDisplayOptionsOnly($id: String!) {
            product(id: $id) {
                variants {
                    sizeChart {
                        displayOptions {
                            size
                            type
                        }
                    }
                }
            }
        }
        """
    }

    print("🚀 Sending Suggestions request to StockX...")
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
            # print(json.dumps(data, indent=2, ensure_ascii=False))

            data_field = data["data"]
            data_product = data_field["product"]
            variants = data_product["variants"]
            single_sku_sizeCharts = []
            for i in variants:
                sizeChart_dict = {}
                sizeChart = i["sizeChart"]
                displayOptions = sizeChart["displayOptions"]
                for j in displayOptions:
                    size = j["size"]
                    size_parts = size.split(" ")
                    size_type = size_parts[0]
                    size_value = size_parts[1]
                    sizeChart_dict[size_type]= size_value
                single_sku_sizeCharts.append(sizeChart_dict)
            return single_sku_sizeCharts
        else:
            print("❌ Response:", resp.text[:500])
            return None
    except Exception as e:
        print("💥 Error:", e)

# D:\Project\pyproject\.venv\Scripts\python.exe D:\Project\pyproject\StockX_crawl\detial_product_all_sizeChart_with_nodeID.py
# 🚀 Sending Suggestions request to StockX (query: DR5415-100)...
# ✅ Status: 200
# {
#   "data": {
#     "product": {
#       "variants": [
#         {
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
#           }
#         },
#         {
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
#           }
#         },
#         {
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
#           }
#         },
#         {
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
#           }
#         },
#         {
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
#           }
#         },
#         {
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
#           }
#         },
#         {
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
#           }
#         },
#         {
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
#           }
#         },
#         {
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
#           }
#         },
#         {
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
#           }
#         },
#         {
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
#           }
#         },
#         {
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
#           }
#         }
#       ]
#     }
#   }
# }
#
# 进程已结束，退出代码为 0