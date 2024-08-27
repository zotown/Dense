ENCODE_QRY_DIR=embeddings-lecard-queries-bert-base-chinese+com
ENCODE_DIR=embeddings-lecard-bert-base-chinese+com
DEPTH=100
RUN=run.lecard.test-bert-base-chinese+com.txt

python -m dense.faiss_retriever \
--query_reps $ENCODE_QRY_DIR/query.pt \
--passage_reps $ENCODE_DIR/'*.pt' \
--depth $DEPTH \
--batch_size -1 \
--save_text \
--save_ranking_to $RUN