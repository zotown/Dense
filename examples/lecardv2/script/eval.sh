RUN=run.lecard.test.txt
TREC_RUN=run.lecard.test.trec
python -m dense.utils.format.convert_result_to_trec --input $RUN --output $TREC_RUN

TREC_RUN=run.lecard.test.trec
JSON_RUN=run.lecard.test.json
python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                                --index wikipedia-dpr \
                                                                --input $TREC_RUN \
                                                                --output $JSON_RUN

python -m pyserini.eval.evaluate_dpr_retrieval --retrieval $JSON_RUN --topk 1 5 10 20 30
