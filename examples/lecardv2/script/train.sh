TRAIN_DIR=../lecard-train-bert-base-chinese+typecrime
OUTDIR=model-lecard-bert-base-chinese+typecrime

python -m torch.distributed.launch --nproc_per_node=1 -m dense.driver.train \
  --output_dir $OUTDIR \
  --model_name_or_path /root/autodl-tmp/PollyZhao/bert-base-chinese/ \
  --do_train \
  --save_steps 20000 \
  --train_dir $TRAIN_DIR \
  --fp16 \
  --per_device_train_batch_size 4 \
  --train_n_passages 2 \
  --learning_rate 1e-5 \
  --q_max_len 512 \
  --p_max_len 512 \
  --num_train_epochs 40 \
  --negatives_x_device \
