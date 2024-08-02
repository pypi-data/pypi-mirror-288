# ztfcosmo
ZTF Cosmo Data Release repo.

Soon be ready for DR2.


# Basic usage

## access data tables

```python
import ztfcosmo
data = ztfcosmo.get_data() # see options
```

## Plot a lightcurve
```python
lc = ztfcosmo.get_target_lightcurve("ZTF18aaqfziz", as_data=False) # see options
fig = lc.show()
```
![](docs/figures/ZTF18aaqfziz_lcfit.png)
