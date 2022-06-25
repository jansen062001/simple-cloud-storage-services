# Simple Cloud Storage
Simple Cloud Storage adalah sebuah service yang digunakan untuk mengupload dan download file yang ada pada service,

## Request: Upload file
![POST](https://badgen.net/badge/Method/POST/yellow)**/api/files**
```
Body (form-data)
    file: /D:/xxx/example.jpg
```


### Responses:
#### Upload file
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "status": "success",
    "message": "File upload successful"
}
```
#### Upload file (No file part)
![Bad%20Request](https://badgen.net/badge/Bad%20Request/400/red)
```json
{
    "status": "error",
    "message": "No file part"
}
```
#### Upload file (No selected file)
![Bad%20Request](https://badgen.net/badge/Bad%20Request/400/red)
```json
{
    "status": "error",
    "message": "No selected file"
}
```
#### Upload file (Unsupported Media Type)
![Unsupported%20Media%20Type](https://badgen.net/badge/Unsupported%20Media%20Type/415/red)
```json
{
    "status": "error",
    "message": "Unsupported Media Type"
}
```

## Request: Download file
![GET](https://badgen.net/badge/Method/GET/green)**/api/files/`<int:file_id>`**


### Responses:
#### Download file
![OK](https://badgen.net/badge/OK/200/green)
```
Headers(5)
    Content-Type: image/jpeg
    Content-Length: 30816
    Content-Disposition: attachment; filename=0_15.jpg
    Date: Sat, 25 Jun 2022 17:17:33 GMT
    Connection: keep-alive
```
#### Download file (File not found)
![Not Found](https://badgen.net/badge/Not%20Found/404/red)
```json
{
    "status": "error",
    "message": "File not found"
}
```

## Request: Get all files
![GET](https://badgen.net/badge/Method/GET/green)**/api/files**


### Responses:
#### Get all files
![OK](https://badgen.net/badge/OK/200/green)
```json
{
    "status": "success",
    "data": [
        {
            "id": 1,
            "filename": "0_15.jpg"
        }
    ]
}
```