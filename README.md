![ezgif com-video-to-gif](https://user-images.githubusercontent.com/85805215/233844237-4a35b91b-fac2-47c1-8f6a-a226cf75144f.gif)

Сервис позволяет искать поставщиков в автоматичеком режиме. На вход подается файл с товарной номенклатурой, далее последовательно запускаются четыре Scrapy проекта. Сначала собирается информация с поисковой выдачи в Яндексе и с сайтов компаний, затем по доменам из выдачи получаем ИНН организаций из Координационного центра доменов (ccTLD, имеют для этого удобный API), после этого обогащаем данные с помощью портала о контрагентах и выводим все в виде дашборда для аналитики. Реализованы сортировка по столбцам, фильтрация, поиск.
