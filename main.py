import numpy as np
import random
import time
import os
from data import video
from utils import val, order, author_val, classes_val, bgm_val
from method import random_rerank, weight_rerank, window_rerank, newwindow_rerank

def start(experiment_num, method, video_dataset_length, feature_num, write_file_name):
    author_num, class_num, bgm_num = feature_num[0], feature_num[1], feature_num[2]
    author_id, class_id, bgm_id = video(author_num, class_num, bgm_num)
    # 根据视频库，随机生成视频数量为rand_num的视频列表，videos_set维度为(20，3)
    true_num = 0
    author_true_num = 0
    classes_true_num = 0
    bgm_true_num = 0
    start_time = time.time()
    total_order_ratio = 0
    for num in range(experiment_num):
        if num % 1000 == 0:
            print("experiment:{} is running".format(num))
        rand_num = video_dataset_length
        videos_set = []
        random.seed()
        while len(videos_set) < rand_num:
            author_sample = random.sample(author_id, 1)
            class_sample = random.sample(class_id, 1)
            bgm_sample = random.sample(bgm_id, 1)
            new_video = [author_sample[0], class_sample[0], bgm_sample[0]]
            if new_video not in videos_set:
                videos_set.append(new_video)
        videos_set_copy = videos_set.copy()
        if method == 'random':
            reranked_videos = random_rerank(videos_set)
        elif method == 'weight':
            reranked_videos = weight_rerank(videos_set, 1, 1, 1)
        elif method == 'window':
            reranked_videos = window_rerank(videos_set)
        elif method == 'newwindow':
            reranked_videos = newwindow_rerank(videos_set)
        true_num += val(reranked_videos, rand_num)
        author_true_num += author_val(reranked_videos, rand_num)
        classes_true_num += classes_val(reranked_videos, rand_num)
        bgm_true_num += bgm_val(reranked_videos, rand_num)
        order_ratio = order(videos_set_copy, reranked_videos)
        total_order_ratio += order_ratio
    end_time = time.time()
    total_time = end_time - start_time
    avg_order_ratio = total_order_ratio / experiment_num
    print("\ttotal_time:{}, acc:{}, author_acc:{}, classes_acc:{}, bgm_acc:{}".format(total_time, true_num/experiment_num, author_true_num/experiment_num, classes_true_num/experiment_num, bgm_true_num/experiment_num))
    result_file_name = write_file_name
    result_file_path = os.path.join("./result/", result_file_name)
    with open(result_file_path, "a") as f:
        print("experiment_num={}, method={}, videos_num={}, data_attributes={}:".format(experiment_num, method, video_dataset_length, feature_num), file=f)
        print("\taverage_order_ratio:", avg_order_ratio, file=f)
        print("\ttotal_time:", total_time, file=f)
        print("\tacc:", true_num/experiment_num, file=f)
        print("\tauthor_acc:", author_true_num / experiment_num, file=f)
        print("\tclasses_acc:", classes_true_num / experiment_num, file=f)
        print("\tbgm_acc:", bgm_true_num / experiment_num, file=f)


method_candidates = ['random', 'weight', 'window']
videos_dataset_length_candidates = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
feature_num_candidates = [[1000, 30, 100], [100, 30, 100], [1000, 30, 1000], [100, 100, 100]]
# weight_alpha = [[1, 1, 1], [1, 1, 2], [1, 1, 5], [1, 1, 10], [1, 2, 5]]
for method in method_candidates:
    for feature_num in feature_num_candidates:
        for videos_dataset_length in videos_dataset_length_candidates:
            start(10000, method, videos_dataset_length, feature_num, method + '_result')

