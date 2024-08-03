# pyNIBS
Preprocessing, postprocessing, and analyses routines for non-invasive brain stimulation experiments.

[![Latest Release](https://gitlab.gwdg.de/tms-localization/pynibs/-/badges/release.svg)](https://gitlab.gwdg.de/tms-localization/pynibs)
[![Documentation](https://readthedocs.org/projects/pynibs/badge/)](https://pynibs.readthedocs.io/)
[![pipeline status](https://gitlab.gwdg.de/tms-localization/pynibs/badges/master/pipeline.svg)](https://gitlab.gwdg.de/tms-localization/pynibs/commits/master)
[![coverage report](https://gitlab.gwdg.de/tms-localization/pynibs/badges/master/coverage.svg)](https://tms-localization.pages.gwdg.de/pynibs)

![](https://gitlab.gwdg.de/uploads/-/system/project/avatar/9753/Fig_4.png?width=128)

`pyNIBS` provides the functions to allow **cortical mappings** with transcranial magnetic stimulation (TMS) via **functional analysis**. `pyNIBS` is developed to work with [SimNIBS](http://www.simnibs.org), i.e. SimNIBS' meshes and FEM results can directly be used.
 Currently, [SimNIBS 3.2.6](https://github.com/simnibs/simnibs/releases/tag/v3.2.6) and [SimNIBS >=4.0](https://github.com/simnibs/simnibs/releases/latest) are supported.

See the [documentation](https://pynibs.readthedocs.io/) for package details and our [protocol](https://doi.org/10.1038/s41596-022-00776-6) publication for a extensive usage examples. Free view only version of the paper: https://t.co/uv7CmVw6tp.

## Installation
Via PiP:

``` bash
pip install pynibs
```

Or clone the source repository and install the development branch for the most recent version:

``` bash
git clone https://gitlab.gwdg.de/tms-localization/pynibs
cd pynibs
git checkout dev
pip install -e .
```

See [here](https://gitlab.gwdg.de/tms-localization/papers/tmsloc_proto/-/blob/2aec4763edf17e7a2ac604403287bc7fb10285ff/README.md) for more detailed installation instructions.

To import CED Signal EMG data use the `export to .mat` feature of Signal. 
To read `.cfs` files exported with CED Signal you might need to [manually](HOW_TO_INSTALL_BIOSIG.txt) compile the libbiosig package.


## Bugs
For sure. Please open an [issue](https://gitlab.gwdg.de/tms-localization/pynibs/-/issues) or feel free to file a PR.


## Citation
Please cite _Numssen, O., Zier, A. L., Thielscher, A., Hartwigsen, G., Knösche, T. R., & Weise, K. (2021). Efficient high-resolution TMS mapping of the human motor cortex by nonlinear regression. NeuroImage, 245, 118654. doi:[10.1016/j.neuroimage.2021.118654](https://doi.org/10.1016/j.neuroimage.2021.118654)_ when using this toolbox in your research.


## References
  - Weise*, K., Numssen*, O., Thielscher, A., Hartwigsen, G., & Knösche, T. R. (2020). A novel approach to localize cortical TMS effects. *NeuroImage*, 209, 116486. doi: [10.1016/j.neuroimage.2019.116486](https://doi.org/10.1016/j.neuroimage.2019.116486)
  - Numssen, O., Zier, A. L., Thielscher, A., Hartwigsen, G., Knösche, T. R., & Weise, K. (2021). Efficient high-resolution TMS mapping of the human motor cortex by nonlinear regression. *NeuroImage*, 245, 118654. doi:[10.1016/j.neuroimage.2021.118654](https://doi.org/10.1016/j.neuroimage.2021.118654)
  - Weise*, K., Numssen*, O., Kalloch, B., Zier, A. L., Thielscher, A., Hartwigsen°, G., Knösche°, T. R. (2023). Precise transcranial magnetic stimulation motor-mapping. *Nature Protocols*. doi:[10.1038/s41596-022-00776-6](https://doi.org/10.1038/s41596-022-00776-6) 
  - Jing, Y., Numssen, O., Weise, K., Kalloch, B., Buchberger, L., Haueisen, J., Hartwigsen, G., Knösche, T. (2023). Modeling the Effects of Transcranial Magnetic Stimulation on Spatial Attention. *Physics in Medicine & Biology*. doi: [10.1088/1361-6560/acff34](https://doi.org/10.1088/1361-6560/acff34)
  - Numssen, O., Kuhnke, P., Weise, K., & Hartwigsen, G. (2024). Electric field based dosing for TMS. *Imaging Neuroscience*. doi: [10.1162/imag_a_00106](https://doi.org/10.1162/imag_a_00106) 