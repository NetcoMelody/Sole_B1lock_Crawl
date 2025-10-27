// 使用 setTimeout 延迟执行整个 Java.perform
setTimeout(() => {
    Java.perform(() => {
        // 获取目标类
        const SwSdk = Java.use("com.shizhuang.dusanwa.main.SwSdk");

        // 创建测试函数 - 支持Base64URL解码
        function testHeraclesDecryption() {
            console.log("[🔍] 开始黑盒解密测试");

            try {
                // Base64URL编码的密文
                const base64UrlCipher = "3YcQgE8nkdnebbb2cX80o_hdwbX1V-U5irCX0h4V4Hwf8sPEJVV7oFCYZmJR7sivs3oQC2Ers5eqfFsluMxoAYei4F8QTMLLrn_Pkc1jk8MqBgcp9no_2jZI32gwvwb2_nAh6S3h8MsGyaVN5WXip6-iBo3htu6e_OgrSxrLMSd4sBTmkNWTKVwspdEHD2C44FQ-BY0BzmVtsZrimIz5Yf7UCXKJuPWBYetWIuIcWW1CZlpTccL18ob9HbJ97WIzgYffOjqPytisOrf2AAXinTTjQ5Vl27ajCrvZuzJ-eSsoaI7MvkeMFJjW1BqFPTxiXGFOHFN0xt678LioPH22N7tSeWuat7iu4iy0JipzH5dWDHq261IImQLynozt-0rAc0jD2YKfJes9Su8KinGfg1mNCNcCUGJGYArGB8O_MtRFe3C7Us3taTsnQIwZwnHWjTrehAZOhNWg2mV9blHpTxA0GFaCUgPL6ycV-JockWjrT4-BQy4QJqgD5yA5NQh1hhW_xCaVxlYZ_4jbtD6uVYrElvE-CCK6MsOI-EuR_KNtf3sO0IcNGYKcjbCd_m4FBVSZ3rC6NlboDcFF6EAjof70EOb6LOKbueH08nZb6R6s7VsSOVvWMaxg05CcGcepM1nLrcWfWCVcV35ZejllUpT1gcCLiL0fH5HxNOGeGfAS5651K1JANj6dX-nxClpS2BCq0HZV5RPp-9ThUth7aVEAmdt3Cv7vVznACa8rtMNqDgNPiULv7r3yGtcDP5NGtqjhPVG1tleTpZV8LMiVnbnkYGI_JA26jqzvZpPIHuT1yG-KDqUt83jqldcixYONsIzKfzBtm0A1HxazLCrUUjsyuX3QUcqyvjG-0QWAh9JqjJwPx1sjGT5qzmPtu8fozPb1kjUhhD5BRPubpkp3JzFDcPZWXz-XcxuVqZ6AWoYBDBhDyEjr0s8TSub1dzzHhNotPyCX9BL30VBZp_ETznDFLYl_XAzibk9SWO6qu6OKo5iDopNBsvn7Jg2aul-i_lubqgjOkbOVv-fTCWLiEvWoOi7nR3w0GQch820SvnC97ijr0Z0xbygLii3Qas9PoOELCeYFwQpL_2-EtrGkuw32SiG4Jq8y-MkNOGQOSGjnRAUtpcPSanXGdHO4w9SX5vNdAI8a5fQolMMVqBHZfHjmyBUehn2jMrZuuSrTRFN74dF8Gy7GTM7T5R3WtE-U02i4s8je-PsEYh7MiCXYtjoRAIqVV6nEMWOsMSiXVisBYyZTbM7tEOv2cl0DsqwtXeFOoI0GjzZg2IORbK78bebq6Wsdo7csgkNAEWezK9doJwdQgge8IyorxpYXraIfN6mrFun8vspCU4jMLEBmffyGPAUbb-kRPjmC_1nDZKRti5gvzQQ5YIkYHA2NaU6FYPsZ3zbCE2t3bnZPRQow8nlrMo4pIsZHYnBw8dILzLKrE2_zmC3Pq6NnQy2Juybn1O8jmz3kWjA9lIgamN0pDK2jpBhivAZTqqGT57Cs46eRte75NCCEg0BSA8QWm0SY8jkRasjvEHgPYfsVZOKpJCxfcPZzqaO6A6zPQebFfCFqEo87o6RG_tG5Bl301qsqaTP-OduCCkU6nPZwDqjQn8JFXQVoovEeb3aJ9Y8PeakKQmYvfRMS1zk-qk8QBCTqbBPly-s2dS9b7e4DcsbLQP_cOkE4y3aATMEmhgOeHU3VNAWtbBJ1JcRPoj7qXGpifhjeN2Cp2-PcwRUv9SGePR_zl7M4HokqfO-ClbbcsehTiQW_5i3bQgu8ew0g4-YPB-NevTNPpWyQV4ETg3N2BC7Ew_NBpDuoo3xoUVCqYT6RM4JgHCvN1y4fmdGHHeLgpddQXCZP-b1GdzMnsBt-22KdAge1CvNgq51HY96HvZDlbgYfFhuSrxPRF_FtJIKX3EZknTHhcPTScYctgeCx91dYX3L8znmLvI5hydePoh276YzJ3ZaW4k0XCzXQJST78tw9w6w-csEyT2THiganIiLWGIl_LoEiS_kyHD3DImmEDM_3ezUuERDEj1GCPF1cpqez2OVr7JSvvaXumWX1UgAGQOrE9FJk1wxKF9OJ3gGnLmAFPfidhVyZ4UaTSMHA0SfVy_3zSLP59xu0AI38LOvf9wTFjtALnaBTm5sHSjGwygOml8lc2t_VDbek4A4UzFZ0PN6O76kFAWNbUXv9gBBNVjmrTVcHo-uf4MCAh2cPwMfBKW8uOdnfiBuI4YwUgYHMr_OtsNxXk4l16EwaXm5eMom-zjcUAc5pXGxe9Y26_I9mv7taI0dlpGSGzA7bO_YQtlZC22D6KTXg7asBGAbdhxHsch0ABSTzJAU11eNEiMuUvVjaVWP1sfK-qUQwdv8JbHojWQj_Ph9sAcarFHqDidDqk5rDcYsSkx-PVZmETH6wdOqTmu7HL-BY7c9rrflJ1ndd-_autA71Rlwt6hqKg0dUQDSeuWh_KZIhR5kwUpazorGZP5ex36Nz-EHCjL2cQfkrGtGj7OoZnEGJW3PbC4S-DqbtDP3kHY9vrCjJv33fUtfKCY7eZ5F_glFoLt4auOngJcl3-i3oMp8hPk0xIy8QYZ0RRh-3Tqg1550jG1LTV7ovkQuZegxWZ_ZvHDcRvr9MstIf5cM3ZAsWFBFEOkkIm3m1TgxYUmjYH32JCi0CHoKvKT5UFG0KNzpED77BVdcjDrqTMAa3GadKecqqvvLtlBT8_R_z4bJH9niat5CkgR1iltXuktPQARc14qE-6coVzfI8yqX0z9S_MwMIEmtgA1hKXEj8wDMvr9hbkr-3SVIrSfBV7UZLWR_xXKnbd-JtFKs0G4SHQahTKrWegFpgS9Zqdtxs46vT23-ag-vn3RfhPOn5mwJ-hRROP97Asb1XobuVtdj095T7rdGbN1bplke4J1fdoRzJksKaBkPNOhfn2Fw6mP24Drk9NS0PqqsmDTfxEKaO7pZke71IYNuTZz3DccfOZXTbbRZjEuiqOdyCmgGUdI33vHqMIp2FuSboQ5Ukre0g0-W4hdo67h6rOn4pmUAsDlNW86BBtJ-zzAJXMPK9eDl-OZ0hRtQykV8v0V7kciEQFJsSS10HBhn-3GodgaVNnTrvEqbI1MIBfuX9DIlZN73JOEcJhJrYrj3u9HJJusZLjugfFAicN1_TToBOVv4H6YN7qqY9cVgVaywvkAyZYnWmHcQ-w5iSrdlC0mp26zExC4XxYbvT7Ff4n3mRVbuntZ8v0Y09rAtFVXQxiST0R81yZznyNwNGZ3949S1yPlI9GsSjZZkfWBWmq_IS0pbYeJZaMX5NihkJBYm0w4V1Q8tMwj1ZlJ667OmB3kvi5FMnMlxMCqx0Zp-N_ev3pSrc9nIN5MW_tDQw9L6C_FLCV6JZA00Px9cBxkXS9-QLPwcxejKmVJ6NFUqZZg7dUc0iLNJV9wZvNorXTFq3-DYp2OycMVLXnV7mtaLlV1WvzFRBr4_NDQTs5p9SUKA86I3_4BqYPyFosJX5PW3MtY8ussnl0xJbjZpfYTp3aaAPgRkqcD9qWY_9MlDMArab6FuQUyGfdW3eM85P_wTmwHU1NMu0XLLIctCJaiYCBa9K2fooHoc61g4kICtNYYlstFDGPlQu2tPW2tTOiydPB6SPppP7C4DRUtw1m4sfRNEY6HoR6nUAiIgURW-1PLW-4ZyzhXZhX3DRL-uwFEcNkya9Y3DZ5HEbMesO1hxkSxryJfYTAbk2AF4ysVZ0D9iiX6OV_4Zxh5OLyh2EFk4R2IHy2C4l9d-tXYkrJd08YcS2FZSfok6cuVZbfX5QTHzAfmcYiOnO1OuE3bDhUmjldBQlr-RgR4u4tBr3JPShg9GS03DILUda8e71BhtFKxQXWcqtie4t9D8FY2w7LCJTQuaTgEjTVKIp97e1qXtXslbMUP4lzWsLHYrGBk5U62ce0Ey6ubNTpVGpMUoo59nFjyK9B7zQbrbDLd67MLxgRjl7rKODPNcBlxE4wLONb96IzNYWuvlA0SadOYg2bxxWpINJpezxfDiZKKrj4D_B15QwU3ylywUTJkp0Ac3qmxWxiACu846mOG92TDIM84Uz2S5j68EaYWmKPzpyE57fKA1AlUz4WliAKoq3swMM_fF7EgeOQ4k_B4K4ejO7YVuYEIyXtxTypxS6Mef2L4nOS2G2bdMWC_PpP1Euidvo8hBHm0DTpkIJ8r0Toc-4aK8bsPcXDZvh8Dc0k0nkFz3giHm39SxzjLwgevPKN9buJM3Nf_aeH2DDxLOk3FHKcNmF6iWahg-AzcWDOYBJeavkvHRyiPk825H0Wmx37zrecHuIZY12aUDH4LkHh0nG5Z5Q1VC5GwGtYIPr2CEa34eF4gVI_chGgHdCa73S7-9e03FhYEUCXfOwh-P3Q0LoteTkR0ZiXpaP-QUUDqAG7uD4tz3yj8gMTkQDhv-7TDRXyyYnlp7EvnCkZNn826nh2aAUKV5-Osouc4XPkc0ztLfgc2k_VO91x13iuLu_57BEGoyLiVS-vRPAYCB9NoD_W-NJQ06GPh2pmBselMQ33xhps_vqhWLsdKCIIp2xh3nr1Cpw5kuQbd_nryBFurQvFphX4QRD7gjv_fd5THCE--7qBY6b-EiGrBGf_L6pLBnwUv0jHjjgDkvCrkyYxnS_G98bwUZqx6hb7Gdgk1zTR96xTGwiiZlkg0Mr6Sby84mmvaoJuxDEqSWCjofmts_L-yd3L3k1hcCrjy7jRqfHqkKSuEdL8DcKsI0zG_nmsjqY9YgecrLZiHmk6qhZTcqizEt7Ljozg5Bdagrdo5bTP9DINJrNi0D2Q3AFqXFHcjR8Z7srJoejQM-wBJdb4hnTgn0z86CGxA5NGqWc4_sfSsW-ZP2iKeTjXZTCS4YQ3To-aqtMbPNgTapp-9B9FGnhvhAlmnr2CDlCxVZYSuaaVIzCA0O2fJW1T2KPxmoelNf02SNXbIUFe2ctc-6DJfqqkWO7bXexy7w1W61pTeKyHzrfbD_3XsFmvBC3lFGYxB7W7N6vbfPro2UHRGCYqsjf0tdWhGFgYMoLDczHhads5-b2pJ_-F0AyGvVjUs4d9yoybcppPE-xhz0ckO0DDt8lGDI_ybPaG_nUP1IoC3G7cZEX5UDD1NoQph_lZiA9jRj7pUTBOVEluwmQJJ6JKxg8j600Jl5_V-pwoHAXmLAiHzwFoEDJFHJYZwjm7q5rduWuaU5OkUMbeFoqRTPbPFu0J--n7M4uZZBq3rI0Og4s9z2HImL36lj84xb_p6xQ-o7oaSKy_NkPIQ_aNAWgJPEtWVZ0P_hJHs6-jtjUjKzY_mVyC_hPThH0_SX_6mt9tJl5u3kk26cZI-9P8QFPQ63q5Hm-az5QaUzfT6FB1wt0CtgO7UvTTyOz1QvVLEzmqsTM_RiLyrZPUDppweTxbXmR8D13VZ42bW6veayFZCeYgmu2IZ3XKwRl1sZf9tSsXDGwf0b8k98XHf3it5RtBEcAg2fmi0eCNjFkzA7MzGsBq9Lta1i90dxnl12mCaTW3v6aP4GYhKg61DOig30REtjGG9AD0TgC0W9Cdk61xlC8tAHwAB6up8hB172LHrxzgDOcWju1udMH2MI09Op9-wExeESjj6e_Hs4B7yX_7eglnP5E0XJcfPZPQgPdyE9isUA71yUr7tbIeBUfos3Z0zQd5iU6fvL0CAAWgGOS8IugynDcsXZbH-xtBtBF_cBEtZYyLBV8P6wmtYj8YQwrWzAjk6Fdel2fn4DlZ0UGJsgACS_T4XZ56TSbP1-tNmzDvvWPVZ_OGzHUfHRZNTpaPOX-r8gYmYUAECGRQpxbCWAP3O7KRdAYCPEwnbnjd7D7oHZo61pYaFZKhNSeY3Lrawwtux7pKGB6cpzp7ppT1f9ZskzDq6fUKgnhrHkHSayX2jvR2AjyHeNGBc9AjpMb8Mj5MHUS2cakmOGnq6m_APq1VKPgyj-qFoGKI7sqCXUOnQbBMWWLgFyJhZiaUTe1PX8_rAk3kHPzaSXJ_xsAxX7mcwIAOciht5SQivGdNYqksAt-GdfDwq-GxcJZQDg7XZS6uNH67C6wfh3KkRvrnn-jcQ38nDiY24p9tnBIpdTfZbI6wVGO1nifWU9HiopVtkY3rmwFYkh3FuX4_so6SliWYLq_So_VM5F9oFEVpPRMZH0fGX8AgFv4dQdPu-HWrwHm3haSj_8wZQuRzlNsBe2v0e-1ExxgApjDZ-yhlL4fgJVpqLbyaouUulDAC-qeCvOFAePWSgO1Co5FJF_Lb9tKpGW_CoHw0EhgRcjHbc1Uj-_9jqfbfFXyCcW0DVsYYBHDPSVFwv3WmvLQ8xtwxXiFDwS9dLYIHqLlkCNvhfJMtc5Xku_HU70V52Z8rk7CLT7YhDcsXcYd_u4_hap3UdSHwmR0fnc-Y0com8txhAFCe-omLAaNDLonJ44vXrxC6i1jDQZw_m9NnMQl5qN-JLLw61c1Dd-3w-hjZOmC2EqsZMvzlOWvTEQJjUKJO3FaiP8o9Us3gu-buMSGvZhlJ3thvLJiswKh8iQqKPNaRq4DicTig4rFRmaRSKDis0Qw_HWnA9ZJZEcEKb96R10oDOyEE0WZN5Lc5KU9KyyvDSg2fjLaQAPRVJandLVgIv-qXviYowfk28czgHnjtmjyRavY_Cd7x9Incd3z35w9B8mpMu4hVQrLv8ubSiSNTamErMe-HLimejh9t7R9tY2skRPsebh-XpTKCEE0pCffluF-kaMfCAqqRDCwOVFNJSlw2T6VpofeqglfvrS1AqG-Gw80456ak5eFoLiIVlCK4Xa_ojv-q2Y07GkkhtixtsJu6dQofOJpwdoJabJaZoXTeiON-mbamJd3rg7mrws2z81DXnv5SIxmP0c6vutPHRMcEPveVue9LX5OtLjApNSBth3gKC9qoleXA3R_giBa4fdel1r1PimSzIAcCEWRyiHfgG0hfQ67pniNNg4o4YhYETTFqw0YH4urtsf6H0CGQU-JmBgBxEF0u86QkLx_nGPlCdh6g6GrH_kK7Ur87Dgdw7awgYaNj2t3jRn2iLcAip7KSU7dPuzR-BWhUDahe42ox1VjjnV0NbT8a-ZxaO37_LNPLg1fgeSZL3hRigxTTq6PXS582YT9aXU6EIfdTks3_M4SGGzt-cHoqoyi2hM6MFs37TZCl4Ta3-X5e0dcVjwzCyPZ5L_QcvdNVXbd68ZNdeL98o63RseGsT0M6tQRP7q3hinv_iIqDGQUCyyl4j-UDXtVje0Nq6sI73djB_97nyy3aloi7S4iXmMpf-qmT7lyOSbWVwiB9_-AUo3mg39gfeSTPtyN74mrzk16pt4ZaAp5mdSnCjrF0SNfYFkDQ1jg7Fx5XIEol7fY03bMVaUS3ND2INF8Cfne37HON3iX8NmWvzQkKbgEAdLj5beW2xLNGzWcKe6nMIAS1LxUbv0QifnQ9fURHk4NRJ-m2m0GPcxP9-Jrq19XaplXhm0jjneQdxYOc1dwuE0GvTZYsUtJ4oNfiTH7LWz0RXX_26o-fXVgnFgBOrUEg32LyNgBuXBsADHfGFQ-AM5bJ3JgzCxNFwukfWZYLcap08h390RTrARuuqMspj1avwfpMbeJ9qkD2TNzxctsW5WZQ7DG_ikYT6e8TF4I7R0NB8c8CzqF8RESFYNJ4zfbfJ8P2DaS7-yIXmrBehrdncuySVRyCSeu1KCxEc9C3vk8YWpyOFwcPLExtYQUHoInF6dKl9JK8nbILWERl0jjvEerVQD24rc0D1V4va5pBksp7YJQNpTInnu9_Srs71OvdRxDQFwxxnrrCx4TIFwSm9kbGLdbEVuDpxzP0JnnN2wdHAc-odPD32Y2jLpqfC_WIkXXGq0fRt6XXZ903llzqx0cB-vya2uofO7LpvMOfc85GVv88pX7CZIurZed6SNoImQ0YWxMJ2AxkgRkzTV9U41YYmYL56X5V9R49BnBH-Ea3WPr1E_7_xwVUmnxp8VD__rqFGTzXek_CRhVBG0uAOoX8gi1YGqZNmtx2H0WWYsMZ6R-TNtfVXxR-uvy7xHbcXg6BPWEytCTMAnnGIZRMHHOvgbH0VNl1KlZ8e6KNE--6SUiFkI57BhMXAVteUZrbkSJ0q9vywRxZmTdANCV6OuvG2jML-9ZrTjF0TaqwuRqrU_3Gqk9-jQ4OcOWu1oi3iosbl_cZRcxbrfW6e9cebmpuYG-Ve6RRskFwLMLdcoAAc3LbzPwU5z8qsF7axv0lfbfF79cVEpq-TVT0SDbugxwcWzFmpykRc-YIUoLZ2BYWe5Z_ogWFB1dTGn5W0NUsILvOiGmNeIQgWY1LoRTvfrIOtJF195BM_-1nRjTiXO0Uh_YF5pMg7_1-LFZf2RIHQjQy2hWHqMxlWUeG4sRV_zzfcLlXk-uydbvFw2iEDXXlMkeomfkvdDvCQVjmJK7i_50aezMi1qU6aDng7KsdhWEg9yykPcmC-1agxUfCaoT2WWAOcSeqVHntUth_qQsxTCo6hUzsX77a7VMERh3TRQkxAcKUlftSWT3H8acrt0EP_yXiX3aAa8NGBGaurv5Z0-gruSWisRCVZgC6yDExDBSvj1HsLWYkL66iBargUpMd25IegMmoczzBrRBu6w_Zs_a30gqo1YwqVnxlrXIawLvueXQvgg5uQSW6NDEpbVEjk86YlG_lK_scKzQJaywhKe38ddzyst8vfYILzZhfbqmiQ3Qk-41OsAEBdoQZu0kFXVtEix3ouDkKk6YLasxKsfi1blfIDLgOQmBbRkrj_W8yntdhG2C5JbSckbeG4Kt2v0X7MUCMD9AMZk_tayHR7xjgUVoFuzSTcMyfzSmhOOUy8fQrpILRTjwKSu6Mnx4YiAOnUdVZ7dhPRPDaeN0XhliFN4slXU9V3ZPFumaP_NDjaWQyvgH6qi2KAspVHhpSuBanZUwPkRk1s2W2eML58_tyXUcoa7_FEmNi7c3i_fmJ8WTjhaWsB7KWGn-BIQOLr0Z1GL0FFd8_RUoYjOTGifV97Owpc9pMmNlXAyinVW1W8u4OWaMonw-GD9Nxc0orCFosl_80dRj9OHEqb1Wax5mqF12-FFS7r6C7J-FxlN8B3gBkNNtOfUA7pNpr7w2Swl95bLs2vONc9uTvGRPFUh3JWUZH7XV0Bf7N6RjJBAte6uRTB-HS3mzGwnH1rRYPpur6F-4NOO5QnXxxSzxilMbE_ybpT-lVrdVPl3yKOjAEOCGC32cnU1Bi8B0e6GPX0ohLsrGNDYnmmCmULoYR1zd7S0sMs3-NtoEh-fpU7SH9tH3MXc1LEgdQJKsuGr6a4aaxPZ_vb4tgTNvK66Iw1l1jU6Mx-4kWyfuabl51qy-ArrhTvnkhNszv33XVLRPk6tXYglvsVnHf5hIzgCbgnlbp-enayCXzy5m1AzeOQSJ1K40QQdajwYjQ6ENWFndbuq-hWfHJrZcZ6FygAOZcsKTQ2lyBqqa4fS_cyJqwco9bMt3h2xDRJ27oqFk7NF4U8F1UhSQCGB1_5mfEGCi9jZCwIb5zSShW2Pum9hrrA3o0rwfIDyRmKuQ4O_3s4sniFIXbwI5PSFfrdVy8YvKTnl_wlROH77Diw-tZOgKwJ9JBy7wfpGRSE350_QuQjE6ejQkZ_w3U3T8El0uVLgWj5gHChFhzUIfmkIHsmYIaBHArHhj6qmfOvICCmNCAVFbKS0RfdJmDcqTOpS_eHvouZYjR-UVVcfHWUDRXYEosNUJS-lR2OdpEIpBFLhWuVlwNglMJyWrcBXw1DlGGRhiql2mN0RFm2-pIIxtK8e02qBJC1flcvRAsReoqEmVvugzN8EnEZe6IQJvaGn9E4vkoWGbEQKmaZXgPErGwWBTWPlRU1hRb9YncO9XMBphRWwzeIoOVYhRROmEYdR5sDBGX3hhouHyZFjuJdACMp71_J-TFi8ZZ_E=";

                // 使用Base64URL解码
                const Base64 = Java.use("java.util.Base64");
                // Base64URL解码需要将 '-' 替换为 '+'，'_' 替换为 '/'，并根据需要添加填充
                let standardBase64 = base64UrlCipher.replace(/-/g, '+').replace(/_/g, '/');
                // 添加必要的填充
                while (standardBase64.length % 4 !== 0) {
                    standardBase64 += '=';
                }

                const cipherBytes = Base64.getDecoder().decode(standardBase64);

                // 调用 heracles 方法进行解密
                // 根据之前分析，heracles([B, int, int)
                const oriLen = cipherBytes.length;  // 原始长度
                const extraLen = 0;                 // 额外长度，可根据实际情况调整

                console.log("[🔧] 调用参数:");
                console.log("  密文长度:", oriLen);
                console.log("  额外长度:", extraLen);

                // 执行解密
                const result = SwSdk.heracles(cipherBytes, oriLen, extraLen);

                // 尝试转换为明文
                if (result) {
                    try {
                        const plainText = Java.use("java.lang.String").$new(result);
                        console.log("[✅] 解密成功:");
                        console.log("  明文:", plainText);
                        send({
                            type: 'decryption_result',
                            status: 'success',
                            data: plainText.toString()
                        });
                        return plainText;
                    } catch (e) {
                        console.log("[⚠️] 解密结果非UTF-8文本，字节长度:", result.length);
                        // 可以进一步处理二进制数据
                        send({
                            type: 'decryption_result',
                            status: 'binary',
                            data: result
                        });
                        return result;
                    }
                } else {
                    console.log("[❌] 解密返回空结果");
                    send({
                        type: 'decryption_result',
                        status: 'empty'
                    });
                    return null;
                }

            } catch (e) {
                console.log("[❌] 解密过程出错:", e.message);
                console.log("[🔧] 错误堆栈:", e.stack);
                send({
                    type: 'decryption_result',
                    status: 'error',
                    error: e.message
                });
                return null;
            }
        }

        // 暴露到全局作用域，方便在 Frida 控制台调用
        globalThis.testHeraclesDecryption = testHeraclesDecryption;

        console.log("[+] 黑盒解密功能已准备就绪");
        console.log("[💡] 使用方法: testHeraclesDecryption()");

        // 自动运行解密功能
        console.log("[🚀] 自动执行解密测试...");
        setTimeout(() => {
            testHeraclesDecryption();
        }, 2000); // 延迟2秒执行

    });
}, 3000); // 整体延迟3秒执行
