# polars_parquet

## Описание ##
Этот код не является заменой для библиотеки [Polars](https://pola.rs/).
Основная задача это улучшить работу (запись/чтением/фильтрация) с партициями путем создания файла Содержания (далее по тексту "TOC" - Table Of Contents).

## Запись партиции
### polars_parquet.wr_partition() 
**polars_parquet.wr_partition(**  
&nbsp; &nbsp; &nbsp; &nbsp; _df_: DataFrame,  
&nbsp; &nbsp; &nbsp; &nbsp; _columns_: array | string,  
&nbsp; &nbsp; &nbsp; &nbsp; _output_path_: str  
**)**

#### Параметры
**df**  
&nbsp; &nbsp; &nbsp; &nbsp; Polars DataFrame  
**columns**  
&nbsp; &nbsp; &nbsp; &nbsp; Массив колонок, по которым нужно создать партиции  
**output_path**  
&nbsp; &nbsp; &nbsp; &nbsp; Путь куда нужно сохранить  

## Запись TOC
### polars_parquet.wr_toc() 
**polars_parquet.wr_toc(**  
&nbsp; &nbsp; &nbsp; &nbsp; _df_: DataFrame на основании которого созданы партиции,  
&nbsp; &nbsp; &nbsp; &nbsp; _columns_: array | string,  
&nbsp; &nbsp; &nbsp; &nbsp; _output_path_: str  
**)**

#### Параметры
**df**  
&nbsp; &nbsp; &nbsp; &nbsp; Словарь, где ключ - колонка, а массив это значения  
**columns**  
&nbsp; &nbsp; &nbsp; &nbsp; Массив колонок, по которым нужно создать партиции  
**output_path**  
&nbsp; &nbsp; &nbsp; &nbsp; Путь куда нужно сохранить  

## Чтение TOC
### polars_parquet.rd_toc() 
**polars_parquet.rd_toc(**  
&nbsp; &nbsp; &nbsp; &nbsp; _output_path_: DataFrame,  
&nbsp; &nbsp; &nbsp; &nbsp; _filters_: dict = None,  
&nbsp; &nbsp; &nbsp; &nbsp; _btwn_: str = None  
**)**

#### Параметры
**output_path**  
&nbsp; &nbsp; &nbsp; &nbsp; Путь куда нужно сохранить  
**filters**  
&nbsp; &nbsp; &nbsp; &nbsp; Словарь, где ключ - колонка, а массив это значения  
**btwn**  
&nbsp; &nbsp; &nbsp; &nbsp; Работает в связке с **filters**. Принимает на вход **название столбца** по которому применить фильтр **between**. Из filters(массива) берет первые два значения.  

## Чтение партиции
### polars_parquet.rd_partition() 
**polars_parquet.rd_partition(**  
&nbsp; &nbsp; &nbsp; &nbsp; _output_path_: str,  
&nbsp; &nbsp; &nbsp; &nbsp; _columns_: array | string = "*",  
&nbsp; &nbsp; &nbsp; &nbsp; _filters_: dict = None,  
&nbsp; &nbsp; &nbsp; &nbsp; _btwn_: str = None  
**)** → LazyFrame  

#### Параметры
**output_path**  
&nbsp; &nbsp; &nbsp; &nbsp; Путь к файлу parquet или к папке с партициями  
**columns**  
&nbsp; &nbsp; &nbsp; &nbsp; Массив колонок, которые нужно вернуть  
**filters**  
&nbsp; &nbsp; &nbsp; &nbsp; Словарь, где ключ - колонка, а массив это значения  
**btwn**  
&nbsp; &nbsp; &nbsp; &nbsp; Работает в связке с **filters**. Принимает на вход **название столбца** по которому применить фильтр **between**. Из filters(массива) берет первые два значения.  

## Как использовать (пример)
``` python
from pl_partitions import polars_partition
from datetime import date
import polars as pl

# Создадим тестовый датасет
df = pl.DataFrame({'col1':[date(2024,1,1),date(2024,1,1),date(2024,1,2),date(2024,1,2),date(2024,1,2),date(2024,1,3),date(2024,1,3),date(2024,1,3)],
              'col2':['A2','A2','A2','A2','B2','B2','B2','B2'],
              'col3':[1,2,3,4,5,6,7,8]
              })

output_path = 'ваш_путь/имя_папки_куда_сохранить'
# По каким столбцам делаем партции
columns = ['col1', 'col2'] 

pp = polars_partitions()

# Записать партиции
# pp.wr_partition(df, columns, output_path)

# Прочитать TOC
# print(pp.rd_toc(output_path))

# Чтение партиций и применение фильтров
# filters = {'col1':[date(2024,1,1),date(2024,1,3)]}
# df = pp.rd_partition(output_path, filters=filters, btwn='col1', columns=['col1', 'col3']) 
# print(df.collect())

```

