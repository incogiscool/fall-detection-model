import os
import pandas as pd
from lib.subject import Subject

def regularize(data: list[int], window: int = 20) -> list[int]:
    # Chunk the data into windows
    windows = []
    for i in range(0, len(data), window):
        windows.append(data[i:i+window])
    
    # Calculate the average of each window
    averages = []
    for window in windows:
        averages.append(sum(window) / len(window))

    return averages

def clean_dataset(dataset_path: str, output_path: str):
    data = os.listdir(dataset_path)

    file_data = []

    for folder in data:
        if not folder.startswith("SA"):
            continue

        subject_data = Subject(folder)
        subject_data.load_data()
        subject_data.tokenize_age()
        
        for file in os.listdir(os.path.join(dataset_path, folder)):
            if not file.endswith(".txt"):
                continue

            is_fall = 0
            if file.startswith("F") and file[1].isdigit():
                is_fall = 1

            with open(os.path.join(dataset_path, folder, file), "r") as f:
                lines = f.readlines()

                # 200hz - trim to 10s
                line_amount = 10 * 200
                lines = lines[:line_amount]

                acceleration_x = []
                acceleration_y = []
                acceleration_z = []
                rotation_x = []
                rotation_y = []
                rotation_z = []

                for line in lines:
                    data = line.replace(";", "").replace("\n", "").split(",")

                    if len(data) < 6:
                        continue
                    
                    data = [int(d.replace(" ", "")) for d in data]
                    
                    acceleration_x.append(data[0])
                    acceleration_y.append(data[1])
                    acceleration_z.append(data[2])
                    rotation_x.append(data[3])
                    rotation_y.append(data[4])
                    rotation_z.append(data[5])
                    
                # Regularize the data - NOTE: Polling is 10hz after regularization

                file_data.append({
                    "acceleration_x": regularize(acceleration_x),
                    "acceleration_y": regularize(acceleration_y),
                    "acceleration_z": regularize(acceleration_z),
                    "rotation_x": regularize(rotation_x),
                    "rotation_y": regularize(rotation_y),
                    "rotation_z": regularize(rotation_z),
                    "is_fall": is_fall,
                    "age": subject_data.age,
                    "height": subject_data.height,
                    "weight": subject_data.weight,
                    "gender": subject_data.gender
                })
                
    accelerometer_data_length = len(file_data[0]["acceleration_x"])

    data = {
        "is_fall": [],
        "age": [],
        "height": [],
        "weight": [],
        "gender": []
    }

    for i in range(accelerometer_data_length):
        data[f"acceleration_x_{i}"] = []
        data[f"acceleration_y_{i}"] = []
        data[f"acceleration_z_{i}"] = []
        data[f"rotation_x_{i}"] = []
        data[f"rotation_y_{i}"] = []
        data[f"rotation_z_{i}"] = []

    for file in file_data:
        data["is_fall"].append(file["is_fall"])
        data["age"].append(file["age"])
        data["height"].append(file["height"])
        data["weight"].append(file["weight"])
        data["gender"].append(file["gender"])

        for i in range(accelerometer_data_length):
            data[f"acceleration_x_{i}"].append(file["acceleration_x"][i])
            data[f"acceleration_y_{i}"].append(file["acceleration_y"][i])
            data[f"acceleration_z_{i}"].append(file["acceleration_z"][i])
            data[f"rotation_x_{i}"].append(file["rotation_x"][i])
            data[f"rotation_y_{i}"].append(file["rotation_y"][i])
            data[f"rotation_z_{i}"].append(file["rotation_z"][i])

    
    dataframe = pd.DataFrame(data)
    dataframe.to_csv(output_path, index=False)
