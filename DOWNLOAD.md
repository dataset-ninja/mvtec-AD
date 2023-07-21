Dataset **MVTec AD** can be downloaded in Supervisely format:

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/4/4/5b/hsCrjVjBTuhVBBzqCnmU5WDR2qmHy8FEa4JjoX8WKrt3AFyshcuOCuWFJ8q3xHqcUsHYKd71tDXEA0NgNu61dbeYxukTyLdB5nXaGumrOpIIWqmSdikNdhuWqnbh.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='MVTec AD', dst_path='~/dtools/datasets/MVTec AD.tar')
```
The data in original format can be 🔗[downloaded here](https://www.mvtec.com/company/research/datasets/mvtec-ad)