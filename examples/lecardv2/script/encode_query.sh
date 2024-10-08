ENCODE_QRY_DIR=embeddings-lecard-queries-bert-base-chinese+com
OUTDIR=temp
MODEL_DIR=model-lecard-bert-base-chinese+com
QUERY=../corpus/query.json

mkdir $ENCODE_QRY_DIR
python -m dense.driver.encode \
  --output_dir=$OUTDIR \
  --model_name_or_path $MODEL_DIR \
  --fp16 \
  --per_device_eval_batch_size 2 \
  --encode_in_path $QUERY \
  --encoded_save_path $ENCODE_QRY_DIR/query.pt