# @Time : 2024/8/24 15:33 
# @Author : LiuHuanghai
# @File : get_model.py 
# @Project: PyCharm

#模型下载
from modelscope import snapshot_download
model_dir = snapshot_download('AI-ModelScope/bert-base-uncased',cache_dir='/root/autodl-tmp')