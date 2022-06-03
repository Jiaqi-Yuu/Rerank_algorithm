import random
import numpy as np
def video(author_num, class_num, bgm_num):
    # 生成视频库，初始设置包含1000个作者id，30个品类id，100个背景音乐id
    author_id = [x for x in range(author_num)]
    class_id = [x for x in range(class_num)]
    bgm_id = [x for x in range(bgm_num)]
    if True:
        random.seed(100)
        random.shuffle(author_id)
        random.shuffle(class_id)
        random.shuffle(bgm_id)
    return author_id, class_id, bgm_id

# file_name = './video_dataset/' + str(rand_num) + '_samples'
# np.save(file_name, videos_set)