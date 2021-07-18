import subprocess
import pandas as pd

versions = [2.1, 2.3, 2.8, 2.9, 2.11, 2.12, 2.13, 2.14, 2.15]
# versions = [2.1]
cols = ["name", "wmc", "dit", "noc", "cbo", "rfc", "lcom", "ca", "ce", "npm", "lcom3", "loc", "dam", "moa", "mfa", "cam", "ic", "cbm", "amc", "is_Bug", "version"]

for version in versions:
    proc = subprocess.Popen(['sh', './sh_files/{}.sh'.format(version)], stdout=subprocess.PIPE)
    count = 0
    rows = []
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        class_metric_data = line.rstrip().decode('ascii')
        if "~" not in class_metric_data and len(class_metric_data.split(" ")) == len(cols) - 2:
            count += 1
            metrics = class_metric_data.split(" ")
            data_row = {}
            for i in range(len(cols)):
                if cols[i] == "is_Bug":
                    data_row["is_Bug"] = 0
                    continue
                if cols[i] == "version":
                    data_row["version"] = version
                    break
                data_row[cols[i]] = metrics[i]
            rows.append(data_row)
        df = pd.DataFrame(rows, columns=cols).set_index("name")
        df.to_csv('./metrics/{}.csv'.format(version))

    print(count)

