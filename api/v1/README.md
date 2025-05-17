# MtG_game_log/api/

Contains API stuff.

### Usage examples

`base URL: http://127.0.0.1:5000/api/v1`

Get: get database entry
```
curl -X GET [URL]
```

Post: create new database entry
```
curl -X POST [URL] /
  -H "Content-Type: application/json" /
  -d '{"key1":"value1","key2":"value2"}'
```

Put: update an existing database entry
```
curl -X PUT [URL] /
  -H "Content-Type: application/json" /
  -d '{"key1":"value1","key2":"value2"}'
```

Delete: deletes a database entry
```
curl -X DELTE [URL]
```
