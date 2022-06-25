# from unittest import result
# from urllib import response
from nameko.extensions import DependencyProvider
import mysql.connector
from mysql.connector import Error
import mysql.connector.pooling


class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection
    
    
    def upload_files(self, arr_filename):
        cursor = self.connection.cursor(dictionary=True)
        
        for i in range(len(arr_filename)):
            sql = 'INSERT INTO `files`(`id`, `filename`) VALUES (NULL, %s)'
            cursor.execute(sql, [str(arr_filename[i])])
        
        self.connection.commit()
        cursor.close()
        return {
            'response_code': 200,
            'response_data': {
                "status": "success",
                "message": "File upload successful"
            }
        }
    
    
    def download_files(self, file_id):
        cursor = self.connection.cursor(dictionary=True)
        response = None
        
        sql = 'SELECT COUNT(*) AS x, files.* FROM `files` WHERE id = %s'
        cursor.execute(sql, [int(file_id)])
        result = cursor.fetchone()
        
        if result['x'] <= 0:
            response = {
                'response_code': 404,
                'response_data': {
                    "status": "error",
                    "message": "File not found"
                }
            }
        else:
            response = {
                'response_code': 200,
                'response_data': {
                    "data": {
                        'filename': result['filename']
                    }
                }
            }
        
        cursor.close()
        return response
    
    
    def get_all_files(self):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        
        sql = 'SELECT * FROM `files` WHERE 1'
        cursor.execute(sql, [])
        
        for file in cursor.fetchall():
            result.append({
                'id': file['id'],
                'filename': file['filename']
            })
        
        cursor.close()
        return {
            'response_code': 200,
            'response_data': {
                "status": "success",
                "data": result
            }
        }


class DatabaseProvider(DependencyProvider):

    connection_pool = None

    def setup(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=32,
                pool_reset_session=True,
                host='127.0.0.1',
                database='simple_cloud_storage',
                user='root',
                password=''
            )
        except Error as e:
            print("Error while connecting to MySQL using Connection pool ", e)
    
    
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())
