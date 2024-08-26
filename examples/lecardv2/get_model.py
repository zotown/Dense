# @Time : 2024/8/24 15:33 
# @Author : LiuHuanghai
# @File : get_model.py 
# @Project: PyCharm

#模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('PollyZhao/bert-base-chinese',cache_dir='/root/autodl-tmp')