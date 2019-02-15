# User Guide

### Loading a File

### Running From a Script

```python
import numpy as np
import xarray as xr
from datasetviewer.dataset.Variable import Variable
from datasetviewer import plot
from collections import OrderedDict as DataSet

ds = DataSet()
ds["threedims"] = Variable("threedims", xr.DataArray(np.random.rand(3, 4, 5), dims=['x', 'y', 'z']))
ds["onedim"] = Variable("onedim", xr.DataArray(np.random.rand(3), dims=['b']))
ds["twodims"] = Variable("twodims", xr.DataArray(np.random.rand(3, 8), dims=['g', 'h']))
ds["fourdims"] = Variable("fourdims", xr.DataArray(np.random.rand(3, 4, 5, 6), dims=['c', 'd', 'e', 'f']))

plot(ds)
```

```python
import xarray as xr
import numpy as np
from datasetviewer import plot

ds = xr.Dataset({'foo': np.arange(10), 'bar': ('x', [1, 2])})

plot(ds)
```