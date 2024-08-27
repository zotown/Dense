ENCODE_DIR=embeddings-lecard-bert-base-chinese+com
OUTDIR=temp
MODEL_DIR=model-lecard-bert-base-chinese+com
CORPUS_DIR=../corpus
mkdir $ENCODE_DIR

python -m dense.driver.encode \
  --output_dir=$OUTDIR \
  --model_name_or_path $MODEL_DIR \
  --fp16 \
  --per_device_eval_batch_size 16 \
  --encode_in_path $CORPUS_DIR/corpus.json \
  --encoded_save_path $ENCODE_DIR/corpus.pt
