from knndtw import recognizer
if __name__ == "__main__":
    recognizer = recognizer.ActivityRecognizer("/home/yupeng/FALL2020/UFII/FT-DTW/Data/ROAMM-1",
                                               "/home/yupeng/FALL2020/UFII/FT-DTW/Data/mock1-test",
                                               "/home/yupeng/FALL2020/UFII/FT-DTW/Data/ROAMM-1.txt")
    recognizer.visualize(1)
