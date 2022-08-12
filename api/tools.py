import requests

def ipfs_upload(file):
    url = 'https://api.web3.storage/upload'
    files = {'file': file}
    print("Uploading file to web3 storage...")
    response = requests.post(url, files=files, headers={
                             "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkaWQ6ZXRocjoweGQyRjVFZkI5QmZFOThhOGQ4YkQ0NzVmMTg4OTU5N2YxQ2M2QzBiMkIiLCJpc3MiOiJ3ZWIzLXN0b3JhZ2UiLCJpYXQiOjE2NjAxMjI0NjQ4OTQsIm5hbWUiOiJ3ZWIzY2x1YiJ9.201PcBlvpXulkXzoeHiZxbb2v5ir3zZOXZGM1Omr8mw"})
    print("File uploaded to web3 storage. Recieved response: ", response)    
    cid = response.json()['cid']
    file_url = "http://ipfs.io/ipfs/" + cid
    print(file_url)
    return file_url