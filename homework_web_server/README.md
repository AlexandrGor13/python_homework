### HTTP сервер

#### Архитектура веб-сервера
http_threading.py
Вариант с использованием многопоточности 

httpd_async.py
Вариант с использованием асинхронности

#### Нагрузочное тестирование
http_threading.py

```
wrk -t12 -c400 -d30s http://localhost:8080/index.html

Running 30s test @ http://localhost:8080/index.html
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     8.68ms   65.21ms   1.67s    98.36%
    Req/Sec   393.26    309.00     1.89k    65.03%
  90656 requests in 30.65s, 23.17MB read
  Socket errors: connect 0, read 0, write 0, timeout 42
Requests/sec:   2957.68
Transfer/sec:    774.08KB
```
httpd_async.py
```
wrk -t12 -c400 -d30s http://localhost:8080/index.html


Running 30s test @ http://localhost:8080/index.html
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   172.15ms   23.71ms 540.38ms   79.63%
    Req/Sec   184.42     58.83   333.00     68.30%
  66083 requests in 30.02s, 16.89MB read
Requests/sec:   2201.21
Transfer/sec:    576.10KB

```

#### Веб-сервер умеет:
• Отвечать 200, 403 или 404 на GET-запросы и HEAD-запросы

• Отвечать 405 на прочие запросы

• Возвращать файлы по произвольному пути в DOCUMENT_ROOT.

• Вызов /file.html должен возвращать содердимое DOCUMENT_ROOT/file.html

• DOCUMENT_ROOT задается аргументом командной строки -r

• Возвращать index.html как индекс директории

• Вызов /directory/ должен возвращать DOCUMENT_ROOT/directory/index.html

• Отвечать следующими заголовками для успешных GET-запросов: Date, Server, Content-Length, Content-Type, Connection

• Корректный Content-Type для: .html, .css, .js, .jpg, .jpeg, .png, .gif, .swf

• Понимать пробелы и %XX в именах файлов