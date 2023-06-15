Please visit dataset [homepage](https://www.mvtec.com/company/research/datasets/mvtec-ad) to download the data. 

Afterward, you have the option to download it in the universal supervisely format by utilizing the *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='MVTEC AD', dst_path='~/dtools/datasets/MVTEC AD.tar')
```
