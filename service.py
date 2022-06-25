from nameko.rpc import rpc
from dependencies.database import DatabaseProvider


class CloudStorageService:
    name = 'cloud_storage_service'
    database = DatabaseProvider()

    @rpc
    def upload_files(self, arr_filename):
        upload_files = self.database.upload_files(arr_filename)
        return upload_files
    
    
    @rpc
    def download_files(self, file_id):
        download_files = self.database.download_files(file_id)
        return download_files
    
    
    @rpc
    def get_all_files(self):
        get_all_files = self.database.get_all_files()
        return get_all_files
