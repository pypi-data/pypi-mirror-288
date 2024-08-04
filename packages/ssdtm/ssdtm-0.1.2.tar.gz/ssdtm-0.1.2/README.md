# Synthetic SDTM (ssdtm)

This is a collection of synthetic CDISC SDTM data creating functions using sequence generators. 

The low-fidelity synthetic SDTM data would be very valuable in multiple scenarios.

1. Allow non-production teams within biopharma companies, CROs, and health technology companies to build the systems without access the sensitive data.
2. Provide low-fidelity data as the default study database for testing purposes.
3. Test and validate the data pipelines before First-Patient-In within a study.
4. Overall assist with faster study startup time.


* Free software: MIT license


## Tutorial
--------


### How to install

```sh
$ pip install ssdtm
```

### Basic Usage

```sh
import ssdtm as sd

	
# Generate synthetic single-domain (adverse events) data for 5 patients
ae = sd.get_adverse_events(5)

# Generate synthetic single-domain (concomitant medication) data 5 patients
cm = sd.get_conmeds(5)

# Generate synthetic single-domain (adverse events) data 5 patients
dm = sd.get_demographics(5)

# Generate synthetic single-domain (adverse events) data 5 patients
ex = sd.get_exposure(5)

# Generate lab anbalytes dataset for 8 patients, where each patient has data for 4 visits.
lb = sd.get_lab_analytes(8,4)

# Generate vital signs dataset for 8 patients, where each patient has data for 4 visits.
vs = sd.get_vital_signs(8,4)

# Generates CDISC SDTM data for 7 domains (ae, cm, dm, ex, lb, rs, and vs)
data = sd.get_sdtm_data(8,4)
# Then you can access individual domain-specific dataframes as follows
data['cm']
data['dm']
data['vs']

# This generates and saves the SDTM data for 7 common SDTM domains in the local directory
sd.save_sdtm_data(8,4)

```
