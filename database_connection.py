from supabase import create_client, Client
import json
from typing import Optional
import threading

_supabase_instance: Optional['DatabaseConnection'] = None
_instance_lock = threading.Lock()

def get_supabase_client() -> 'DatabaseConnection':
    global _supabase_instance
    if _supabase_instance is None:
        with _instance_lock:
            # Double-check locking pattern for thread safety
            if _supabase_instance is None:
                _supabase_instance = DatabaseConnection()
    return _supabase_instance

def get_db_client():
    # 使用全局实例或工厂函数创建实例
    return get_supabase_client()

class DatabaseConnection:

    supabase_url = "https://eeuwpcynygzohstndlxf.supabase.co"
    supabase_key = "sb_secret_C-HpaYbH0gGYtivfb6j_1A_hkdWVKVy"
    table_name = "news"

    def __init__(self,):
        self.supabase = create_client(self.supabase_url, self.supabase_key)

    def create_supabase_client(self) -> Client:
        return create_client(self.supabase_url, self.supabase_key)

    def insert_data(self, data: dict):
        if self.supabase is None:
            raise RuntimeError("Supabase client not initialized")
        self.supabase.table(self.table_name).insert(data).execute()

    def query_data(self) -> list:
        if self.supabase is None:
            raise RuntimeError("Supabase client not initialized")
        return self.supabase.table(self.table_name).select("*").execute().data

    def query_data_id(self, id:int) -> dict:
        if self.supabase is None:
            raise RuntimeError("Supabase client not initialized")
        return self.supabase.table(self.table_name).select("*").eq("id", id).execute().data

    def update_data_id(self, id: int, data: dict) -> list:
        if self.supabase is None:
            raise RuntimeError("Supabase client not initialized")
        return self.supabase.table(self.table_name).update(data).eq("id", id).execute().data

    def delete_data_id(self, id: int):
        if self.supabase is None:
            raise RuntimeError("Supabase client not initialized")
        self.supabase.table(self.table_name).delete().eq("id", id).execute()

# --- 示例操作 ---

# 1. 插入数据 (INSERT)
# new_record = {"name": "Alice", "email": "alice@example.com"}
# result = supabase.table(table_name).insert(new_record).execute()
# print("插入结果:", result.data)

# 2. 查询数据 (SELECT)
# 例如，查询所有记录
# data = supabase.table(table_name).select("*").execute()
# print("查询到的数据:", data.data)

# 例如，查询特定条件的记录 (假设表有 id 列)
# specific_id = 1
# data = supabase.table(table_name).select("*").eq("id", specific_id).execute()
# print(f"ID为 {specific_id} 的记录:", data.data)

# 3. 更新数据 (UPDATE)
# update_data = {"name": "Alice Updated"}
# record_id_to_update = 1
# result = supabase.table(table_name).update(update_data).eq("id", record_id_to_update).execute()
# print("更新结果:", result.data)

# 4. 删除数据 (DELETE)
# record_id_to_delete = 999 # 一个假设的ID
# result = supabase.table(table_name).delete().eq("id", record_id_to_delete).execute()
# print("删除结果:", result.data)