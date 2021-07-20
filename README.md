# Android App Bug Prediction
## The app
In this project bugs are predicted on an open source Android app namely Anki [1].
### About the app
Anki is a repetition technique.
Helps you memorize things by automatically repeating them.
No need to keep track of what to study or when to study it.

- Total Releases:          **997**
- Versions:                **0.3 - 1.1, 2.0 - 2.15**
- Bug reported versions:   **2.1 - 2.15**
- Used versions:           **2.1, 2.3, 2.8, 2.9, 2.11 - 2.15**
- All issues open/closed:  **359/4973**
- Bug issues open/closed:  **110/2340**

## Implementation
### 1.Dataset
The first step is dataset creation which needs to be done manually. Closed, labelled as Bug and linked to pull request(merge request) issues needed to be extracted. For that purpose Github API is used [4]. After fetching all issues with the specifications mentioned above, each fetched issues is inspected in order to find out versions that they have been mentioned in. Their class locations are also obtained in the same procedure by inspecting pull requests that they have been linked to. At the end of the day, we will have a dataset which has records as class locations and versions where classes are buggy as a feature.

### 2.DVM
Dalvik Virtual Machine is a runtime environment for Android apps. The primary difference between the Java Virtual Machine (JVM) and the Dalvik Virtual Machine is that Dalvik is register-based rather than stack-based, which allows it to be more memory economical. In other words, the Dalvik Virtual Machine interprets the resultant bytecode generated from Java sources. APK is the file format used to deliver Android apps and being stored in .zip file. Inside the .zip file, there is a file with the extension of .dex containing compiled application files. Since metrics can be extracted from compiled java files (byte code) I needed to reach out them. Compiled classes from .dex files can be extracted by using dex2jar [6] package which was done manually.

### 3.Metrics
Chidamber and Kemerer Java Metrics CKJM [2] is recommended for this task since it extracts many useful OO metrics. Different metric extractor software/packages are tested. One of them was Prest which was developed by Softlab(Bogazici University) in 2009 [5]. It is outdated and did not function as expected. Another tool is Dependency Finder which does not extract OO metrics that I was after. Metric extraction is applied on all classes for all used versions. APK files can be reached on [1].

### 4.Train and Test
After obtaining the metrics, the next step is training and testing the model. Four different algorithms such as Decision Tree Classifier, Random Forest Classifier, Logistic Regression and SVM to train and test the dataset. Performance of the model is monitored with precision, accuracy and recall scores for each algorithm.

### 5.Methodology
1. First step was fetching issues and creating the dataset as decribed in the first section (1. Dataset), and the code for fetching issues can be found in [fetch_issues.py](https://github.com/bakhyaddin/android-app-bug-prediction/blob/main/fetch_issues.py). Firstly, fetched data is stored in a Json [file](https://github.com/bakhyaddin/android-app-bug-prediction/blob/main/bug_issues_with_pr.json) then converted to [CSV](https://github.com/bakhyaddin/android-app-bug-prediction/blob/main/bug_issues_with_pr.csv). In the CSV file, each issue containes their respective link. Buggy classes and the versions that they are found in are collected manually and stored in [versions_and_classes.csv](https://github.com/bakhyaddin/android-app-bug-prediction/blob/main/versions_and_classes.csv) by inspecting in the links. [cleaned_versions_and_locations.csv](https://github.com/bakhyaddin/android-app-bug-prediction/blob/main/cleaned_versions_and_locations.csv) is created to make versions_and_classes.csv file more managable by running [clean_versions_and_classes.py](https://github.com/bakhyaddin/android-app-bug-prediction/blob/main/clean_versions_and_classes.py) script.
2. The second step was getting all classes' CKJM metrics by running [extract_metrics](https://github.com/bakhyaddin/android-app-bug-prediction/blob/main/extract_metrics.py) script which saves data in another folder called [metrics](https://github.com/bakhyaddin/android-app-bug-prediction/tree/main/metrics) for each version. Labeling records as buggy or not (1 and 0 respectively) was also done manully by taking advantage of previosly created [cleaned_versions_and_locations.csv](https://github.com/bakhyaddin/android-app-bug-prediction/blob/main/cleaned_versions_and_locations.csv).
3. The last step is training and testing phase. For this purpose all labelled CSV files are converted into [labelled/combined.csv](https://github.com/bakhyaddin/android-app-bug-prediction/blob/main/labelled/combined.csv). The training dataset consists of the combination of all the datasets that exist up to the test dataset. If version 2.8 is going to be used as a testing dataset then we need to train our model with datasets of version 2.1 and version 2.3.

### 6.Results
#### version 2.15 with Logistic Regression

- Prevalence: 4.18% of  classes have been flagged as defective

- Precision: 83% of identified as defective classes are in fact defects

- Recall: 14.7% of all defective classes (4.18%) is classified as defective

- Accuracy: 96.0%

- Confusion Matrix: 
```
    0    1
0 [766   1]
1 [ 29   5]
```

## References
- [1] https://github.com/ankidroid/Anki-Android
- [2] https://gromit.iiar.pwr.wroc.pl/p_inf/ckjm/
- [3] https://github.com/pxb1988/dex2jar
- [4] https://docs.github.com/en/rest
- [5] E. Kocaguneli, A. Bener, A. Tosun, B. Turhan. Prest: An Intelligent Software Metrics Extraction, Analysis and Defect Prediction Tool. DBLP conference paper, 2009

## [Presentation](https://docs.google.com/presentation/d/1LXYIboBlyS0ZC1IMv3zsyrQ357Oqifi0PKD66Tvg3oc/edit?usp=sharing)
