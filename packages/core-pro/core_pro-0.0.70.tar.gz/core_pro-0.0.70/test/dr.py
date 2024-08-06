from src.core_pro import Drive
from pathlib import Path
import polars as pl


# id = '16CafO9K9uiCCx48rK3g9fCOV7QCv59Vw'
# lst_file = [*Path('/media/kevin/75b198db-809a-4bd2-a97c-e52daa6b3a2d/category_tag/raw').glob('*.parquet')]
# Drive(debug=True).upload_batches(lst_file=lst_file, folder_id=id)

drive_id = '1cHcXr31pxa5XSkhpjrHCAv8E3R79QAZ7'
lst = Drive().search_files(drive_id)
all_files = (
    pl.DataFrame(lst)
    .with_columns(
        pl.col(i).str.strptime(pl.Datetime, strict=False)
        for i in ['createdTime', 'modifiedTime']
    )
    .sort(['name', 'createdTime'], descending=True)
    .with_columns(
        pl.col('createdTime').rank(method='max', descending=True).over('name').alias('rank')
    )
    .to_dicts()
)
for f in all_files:
    if f['rank'] != 1:
        Drive().remove_file(f['id'])
