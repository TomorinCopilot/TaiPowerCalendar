# 台電時間電價日曆資料

以年度取得時間電價日別資料的靜態 JSON 服務。此為獨立整理專案，非台灣電力公司官方服務。

> 2026 與 2027 的來源是第三方 CSV，目前尚未逐日比對台電官方 PDF。資料的格式及日期完整性已檢查，日別正確性尚待核對；計費使用前請確認台電公告。

## 資料網址

發布後的預計網址（以實際部署為準）：

```text
https://tomorincopilot.github.io/TaiPowerCalendar/data/{year}.json
https://tomorincopilot.github.io/TaiPowerCalendar/data/years.json
```

例如將 `{year}` 換成 `2026`。未提供的年份回傳 HTTP 404。`years.json` 是可用年份的陣列。全年 JSON 是依日期排序的陣列：

```json
[
  {"date": "2026-01-01", "day_type": "sunday_holiday"},
  {"date": "2026-01-02", "day_type": "weekday"}
]
```

以上為格式示例。`weekday` 表示平日，`saturday` 表示週六日別，`sunday_holiday` 表示週日或離峰日；定義沿用來源資料。日別並非每個時段的費率，實際計費仍須依適用方案、電壓、季節及台電公告。

## 更新資料

1. 在 `source/` 增加或修正以西元年命名的 CSV，欄位為 `date,day_type`。
2. 根據台電公告逐日核對並記錄核對情況。
3. 執行 `python3 scripts/build.py`，更新 `docs/data/`。
4. 提交變更。GitHub Actions 會驗證 CSV，重新產生 JSON 並部署 Pages。請在 Settings → Pages → Build and deployment 的 Source 選擇 GitHub Actions。

檢查涵蓋欄位、日別、日期格式、順序與全年日期完整性；不能判斷日別是否符合官方資料。若移除年度，亦應刪除 `docs/data/` 中對應的舊 JSON，避免保留過期檔案。

## 來源與授權

- 年度 CSV：使用者提供，來源為 [JUN-WEI-DING/taipower-tou](https://github.com/JUN-WEI-DING/taipower-tou)。上游專案使用 MIT 授權，原始授權與著作權聲明見 `THIRD_PARTY_LICENSE.txt`。
- 官方參考：[台電最近兩年時間電價日曆表](https://www.taipower.com.tw/media/c4al2pqn/%E6%9C%80%E8%BF%91%E5%85%A9%E5%B9%B4%E6%99%82%E9%96%93%E9%9B%BB%E5%83%B9%E6%97%A5%E6%9B%86%E8%A1%A8.pdf?mediaDL=true)。官方連結內容可能隨時間更新，應記錄實際核對的版本。
