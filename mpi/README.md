Код в hw_main.cpp честно запускает всё, что попросили в условии, и выводит результаты.

Код в solo.cpp - тот код, который запускался при замерах для одного процесса: run_sbatch_solo.sh 
т е он тоже запускался в slurm и это кажется более правильным, чтобы машина была как минимум схожей с той, на который запускали много процессов.

Код в multi.cpp - то, что запускалось как много процессов в slurm с помощью run_sbatch_multi.sh - да, мне пришлось менять число процессов вручную.

В обоих случаях я не стала выводить результат подсчёта интеграла - точность можно понять, запустив hw_main.cpp, а на время работы часто влияют лишние выводы.

В файле input.txt всегда лежало просто число N: 1000, 1000000 или 100000000

Результаты я оформляла в jupyter notebook и можно посмотреть и запустить: Graphics.ipynb
Поскольку просили график в других форматах, я сделала Graphics.pdf - это просто выгруженный в формате pdf notebook
