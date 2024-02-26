import polars as pl
import os


class EasyPartition:
    def __init__(self, path):
        self.path = path
        
    # Create TOC - Table Of Contents
    def write_toc(self, df:pl.DataFrame, columns:list):
        partitions_list = pl.DataFrame(df[columns].unique())

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        partitions_list.write_parquet(f'{self.path}/toc.parquet')
        print(f'{self.path}/toc.parquet - done!')
        
    # Recording partitions or a single parcel
    def write_data(self, df:pl.DataFrame, columns:list):
        df.write_parquet(
            self.path,
            use_pyarrow=True,
            pyarrow_options={"partition_cols": columns}
        )
        self.write_toc(df, columns)
    
    # Read and search TOC
    def get_toc(self, filters:list=None, between:list=None, structure:bool=False) -> pl.DataFrame:
        df_toc = pl.read_parquet(f'{self.path}/toc.parquet')
        
        if structure:
            for i in range(df_toc.width):
                print(df_toc.columns[i] if i==0 else ' '*i+'↳'+df_toc.columns[i])
        
        #If a partition filter has been specified, go through each one and return only those values,
        #that are in the TOC
        if filters is not None and bool(filters):
            for index in range(df_toc.width):  
                column = df_toc.columns[index]
                
                if column in filters:
                    if column == between:
                        df_toc = df_toc.filter(pl.col(column).is_between(filters[column][0],filters[column][1]))
                    else:
                        df_toc = df_toc.filter(pl.col(column).is_in(filters[column]))
        
        return df_toc
        
    # Reading partitions based on TOC
    def get_data(self, columns:list='*', filters:list=None, between:list=None) -> pl.LazyFrame:
        dir_parquet = self.get_toc(filters, between)
    
        if filters is not None and bool(filters):
            try:
                # Leave out the column that you didn't specify in the filter when you called it and put '*'
                for column in list(set(dir_parquet.columns) - set(list(filters.keys()))):
                    dir_parquet = dir_parquet.with_columns(pl.lit('*').alias(column)).unique() 

                # Put a filter on each record using the "field=partition" template
                for column in list(filters.keys()):
                    dir_parquet = dir_parquet.with_columns((column + '=' + pl.col(column)).alias(column))

                # Merge everything and leave only the "path" column
                dir_parquet = dir_parquet.with_columns(
                    pl.concat_str([pl.col(i) for i in dir_parquet.columns],
                                  separator='/',
                                 ).alias('path')).select(pl.col('path'))
                
                # Read all partitions satisfying the conditions
                with pl.StringCache():
                    for index in range(dir_parquet.width):
                        dfs = [pl.scan_parquet(f'{self.path}/{dir}/*').select(pl.col(columns))for dir in dir_parquet['path']]
                    return pl.concat(dfs)
                
            except ValueError:
                return pl.DataFrame()
            
            except Exception:
                raise ValueError(f'Partitions by column {column} - Does not exist')

        else:
            path_partition = '/*'.join(['/*' for _ in range(dir_parquet.width)])
            with pl.StringCache():
                return pl.scan_parquet(f'{self.path}{path_partition}').select(pl.col(columns))
