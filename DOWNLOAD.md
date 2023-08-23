Dataset **MVTec AD** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/4/T/iN/PTvi1vS1Qjku8VHd3PDsTPo06isfmzSDEhmyiypWrQsHnUmmGxMlXxNUAgKIy5tnbQqRbtDRcW02NdAIPQcCOiaCFyb9y90lBJl9uJtEz0a2mKqj5hmbU6gLEk3z.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='MVTec AD', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.mvtec.com/company/research/datasets/mvtec-ad).