__version__ = "0.3.2"


from .io import get_data, get_target_lightcurve, get_target_spectra, get_spec_datafile

# internal shortcut
_SPEC_DATAFILE = get_spec_datafile()
