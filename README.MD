# Frequency Analytic

Приложение для анализа текста и получания отчета, включающего в себя частотную статистику слов в этом тексте

# Запуск
Клонирование репозитория
```
bash git clone https://github.com/egorkagod/frequency_statistics.git 
```
Запуск через Docker(убедитесь что установлен и запущен docker engine)
```
bash docker build -t frequency-stat . && docker run -p 8000:8000 frequency-stat
```

# Использование 
Убедитесь что в текущей папке присутствует файл log.txt или же введите свой путь
```
bash curl -o report.xlsx  -F "file=@./log.txt" http://localhost:8000/public/report/export
```