
## polars_partitions

[![PyPI - Version](https://img.shields.io/pypi/v/polars_partitions?style=flat-square&logo=PyPI&logoColor=white)](https://pypi.org/project/polars-partitions/)


### Python
```
pip install polars_partitions
```

## Description


This library is not a replacement for [Polars](https://pola.rs/).
The main goal is to improve the work (write/read/filter) with partitions by creating a Table Of Contents file (hereinafter referred to as "TOC").

### Write Partition
**polars_parquet.write_data(**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; _df_: DataFrame,  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; _columns_: array | string  
**)**

#### Parameters
**df**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Polars DataFrame  
**columns**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Array of columns on which to create partitions  

<details>
    <summary>Example 🤔🤔🤔</summary>

``` python
from polars_partitions import easy as pp
from datetime import date
import polars as pl

# Create a test dataset
df = pl.DataFrame({'col1':[date(2024,1,1),date(2024,1,1),date(2024,1,2),date(2024,1,2),date(2024,1,2),date(2024,1,3),date(2024,1,3),date(2024,1,3)],
              'col2':['A2','A2','A2','A2','B2','B2','B2','B2'],
              'col3':[1,2,3,4,5,6,7,8]
              })

path = './your_path'

# Which columns are partitioned by
columns = ['col1', 'col2'] 

ep = pp.EasyPartition(path)

# Write the partitions
ep.write_data(df, columns)

# Output: 
# ./your_path/toc.parquet - done! 

```
</details>

### Write TOC
**polars_parquet.write_toc(**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; _df_: DataFrame on which the partitions are based,  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; _columns_: array | string  
**)**

#### Parameters
**df**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Dictionary, where the key is the column and the array is the values  
**columns**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Array of columns to create partitions for  

### Reading TOC
**polars_parquet.get_toc(**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; _filters_: dict = None,  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; _between_: str = None  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; _structure_: bool = False  
**)**

#### Parameters
**filters**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Dictionary, where the key is the column and the array is the values  
**between**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Works in conjunction with **filters**. It takes as input the **column name** on which to apply the **between** filter. It takes the first two values from the filters(array).  
**structure**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Передав значение True печатает структуру словаря, так как партиции вложены друг в друга.

<details>
    <summary>Example 🤔🤔🤔</summary>

``` python
ep.get_toc(structure=True)

# Output: 
col1
 ↳col2

shape: (4, 2)
┌────────────┬──────┐
│ col1       ┆ col2 │
│ ---        ┆ ---  │
│ date       ┆ str  │
╞════════════╪══════╡
│ 2024-01-02 ┆ A2   │
│ 2024-01-02 ┆ B2   │
│ 2024-01-01 ┆ A2   │
│ 2024-01-03 ┆ B2   │
└────────────┴──────┘
```

</details>

### Read Partition
**polars_parquet.get_data(**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; _columns_: array | string = "*",  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; _filters_: dict = None,  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; _btwn_: str = None  
**)** → LazyFrame  

#### Parameters
**columns**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Array of columns to return  
**filters**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Dictionary where the key is the column and the array is the values  
**btwn**  
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Works in conjunction with **filters**. It takes as input the **column name** on which to apply the **between** filter. It takes the first two values from the filters(array).  

<details>
    <summary>Example 🤔🤔🤔</summary>

``` python
filters = {'col1':[date(2024,1,1),date(2024,1,3)]}

with pl.StringCache():
    df = ep.get_data(filters=filters, between='col1', columns=['col1', 'col3']).collect()

df

# Output: 
shape: (8, 2)
┌────────────┬──────┐
│ col1       ┆ col3 │
│ ---        ┆ ---  │
│ str        ┆ i64  │
╞════════════╪══════╡
│ 2024-01-02 ┆ 3    │
│ 2024-01-02 ┆ 4    │
│ 2024-01-02 ┆ 5    │
│ 2024-01-01 ┆ 1    │
│ 2024-01-01 ┆ 2    │
│ 2024-01-03 ┆ 6    │
│ 2024-01-03 ┆ 7    │
│ 2024-01-03 ┆ 8    │
└────────────┴──────┘
```
</details>
