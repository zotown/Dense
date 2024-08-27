TYPE="+typecrime"
ENCODE_DIR=embeddings-lecard-bert-base-chinese$TYPE
OUTDIR=temp
MODEL_DIR=model-lecard-bert-base-chinese$TYPE
CORPUS_DIR=../corpus
mkdir $ENCODE_DIR

python -m dense.driver.encode \
  --output_dir=$OUTDIR \
  --model_name_or_path $MODEL_DIR \
  --fp16 \
  --per_device_eval_batch_size 16 \
  --encode_in_path $CORPUS_DIR/corpus.json \
  --encoded_save_path $ENCODE_DIR/corpus.pt

ENCODE_QRY_DIR=embeddings-lecard-queries-bert-base-chinese$TYPE
OUTDIR=temp
QUERY=../corpus/query.json

mkdir $ENCODE_QRY_DIR
python -m dense.driver.encode \
  --output_dir=$OUTDIR \
  --model_name_or_path $MODEL_DIR \
  --fp16 \
  --per_device_eval_batch_size 2 \
  --encode_in_path $QUERY \
  --encoded_save_path $ENCODE_QRY_DIR/query.pt


DEPTH=100
RUN=run.lecard.test-bert-base-chinese$TYPE.txt

python -m dense.faiss_retriever \
--query_reps $ENCODE_QRY_DIR/query.pt \
--passage_reps $ENCODE_DIR/'*.pt' \
--depth $DEPTH \
--batch_size -1 \
--save_text \
--save_ranking_to $RUN