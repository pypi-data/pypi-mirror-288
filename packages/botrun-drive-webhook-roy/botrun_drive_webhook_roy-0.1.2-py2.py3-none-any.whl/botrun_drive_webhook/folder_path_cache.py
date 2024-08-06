# =============================================
# FolderTree Class 用於管理和操作目錄樹結構，目錄資訊儲存於 CSV 文件中。
# 所有文件檔案操作均在 data 子資料夾中進行，以保持數據文件整潔。以下是 FolderTree 的主要功能：
# 初始化 (__init__): 初始化時設定目錄樹的名字和資料存放路徑，若指定的 CSV 文件存在，將自動讀取現有數據。
# 新增分支 (add_branch): 新增一個目錄分支到目錄樹中。如果添加的新分支與現有分支存在重疊，會自動更新現有分支。
# 搜尋目錄 (search):根據目錄名稱查找目錄樹中的特定路徑。提供 reload 選項以控制是否從文件重新讀取數據，以確保資料最新。
# 備份 (backup):將當前目錄樹數據備份到帶有時間戳的 CSV 文件中，便於還原和追溯。
# 重置 (reset):先備份現有數據，然後清空目錄樹並刪除 CSV 文件。
# =============================================
import json
import os
from datetime import datetime
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

class FolderTree:
    def __init__(self, folder_tree_name):
        self.folder_tree_name = folder_tree_name
        self.data = pd.DataFrame(columns=["path"])
        self.data_dir = "data"
        self.csv_file_path = os.path.join(self.data_dir, f"{self.folder_tree_name}.csv")
        
        # 確保資料夾存在
        os.makedirs(self.data_dir, exist_ok=True)

        # 嘗試從CSV檔案載入現有資料
        try:
            self.load_from_csv(self.csv_file_path)
        except FileNotFoundError:
            pass  # 文件不存在，表示新建一個空的資料結構

    def add_branch(self, branch_list):
        new_path = branch_list
        update_required = False
        
        # 檢查是否存在包含或等於新路徑的分支
        for i, row in self.data.iterrows():
            existing_path = row["path"]
            
            # 如果現有路徑包含新路徑或等於新路徑，不需要新增
            if new_path == existing_path or all(item in existing_path for item in new_path):
                return
            
            # 如果新路徑包含現有路徑，標記為需要更新且刪除該行
            if all(item in new_path for item in existing_path):
                update_required = True
                self.data.drop(i, inplace=True)
                
        if update_required:
            # 當有更新需求時，把所有符合條件的路徑刪除後加上一條新的路徑
            new_row = pd.DataFrame({"path": [new_path]})
            self.data = pd.concat([self.data, new_row], ignore_index=True)
        else:
            # 如果沒有更新需求且不包含已存在的路徑，則新增一行
            new_row = pd.DataFrame({"path": [new_path]})
            self.data = pd.concat([self.data, new_row], ignore_index=True)
        
        # 新增或更新後儲存資料
        self.to_csv(self.csv_file_path)
    
    def search(self, folder_name, reload=False):
        # 如 reload 參數為 True，則重新讀取CSV檔案
        if reload:
            self.load_from_csv(self.csv_file_path)
        
        # 檢查DataFrame所有行的path，如果找到folder_name則回傳從根節點到該節點之間的路徑
        for i, row in self.data.iterrows():
            path = row["path"]
            if folder_name in path:
                index = path.index(folder_name)
                return path[:index + 1]
        return None

    def to_csv(self, file_path):
        # 確保在寫入CSV時將路徑轉換為JSON字串形式
        temp_data = self.data.copy()
        if not temp_data.empty:
            temp_data['path'] = temp_data['path'].apply(json.dumps)
        temp_data.to_csv(file_path, index=False)

    def load_from_csv(self, file_path):
        try:
            self.data = pd.read_csv(file_path)
            # 確保path還是保持列表格式而不是字串
            self.data["path"] = self.data["path"].apply(json.loads)
        except pd.errors.EmptyDataError:
            # 如果文件是空的，建立一個空的 DataFrame
            self.data = pd.DataFrame(columns=["path"])

    def del_branch(self, node_name):
        print(f"Attempting to delete branches containing node: {node_name}")

        # 使用布爾索引來標記需要保留的行
        mask = self.data['path'].apply(lambda path: node_name not in path)
        
        # 計算要刪除的行數
        rows_to_delete = (~mask).sum()
        print(f"delete {self.folder_tree_name} {rows_to_delete} rows")

        # 更新 DataFrame，只保留不包含指定節點的路徑
        self.data = self.data[mask]

        # 如果 DataFrame 為空，創建一個只有列名的空 DataFrame
        if self.data.empty:
            self.data = pd.DataFrame(columns=["path"])

    def backup(self):
        """ 備份 CSV 檔案，檔案名稱接上日期時間 """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M")
        backup_file = os.path.join(self.data_dir, f"{self.folder_tree_name}-{timestamp}.csv")
        self.to_csv(backup_file)
        print(f"Backup created: {backup_file}")

    def reset(self):
        """ 先備份 CSV 檔案後刪除清空 self.data """
        self.backup()
        self.data = pd.DataFrame(columns=["path"])
        if os.path.exists(self.csv_file_path):
            os.remove(self.csv_file_path)
        print("Folder tree data cleared and CSV file removed.")