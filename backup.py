import os
import shutil
import datetime
import zipfile

class BackupManager:
    def __init__(self, backup_dir="backups"):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)
        
    def create_backup(self, data_dir):
        """创建备份"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}.zip")
        
        with zipfile.ZipFile(backup_file, 'w') as zipf:
            for root, dirs, files in os.walk(data_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, data_dir)
                    zipf.write(file_path, arcname)
                    
        return backup_file
        
    def restore_backup(self, backup_file, restore_dir):
        """恢复备份"""
        with zipfile.ZipFile(backup_file, 'r') as zipf:
            zipf.extractall(restore_dir) 