## What is the accuracy threshold?

Lower bound for the accuracy (clf) or scores (other scoring methods) of hotspot elements. Below that, 
an element will not be categorized as hotspot.

## How to find out a threshold that makes sense?
A good source of knowledge to go on is the accuracy/score of a pseudonetwork (NO effect) of comparable parameters.
Accuracy mostly depends on the given sample size, while also being influenced by the noise level and effect strength. 
The higher the threshold, the higher the specificity of the detection - but also the higher the chance NO network is
detected, even when there could be one.


## CLF-accuracies per sample size
Using the decision tree classification scores (`clf`), the recommended accuracy thresholds are listed in the table below.
The results were obtained by running 50 pseudonetwork trials (NO effect) with the `network_detection_algorithm_testing()`, for each sample size 
in np.range(20,1000,20). The corresponding data is in `/data/pt_01756/studies/network_mapping/testing_NDA/15484.08/pseudonetwork_data.csv`. 

The given recommendations represent the highest achieved accuracies of the tested pseudonetworks per sample size.
To conduct a more elaborate analysis use `appprox_optimal_acc_threshold()`  in ``result_analysis.py``.


| Sample Size | Accuracy Threshold |
|-------------|--------------------|
| 20          | 1                  |
| 40          | 0.93               |
| 60          | 0.87               |
| 80          | 0.81               |
| 100         | 0.77               |
| 120         | 0.77               |
| 140         | 0.74               |
| 160         | 0.73               |
| 180         | 0.72               |
| 200         | 0.71               |
| 220         | 0.71               |
| 240         | 0.7                |
| 260         | 0.69               |
| 280         | 0.69               |
| 300         | 0.69               |
| 320         | 0.7                |
| 340         | 0.67               |
| 360         | 0.67               |
| 380         | 0.67               |
| 400         | 0.65               |
| 420         | 0.65               |
| 440         | 0.64               |
| 460         | 0.64               |
| 480         | 0.64               |
| 500         | 0.63               |
| 520         | 0.63               |
| 540         | 0.63               |
| 560         | 0.63               |
| 580         | 0.63               |
| 600         | 0.62               |
| 620         | 0.63               |
| 640         | 0.62               |
| 660         | 0.62               |
| 680         | 0.62               |
| 700         | 0.61               |
| 720         | 0.61               |
| 740         | 0.61               |
| 760         | 0.62               |
| 780         | 0.61               |
| 800         | 0.61               |
| 820         | 0.61               |
| 840         | 0.61               |
| 860         | 0.61               |
| 880         | 0.6                |
| 900         | 0.6                |
| 920         | 0.6                |
| 940         | 0.6                |
| 960         | 0.6                |
| 980         | 0.6                |
| 1000        | 0.6                |

## R2 scores
No proper analysis has been conducted, but they tend to be much lower than clf-accuracies. 
Values of about ``0.15`` have proven sufficient.