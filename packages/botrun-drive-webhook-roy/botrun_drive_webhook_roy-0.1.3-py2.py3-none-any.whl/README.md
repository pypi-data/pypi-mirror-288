# Botrun Drive Webhook

這個專案提供了一個從 Google Drive 資料夾監控哪些修改檔案，並可以呼叫 callback function 去處理更新的工具。以下是如何使用這個工具的說明。

---

## 安裝

請先確保您已經安裝 Python 以及 pip。然後，您可以使用以下指令來安裝這個專案的依賴套件：

```sh
pip install botrun-drive-webhook
```

---

## 使用方法

### 調用 `get_update_queue()` 取得要更新的檔案清單
### 調用 `finish_queue_process()` 回傳檔案更新完畢
