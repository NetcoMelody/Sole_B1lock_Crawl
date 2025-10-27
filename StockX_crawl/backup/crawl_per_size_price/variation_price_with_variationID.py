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
    "operationName": "FetchDeliveryOptions",
    "variables": {
        "variantId": "5ffda273-efce-4526-a2b5-96e186cbdf27",
        "countryCode": "CN",
        "currencyCode": "USD",
        "market": "",
        "apiVersion": 2
    },
    "query": """
        query FetchDeliveryOptions(
            $variantId: String!,
            $countryCode: String,
            $currencyCode: CurrencyCode,
            $market: String,
            $apiVersion: Int
        ) {
            variant(id: $variantId) {
                id
                deliveryOptions(
                    countryCode: $countryCode,
                    currencyCode: $currencyCode,
                    market: $market,
                    apiVersion: $apiVersion
                ) {
                    methods {
                        deliveryDateSummary
                        description
                        subTotal
                        expressShippingPrice
                        title
                        secondaryTitle
                        type
                    }
                }
            }
        }
    """
}
# ========== MAIN ==========
if __name__ == "__main__":
    print("🚀 Sending Suggestions request")
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

# D:\Project\pyproject\.venv\Scripts\python.exe D:\Project\pyproject\StockX_crawl\variation_price_with_variationID.py
# 🚀 Sending Suggestions request
# ✅ Status: 200
# {
#   "data": {
#     "variant": {
#       "id": "5ffda273-efce-4526-a2b5-96e186cbdf27",
#       "deliveryOptions": {
#         "methods": [
#           {
#             "deliveryDateSummary": "2025-10-22T09:00:00.000Z",
#             "description": "先发货到 StockX 进行鉴定",
#             "subTotal": 81.95,
#             "expressShippingPrice": 0,
#             "title": "标准发货",
#             "secondaryTitle": "最佳价格",
#             "type": "STANDARD"
#           }
#         ]
#       }
#     }
#   }
# }
#
# 进程已结束，退出代码为 0