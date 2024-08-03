# Network detection: Guide to using the configuration files

All settings and parameters relevant in the network detection process can be adjusted via the configuration files.
Here is a short explanation of the process and the configuration entries. 

## Loading the config file

Using the following code you can add the desired configuration file to your script:

    import yaml
    # choose file name and path
    configfile = 'configuration_TEMPLATE.yaml'  
    config_path = '/data/pt_01756/software/git/pynibs/data/network mapping configuration'
    # read configfile
    with open(f'{config_path}/{configfile}', "r") as yamlfile:
        config = yaml.load(yamlfile, Loader=yaml.FullLoader)
        print("-" * 64)
        print("Using file '" + configfile + "' for current parameter setting.")
        print("-" * 64)

Aside from that, the NDA application and testing functions only need the experimental data (e_matrix, response_values, roi_surf, fn_geo)
and the base_path (output folder).

## Configuration Parameters Guide

There are two different main functions: `network_detection_algorithm_testing()` and 
`network_detection_algorithm_application()`. The configuration parameters are very similar, many entries apply to both. 
They are presented separately in the following for simplicity.


### Application (real data)

<u> Binarization </u>

Data binarization is a crucial preprocessing step since it determines what data the algorithm considers as affected.
Carefully adjust to the data at hand. Note that this is only relevant for the scoring_method 'clf'.
Default function is `binarize_response_data()`. For MEPs, you could also use `binarize_real_meps()`.

- ``bin_method``: Method used to calculate the binarization threshold.
  - Options: `'mean'`, `'slope'`, `'median'`.

- ``bin_factor``: Multiplied with the value of `bin_method(response)` is used as binarization threshold. 
(Above=1=affected, below=0=not affected).

<u> Scoring </u>

- ``scoring_method``: Select the method for the computation of hotspot scores per ROI element. 
  - Options: `'clf'`, `'regression'`, `'regress_data'` (single hotspot), `'mi'` (single hotspot).
  - Remark: 
  Network detection:
    - `'clf'`: Scores are based on the accuracies of Decision Tree Classifiers of pairwise element combinations. (recommended)
    - `'regression'`: Scores are the R2-scores of multivariable regression.
    - `'regress_data'`: Scores are the R2-score of a sigmoidal fit.
    - `'mi'`: Scores are the mutual information scores of the e-fields and the response variables.

- ``scoring_emag_thr``: Threshold above which elements are scored. 
More specifically: Per element, the `e_mag_max` as the
maximum e-field magnitude reached in all zaps indicates how accessible an element is to stimulation (gyral element have
the highest `e_mag_max`). This parameter is the lower bound for the `e_mag_max` of all scored elements. 
  - Remark: The higher the threshold, the higher the scored elements are on the cortical ROI.

- ``scoring_interval``: Interval at which elements are scored, determines subsampling resolution.
  - Remark: `1/scoring_interval` elements are scored. Adjust to balance between computational efficiency and scoring detail.

<u>Detection</u>

- ``acc_thr``: Lower bound for the accuracy (clf) or scores (other scoring methods) of hotspot elements. Below that, 
an element will not be categorized as hotspot.
  - Remark: See recommendation sheet``data/network mapping configuration/recommendations_for_accuracy_threshold.md``.
  For the clf-method, there is a table included recommending accuracy thresholds based on sample size.

- ``corr_thr``: Correlation threshold (upper bound) for hotspot pairs. 
  - Remark: When a second hotspot candidate too highly 
  correlates with the first one, it is ignored, to avoid double detection of a single hotspot. Preliminary analyses have 
  shown that this threshold does not have a lot of impact.
  - 1: no limitation to how correlated they are, 0: only one hotspot allowed)
 

<u>Additional Info</u>

- ``note``: Arbitrary string for additional comments or notes.

- ``fn_flag``: String to be mentioned in the output files. (to distinguish)

- ``subject_id``: ID of the subject.
- ``response_spec``:  Specification (if any) to retrieve the response. (e.g. FDI, APB,...)
- ``e_field``:  Specification (if any) to retrieve the e-field values. (E_tan, E_mag, E_norm)


The remaining 8 entries are not saved in the results overview. Namely the following: 

- ``save_files``:  (boolean) Whether to save hotspot scores and scoremaps as HDF5 files.

- ``write_effect_map``: (boolean) Whether to create an effect map. See more under <u> Effect map </u>.

- ``fn_results``: Filename for the CSV the results/evaluation should be saved in.
To understand output, see ``output_documentation``.


<u> Effect map </u>

If the output should include an effect map (useful for validation), the following parameters should be included.

- ``effect_full``:  The e-field magnitude that approximately needs to be reached to achieve the desired effect (in  µV).

- ``effect_saturation``: The approx. e-field magnitude at which the effect is expected to saturate (in  µV).

The effect map depicts the following: Assuming a network as detected was in effect, where can the effect
be expected highest/lowest? I.e., where is the response expected to be affected most/least?
This can be useful during experimental validation. 

<u>Plotting</u> 

- ``plot_std``: (boolean) Whether to plot the response data with color indicating response value, and the e-field values
of the chosen hotspots on x- and y-axis.

- ``plot_bin``: (boolean) Whether to plot the binarized response data with color indicating response category, 
and the e-field values of the chosen hotspots on x- and y-axis.

- ``plot_curves``: (boolean) Whether to create two response data scatter plots, one for each chosen hotspot. (e-field 
magnitudes on x-axis, response on y-axis).


### Testing (generated data)

<u> Artificial Data Generation </u>

The response will be generated as if `hotspot_elm0` and `hotspot_elm1` 
form a network of type `network_type`. See function `create_response_data()` for the detailed process.

