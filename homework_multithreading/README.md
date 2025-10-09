### MemcLoad

В проекте переделана однопоточная версия memc_load.py в более производительный вариант. 
Сам скрипт парсит и заливает в мемкеш поминутную выгрузку логов трекера установленных приложений. 
Ключом является тип и идентификатор устройства через двоеточие, значением является protobuf сообщение.

Ссылки на tsv.gz файлы:
* https://cloud.mail.ru/public/KxgQ/UjzmvrKzN
* https://cloud.mail.ru/public/2Gby/6RtFfLyKD

Пример запуска однопоточной версии
```
/home/alexandr/PycharmProjects/python_homework/homework/.venv/bin/python /home/alexandr/PycharmProjects/python_homework/homework/homework_multithreading/memc_load.py 
[2025.10.08 21:28:17] I Memc loader started with options: {'test': False, 'log': None, 'dry': False, 'pattern': '*.tsv.gz', 'idfa': '127.0.0.1:33013', 'gaid': '127.0.0.1:33014', 'adid': '127.0.0.1:33015', 'dvid': '127.0.0.1:33016'}
[2025.10.08 21:28:17] I Processing 20170929000000.tsv.gz
[2025.10.08 22:44:13] I Acceptable error rate (0.0). Successfull load

Process finished with exit code 0

```

Пример запуска многопоточной версии
```
/home/alexandr/PycharmProjects/python_homework/homework/.venv/bin/python /home/alexandr/PycharmProjects/python_homework/homework/homework_multithreading/memc_load_multithreading.py 
[2025.10.08 21:00:58] I Memc loader started with options: {'test': False, 'log': None, 'dry': False, 'pattern': '*.tsv.gz', 'idfa': '127.0.0.1:33013', 'gaid': '127.0.0.1:33014', 'adid': '127.0.0.1:33015', 'dvid': '127.0.0.1:33016'}
[2025.10.08 21:00:58] I Processing 20170929000000.tsv.gz
[2025.10.08 21:24:42] I Acceptable error rate (0.0). Successfull load

Process finished with exit code 0
```
