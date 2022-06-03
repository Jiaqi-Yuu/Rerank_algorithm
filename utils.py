def val(rerank_videos_set, rand_num):
    # 滑动窗口长度为8，若作者8出2，品类8出3，音乐8出1，算做成功打散
    for i in range(8, rand_num):
        window = rerank_videos_set[i-8:i]
        author_dict = {}
        class_dict = {}
        bgm_dict = {}
        for j in range(8):
            try:
                author = window[j][0]
            except:
                print(rerank_videos_set)
                print(len(rerank_videos_set))
            classes = window[j][1]
            bgm = window[j][2]
            if author not in author_dict:
                author_dict[author] = 1
            else:
                author_dict[author] += 1
                if author_dict[author] > 2:
                    return 0
            if classes not in class_dict:
                class_dict[classes] = 1
            else:
                class_dict[classes] += 1
                if class_dict[classes] > 3:
                    return 0
            if bgm not in bgm_dict:
                bgm_dict[bgm] = 1
            else:
                bgm_dict[bgm] += 1
                if bgm_dict[bgm] > 1:
                    return 0
    return 1

def order(videos_set, reranked_videos_set):
    n = len(videos_set)
    compare_len = int(n * 0.5)
    in_num = 0
    for i in range(compare_len):
        if videos_set[i] in reranked_videos_set[:compare_len]:
            in_num += 1
    return in_num / compare_len

def author_val(rerank_videos_set, rand_num):
    # 滑动窗口长度为8，作者8出2, 算做成功打散
    # window = rerank_videos_set[:8]
    for i in range(8, rand_num):
        window = rerank_videos_set[i-8:i]
        author_dict = {}
        for j in range(8):
            author = window[j][0]
            if author not in author_dict:
                author_dict[author] = 1
            else:
                author_dict[author] += 1
                if author_dict[author] > 2:
                    return 0
    return 1

def classes_val(rerank_videos_set, rand_num):
    # 滑动窗口长度为8，品类8出3，算做成功打散
    # window = rerank_videos_set[:8]
    for i in range(8, rand_num):
        window = rerank_videos_set[i-8:i]
        class_dict = {}
        for j in range(8):
            classes = window[j][1]
            if classes not in class_dict:
                class_dict[classes] = 1
            else:
                class_dict[classes] += 1
                if class_dict[classes] > 3:
                    return 0
    return 1

def bgm_val(rerank_videos_set, rand_num):
    # 滑动窗口长度为8，音乐8出1，算做成功打散
    # window = rerank_videos_set[:8]
    for i in range(8, rand_num):
        window = rerank_videos_set[i-8:i]
        bgm_dict = {}
        for j in range(8):
            bgm = window[j][2]
            if bgm not in bgm_dict:
                bgm_dict[bgm] = 1
            else:
                bgm_dict[bgm] += 1
                if bgm_dict[bgm] > 1:
                    return 0
    return 1