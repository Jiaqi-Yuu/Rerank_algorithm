import random
import ast
def random_rerank(videos_set):
    random.shuffle(videos_set)
    return videos_set

def weight_rerank(videos_set, author_alpha, classes_alpha, bgm_alpha):
    author_dict = {}
    classes_dict = {}
    bgm_dict = {}
    weight_videos_set_dict = {}
    for i in range(len(videos_set)):
        author = videos_set[i][0]
        classes = videos_set[i][1]
        bgm = videos_set[i][2]
        if author not in author_dict:
            author_dict[author] = 1
        else:
            author_dict[author] += 1
        if classes not in classes_dict:
            classes_dict[classes] = 1
        else:
            classes_dict[classes] += 1
        if bgm not in bgm_dict:
            bgm_dict[bgm] = 1
        else:
            bgm_dict[bgm] += 1
        weight_cur = author_dict[author] * author_alpha + classes_dict[classes] * classes_alpha + bgm_dict[bgm] * bgm_alpha
        weight_videos_set_dict[str(videos_set[i])] = weight_cur
    reranked_videos_set = []
    temp = sorted(weight_videos_set_dict.items(), key=lambda x: x[1])
    for key in temp:
        reranked_videos_set.append(ast.literal_eval(key[0]))
    return reranked_videos_set


def window_rerank(videos_set):
    reranked_videos_num = len(videos_set)
    reranked_videos_set = []
    author_dict = {}
    classes_dict = {}
    bgm_dict = {}
    while True:
        for i in range(len(videos_set)):
            author = videos_set[i][0]
            classes = videos_set[i][1]
            bgm = videos_set[i][2]
            if classes not in classes_dict:
                classes_dict[classes] = 1
            elif classes_dict[classes] > 2:
                continue
            else:
                classes_dict[classes] += 1
            if author not in author_dict:
                author_dict[author] = 1
            elif author_dict[author] > 1:
                classes_dict[classes] -= 1
                continue
            else:
                author_dict[author] += 1

            if bgm not in bgm_dict:
                bgm_dict[bgm] = 1
            elif bgm_dict[bgm] > 0:
                author_dict[author] -= 1
                classes_dict[classes] -= 1
                continue
            else:
                bgm_dict[bgm] += 1
            reranked_videos_set.append(videos_set[i])
            if len(reranked_videos_set) > 7:
                del_video = reranked_videos_set[-8]
                del_author = del_video[0]
                del_classes = del_video[1]
                del_bgm = del_video[2]
                author_dict[del_author] -= 1
                classes_dict[del_classes] -= 1
                bgm_dict[del_bgm] -= 1
            videos_set.pop(i)
            break
        if i == len(videos_set)-1:
            reranked_videos_set.extend(videos_set)
            break
        if len(reranked_videos_set) == reranked_videos_num:
            break
    return reranked_videos_set


def newwindow_rerank(videos_set):
    reranked_videos_num = len(videos_set)
    reranked_videos_set = []
    author_dict = {}
    classes_dict = {}
    bgm_dict = {}
    flag = 0
    while True:
        is_have = 0
        for i in range(len(videos_set)):
            author = videos_set[i][0]
            classes = videos_set[i][1]
            bgm = videos_set[i][2]
            if classes not in classes_dict:
                classes_dict[classes] = 1
            elif classes_dict[classes] > 2:
                continue
            else:
                classes_dict[classes] += 1
            if author not in author_dict:
                author_dict[author] = 1
            elif author_dict[author] > 1:
                classes_dict[classes] -= 1
                continue
            else:
                author_dict[author] += 1

            if bgm not in bgm_dict:
                bgm_dict[bgm] = 1
            elif bgm_dict[bgm] > 0:
                author_dict[author] -= 1
                classes_dict[classes] -= 1
                continue
            else:
                bgm_dict[bgm] += 1
            is_have = 1
            reranked_videos_set.append(videos_set[i])
            if len(reranked_videos_set) > 7:
                del_video = reranked_videos_set[-8]
                del_author = del_video[0]
                del_classes = del_video[1]
                del_bgm = del_video[2]
                author_dict[del_author] -= 1
                classes_dict[del_classes] -= 1
                bgm_dict[del_bgm] -= 1
            videos_set.pop(i)
            break
        if is_have == 0 and flag < 5:
            j = 0
            for m in range(len(videos_set)):
                has_changed = 0
                while j < len(reranked_videos_set)-8 and has_changed == 0:
                    for k in range(-7, 1):
                        if j + k >= 0:
                            if istrue(j+k, reranked_videos_set, videos_set[m]):
                                temp = reranked_videos_set[j]
                                reranked_videos_set[j] = videos_set[m]
                                videos_set[m] = temp
                                has_changed = 1
                            else:
                                break
                    j += 1
            flag += 1
        elif flag >= 5:
            reranked_videos_set.extend(videos_set)
        if len(reranked_videos_set) == reranked_videos_num:
            break
    return reranked_videos_set

def istrue(num, reranked_videos_set, videos_set):
    author_dict = {}
    classes_dict = {}
    bgm_dict = {}
    author_dict[videos_set[0]] = 1
    classes_dict[videos_set[1]] = 1
    bgm_dict[videos_set[2]] = 1
    for i in range(num+1, num+8):
        author = reranked_videos_set[i][0]
        classes = reranked_videos_set[i][1]
        bgm = reranked_videos_set[i][2]
        if author not in author_dict:
            author_dict[author] = 1
        else:
            author_dict[author] +=1
        if classes not in classes_dict:
            classes_dict[classes] = 1
        else:
            classes_dict[classes] += 1
        if bgm not in bgm_dict:
            bgm_dict[bgm] = 1
        else:
            bgm_dict[bgm] += 1
        if author_dict[author] > 2 or classes_dict[classes] > 3 or bgm_dict[bgm] > 1:
            return False
    return True