TYPE=+crime
MODEL=Lawformer
TRAIN_DIR=../lecard-train-$MODEL$TYPE
OUTDIR=model-lecard-$MODEL$TYPE

python -m torch.distributed.launch --nproc_per_node=1 -m dense.driver.train \
  --output_dir $OUTDIR \
  --model_name_or_path /root/autodl-tmp/$MODEL \
  --do_train \
  --save_steps 20000 \
  --train_dir $TRAIN_DIR \
  --fp16 \
  --per_device_train_batch_size 2 \
  --train_n_passages 2 \
  --learning_rate 1e-5 \
  --q_max_len 512 \
  --p_max_len 512 \
  --num_train_epochs 40 \
  --negatives_x_device \
