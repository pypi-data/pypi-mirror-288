


import os
import numpy as np
import pandas

def get_ztfcosmodir(directory=None):
    """ simple function to access the directory where the data is """
    if directory is not None:
        return directory
    
    directory = os.getenv("ZTFCOSMODIR", None)
    if directory is None:
        directory = input('Please specify the directory where data are (or where to download them):')
        if os.path.isdir( os.path.dirname( directory ) ):
            raise IOError(f"No such directory: {os.path.dirname( directory )} ")
            
        os.environ['ZTFCOSMODIR'] = directory
    
    return directory

# ============= #
#   Tables      #
# ============= #
def get_data(good_coverage=None, good_lcfit=None, redshift_range=None,
             saltmodel="salt2-T21", band="gri", phase_range=[-10,40]):
    """ """
    sndata = get_sn_data()
    globalhost = get_globalhost_data()
    localhost = get_localhost_data()

    # merging naming convention
    param_keys = ["mass", "mass_err", "restframe_gz", "restframe_gz_err"]
    globalhost = globalhost.rename({f"{k}":f"global{k}" for k in param_keys}, axis=1)
    localhost = localhost.rename({f"{k}":f"local{k}" for k in param_keys}, axis=1)

    # out dataframe
    joined_df = sndata.join( globalhost.join(localhost) )

    #
    # some additional Selections
    # 
    if good_coverage is not None:
        if good_coverage:
            joined_df = joined_df[joined_df["lccoverage_flag"].astype(bool)]
        else:
            joined_df = joined_df[~joined_df["lccoverage_flag"].astype(bool)]


    if good_lcfit is not None:
        if good_lcfit:
            joined_df = joined_df[joined_df["fitquality_flag"].astype(bool)]
        else: # lcquality_flag
            joined_df = joined_df[~joined_df["fitquality_flag"].astype(bool)]

    if redshift_range is not None:
        joined_df = joined_df[joined_df["redshift"].between(*redshift_range)]

    return joined_df

def get_sn_data(saltmodel="salt2-T21", band="gri", phase_range=[-10,40]):
    """ """
    ztfcosmodir = get_ztfcosmodir()
    # default
    if saltmodel=="salt2-T21" and band=="gri" and phase_range==[-10,40]:
        fullpath = os.path.join(ztfcosmodir, "tables", "snia_data.csv")
        
    else:
        phase = f"phase{phase_range[0]:d}to{phase_range[1]:d}"
        naming_convention = f"snia_data_{phase}_{band}_{saltmodel}.csv"
        fullpath = os.path.join(ztfcosmodir, "tables", "extra", naming_convention)
        if not os.path.isfile(fullpath):
            raise ValueError(f"unknown data file phase: {phase}, band: {band}, model: {saltmodel} (file: {naming_convention})")
        
    return pandas.read_csv(fullpath, index_col=0)

def get_globalhost_data():
    """ """
    ztfcosmodir = get_ztfcosmodir()
    fullpath = os.path.join(ztfcosmodir, "tables", "globalhost_data.csv")
    return pandas.read_csv(fullpath, index_col=0)

def get_localhost_data():
    """ """
    ztfcosmodir = get_ztfcosmodir()
    fullpath = os.path.join(ztfcosmodir, "tables", "localhost_data.csv")
    return pandas.read_csv(fullpath, index_col=0)


# ============= #
#   Spectra     #
# ============= #
def get_target_spectra(name, as_data=True):
    """ """
    from . import _SPEC_DATAFILE
    from . import spectrum
    fullpath = _SPEC_DATAFILE[_SPEC_DATAFILE["ztfname"]==name]["fullpath"].values
    
    # single spectrum case
    if len(fullpath)==1:
        file_ = fullpath[0]
        if as_data:
            return spectrum.read_spectrum(file_)
        return spectrum.Spectrum.from_filename(file_)
    else: # multiple spectra case
        if as_data:
            return [spectrum.read_spectrum(file_) for file_ in fullpath]
        return [spectrum.Spectrum.from_filename(file_) for file_ in fullpath]
    

def parse_spec_filename(filename):
    """ file or list of files.
    
    Returns
    -------
    - Serie if single file
    - DataFrame otherwise
    """
    index = ["ztfname", "date", "telescope", "version"]
    fdata = []
    for file_ in np.atleast_1d(filename):
        file_ = os.path.basename(file_).split(".ascii")[0]
        name, date, *telescope, origin = file_.split("_")    
        telescope = "_".join(telescope)
        fdata.append([name, date, telescope, origin])

    if len(fdata) == 1:
        return pandas.Series(fdata[0], index=index)
    
    return pandas.DataFrame(fdata, columns=index)

def get_spec_datafile():
    """ """
    from glob import glob
    from astropy.time import Time
    
    ztfcosmodir = get_ztfcosmodir()
    specfiles = glob( os.path.join(ztfcosmodir, "spectra", "*.ascii"))
    datafile = pandas.DataFrame(specfiles, columns=["fullpath"])
    datafile["basename"] = datafile["fullpath"].str.split(pat="/", expand=True).iloc[:, -1]
    
    specfile = pandas.concat([datafile, parse_spec_filename(datafile["basename"])], axis=1)
    
    data = get_sn_data()
    specfile["dateiso"] = Time(np.asarray(specfile["date"].apply(lambda x: f"{x[:4]}-{x[4:6]}-{x[6:]}"), dtype=str), format="iso").mjd
    specfile = specfile.join(data[["t0", "redshift"]], on="ztfname")
    specfile["phase_obs"] = (specfile.pop("dateiso")-specfile.pop("t0"))
    specfile["phase"] = specfile["phase_obs"]/(1+specfile.pop("redshift"))
        
    return specfile

# ============= #
#  LightCurves  #
# ============= #
def get_target_lightcurve(name, as_data=True,
                          saltmodel="salt2-T21",
                          band="gri",
                          phase_range=[-10,40]):
    """ get the dataframe of a target's lightcurve """
    if as_data:
        ztfcosmodir = get_ztfcosmodir()
        fullpath = os.path.join(ztfcosmodir, "lightcurves", f"{name}_lc.csv")
        return pandas.read_csv(fullpath,  delim_whitespace=True, comment='#')

    from .lightcurve import LightCurve
    saltparam = get_sn_data(saltmodel=saltmodel, band=band, phase_range=phase_range).loc[name]
    return LightCurve.from_name(name,
                                saltmodel=saltmodel,
                                saltparam=saltparam,
                                phase_range=phase_range)


# ============= #
#   Download    #
# ============= #
def get_phase_coverage():
    """ """
    ztfcosmodir = get_ztfcosmodir()
    filepath = os.path.join(ztfcosmodir, "tables", "phase_coverage.parquet")
    return pandas.read_parquet( filepath )
    
def download_release(which="dr2", directory=None):
    """ download the ZTF Cosmo release.

    Parameters
    ----------
    which: str
        release id:
        - dr2
        - dr2.5 [not available yet]
        - dr3 [not available yet]

    directory: path
        which should the data be downloaded.

    Returns
    -------
    None
    """
    if which not in ["dr2"]:#, "dr2.5", "dr3"]:
        raise ValueError(f'Only "dr2" implemented, {which} given')
        
    directory  = get_ztfcosmodir(directory)
    this_directory = os.path.join(directory, which)

    
    
