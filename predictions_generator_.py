import csv
import pickle
import pandas as pd
import json
import requests
import os
from datetime import datetime

import isw_vector_generator

INPUT_DATA_FOLDER = "lab3/data/modified"
MODELS_FOLDER = "lab3/models"
MODEL_FILE = "model_3_tuned_no_sklearnx.pkl"
REGION_FILE = "regions.csv"
DATES_FILE = "dates.pkl"
VECTOR_FILE = "word_count_vector.pkl"


# addition funcs
def findRegion(check, regions):
    for region in regions:
        for regionTemp in region:
            if regionTemp == check:
                return region[4]
    return None


def findRegionName(regiond_id, regions):
    for region in regions:
        if region[4] == regiond_id:
            return region[2]
    return None


def findDate(dates, dateTemp):
    for date in dates:
        if date == dateTemp:
            return True
        if date > dateTemp:
            return False
    return False


def findVector(vectors, dates, date):
    for i in range(len(dates)):
        if dates[i] == date:
            return vectors[i]

    return None


def getAlarmByDate(location, date, alarmsDict):
    started = False
    for data in alarmsDict[location]:
        if data > (date + pd.Timedelta(hours=1, minutes=0, seconds=0)):
            if started:
                return 1
            else:
                return 0
            break
        started = not started
    return 0


url = "http://localhost:8080/forecast"


def generate_predictions():
    print("Started predictions generator")
    isw_vector_generator.main()

    with open(f"{INPUT_DATA_FOLDER}/{VECTOR_FILE}", 'rb') as datafile:
        vectors = pickle.load(datafile)

    vectors = vectors.toarray()
    vectorsFloat = []
    for i in range(len(vectors)):
        vectorsFloat.append([])
        for j in range(len(vectors[i])):
            vectorsFloat[i].append(float(vectors[i][j]))

    vectors = []
    with open(f"{INPUT_DATA_FOLDER}/{REGION_FILE}", newline='', encoding='utf-8') as csvfile:
        regions = list(csv.reader(csvfile))

    with open(f"{INPUT_DATA_FOLDER}/{DATES_FILE}", 'rb') as datafile:
        dates = pickle.load(datafile)

    for i in range(len(dates)):
        dates[i] = pd.to_datetime(dates[i].replace(".txt", ""), format="%d:%m:%y")
    dates = sorted(dates)

    pickled_model = pickle.load(open(f'{MODELS_FOLDER}/{MODEL_FILE}', 'rb'))

    response = requests.get(url)

    if response.status_code == 200:
        data = json.loads(response.text)
        # print(data)
    else:
        print(f"Error: {response.status_code}")
        exit()

    test_data = []
    prediction_descriptions = []
    for line in data['data']:
        words = line.split(',')
        test_data.append(words)
        prediction_descriptions.append([findRegionName(words[0], regions), words[17][0:5]])

    dayConditions = {}
    hourConditions = {}
    dayConditionsIndex = 16
    hourConditionsIndex = 29
    indexsToRemove = []
    for i in range(len(test_data)):
        if i % 10000 == 0:
            print(i)
        x = test_data[i]
        aaa = findRegion(x[0].split(",")[0], regions)
        if aaa is None:
            print(x)
        x[0] = aaa
        # remove  time

        x.pop(17)
        try:
            x[dayConditionsIndex] = dayConditions[x[dayConditionsIndex]]
        except (KeyError):
            dayConditions[x[dayConditionsIndex]] = len(dayConditions) + 1
            x[dayConditionsIndex] = dayConditions[x[dayConditionsIndex]]

        try:
            x[hourConditionsIndex] = hourConditions[x[hourConditionsIndex]]
        except (KeyError):
            hourConditions[x[hourConditionsIndex]] = len(hourConditions) + 1
            x[hourConditionsIndex] = hourConditions[x[hourConditionsIndex]]

        #     remove date
        x.pop(1)
        vector = vectorsFloat[len(vectorsFloat) - 1]
        x.extend(vector)

    #     weather.append(temp.copy())
    dayConditions = {}
    dayIcons = {}
    hourConditions = {}
    hourIcons = {}
    alarmsDict = {}
    vectorsFloat = []
    # print(len(indexsToRemove))
    # print(len(test_data))
    # for index in indexsToRemove:
    #     test_data.pop(index)

    for x in test_data:
        for i in range(len(x)):
            if x[i] == '':
                x[i] = 0.0
            if type(x[i]) is str:
                x[i] = float(x[i])
            if type(x[i]) is int:
                x[i] = float(x[i])
    for x in test_data:
        expected_features = pickled_model.n_features_in_
        if expected_features > len(x):
            for n in range(expected_features - len(x)):
                x.append(0.0)
        else:
            while len(x) > expected_features:
                x.pop()

    prediction = pickled_model.predict(test_data)
    print(max(prediction))
    now = datetime.utcnow()
    result = {}
    # formatted_result['regions_forecast']={}
    for n in range(len(prediction)):
        prediction[n] = round(prediction[n])
        alarm_expected = bool(prediction[n] == 1)
        place = prediction_descriptions[n][0]
        time = prediction_descriptions[n][1]
        if place not in result:
            result[place] = {}
        result[place][time] = alarm_expected

    modified_time = os.path.getmtime(f"{MODELS_FOLDER}/{MODEL_FILE}")

    modified_datetime = datetime.utcfromtimestamp(modified_time)

    formatted_date = modified_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

    formatted_result = {
        "last_model_train_time": formatted_date,
        "last_prediction_time": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "regions_forecast": result
    }
    with open("predictions_all.json", "w") as f:
        # Write the dictionary to the file in JSON format
        json.dump(formatted_result, f)


generate_predictions()

# if __name__ == '__main__':
#     generate_predictions()