- ``hotspot_elm0``:  `[0, n_elms-1]`
Specify the index of the first hotspot element. 

- ``hotspot_elm1``: `[0, n_elms-1]`
Specify the index of the second hotspot element.

- ``sample_size``: The desired number of samples. Bounded by the number of available e-fields. 
If `sample_size` is smaller, e-fields are randomly chosen. 
(See `create_dummy_binary_data.py` for more elaborate e-field choosing functions.)

- ``rn_seed``: Seed for all processes that are in some way random, ensuring reproducibility.

- ``distribution_type``: Defines the statistical distribution type for data generation.
  - Options: `'normal'`, `'logistic'`.  
  - Remark: `'ExGaussian'` is also an option but is not fully implemented. 

- ``network_type``: Choose the network the two hotspots are forming. 
  - Options: `['NO', 'AND', '1_INH_0', 'SH_0', '0_INH_1', 'SH_1', 'XOR', 'OR']`.
  - Remark:
    - (1) NO: No network ("pseudonetwork").
    - (2) AND: Dual node network: Effect if elm0 AND elm1 are stimulated.
    - (3) 1_INH_0: Dual node network: elm1 inhibits elm0, elm0 has an effect.
    - (4) SH_0: Single hotspot: Only elm0 has an effect.
    - (5) 0_INH_1: Dual node network: elm0 inhibits elm1, elm1 has an effect.
    - (6) SH_1: Single hotspot: Only elm1 has an effect.
    - (7) XOR: Dual node network: elm0 inhibits elm1, elm1 inhibits elm0. Both have an effect.
    - (8) OR: Dual node network: Effect if either elm0 or elm1 is stimulated.

- ``effect_full``: E-field magnitude at which the desired effect fully manifests.
  - Remark: What value makes sense here strongly depends on the range of the e-field values. 
  For normalized e-field values (1% stimulator intensity) across the motor cortex, values tend to range up to 1.6 µV. 
  We chose to normalize the effect to 0.9 µV.

- ``effect_saturation``: E-field magnitude at which the desired effect saturates.
  - Remark: See `effect_full`. We chose an effect saturation at 1.2 µV.

- ``jitter_ratio``: Percentage of data receiving random response values (uniformly distributed within the expected range).

- ``jitter_scale``: Multiplied with the mean value to calculate distribution deviation. Note that a heteroscedastic 
distribution is implemented at the moment -> the higher the effect, the higher the deviation. 


<u> Binarization </u>

Data binarization is a crucial preprocessing step since it determines what data the algorithm considers as affected.
Carefully adjust to the data at hand.
Default function is `binarize_response_data()`. For MEPs, you could also use `binarize_real_meps()`.

- ``bin_method``: Method used to calculate the binarization threshold.
  - Options: `'mean'`, `'slope'`, `'median'`.

- ``bin_factor``: Multiplied with the value of `bin_method(response)` is used as binarization threshold. 
(Above=1=affected, below=0=not affected).

<u> Scoring </u>

- ``scoring_method``: Select the method for the computation of hotspot scores per ROI element. 
  - Options: `'clf'`, `'regression'`, `'regress_data'` (single hotspot), `'mi'` (single hotspot).
  - Remark: 
  Network detection:
    - `'clf'`: Scores are based on the accuracies of Decision Tree Classifiers of pairwise element combinations. (recommended)
    - `'regression'`: Scores are the R2-scores of multivariable regression.
    - `'regress_data'`: Scores are the R2-score of a sigmoidal fit.
    - `'mi'`: Scores are the mutual information scores of the e-fields and the response variables.

- ``scoring_emag_thr``: Threshold above which elements are scored. 
More specifically: Per element, the `e_mag_max` as the
maximum e-field magnitude reached in all zaps indicates how accessible an element is to stimulation (gyral element have
the highest `e_mag_max`). This parameter is the lower bound for the `e_mag_max` of all scored elements. 
  - Remark: The higher the threshold, the higher the scored elements are on the cortical ROI.

- ``scoring_interval``: Interval at which elements are scored, determines subsampling resolution.
  - Remark: `1/scoring_interval` elements are scored. Adjust to balance between computational efficiency and scoring detail.

<u>Detection</u>

- ``acc_thr``: Lower bound for the accuracy (clf) or scores (other scoring methods) of hotspot elements. Below that, 
an element will not be categorized as hotspot.
  - Remark: Remark: See recommendation sheet``data/network mapping configuration/recommendations_for_accuracy_threshold.md``.
  For the clf-method, there is a table included recommending accuracy thresholds based on sample size.

- ``corr_thr``: Correlation threshold (upper bound) for hotspot pairs. 
  - Remark: When a second hotspot candidate too highly 
  correlates with the first one, it is ignored, to avoid double detection of a single hotspot. Preliminary analyses have 
  shown that this threshold does not have a lot of impact.
  - 1: no limitation to how correlated they are, 0: only one hotspot allowed)

- ``note``: Arbitrary string for additional comments or notes.

The remaining 5 entries are not saved in the results overview. Namely the following: 

<u>Evaluation</u>

- ``save_files``: (boolean) Whether to save hotspot scores and scoremaps as HDF5 files.

- ``fn_results``: Filename for the CSV the results/evaluation should be saved in.
To understand output, see ``output_documentation``.

<u>Plotting</u> 

- ``plot_std``: (boolean) Whether to plot the response data with color indicating response value, and the e-field values
of the chosen hotspots on x- and y-axis.

- ``plot_bin``: (boolean) Whether to plot the binarized response data with color indicating response category, 
and the e-field values of the chosen hotspots on x- and y-axis.

- ``plot_curves``: (boolean) Whether to create two response data scatter plots, one for each chosen hotspot. (e-field 
magnitudes on x-axis, response on y-axis).