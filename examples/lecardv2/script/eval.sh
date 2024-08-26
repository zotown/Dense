RUN=run.lecard.test.txt
TREC_RUN=run.lecard.test.trec
python -m dense.utils.format.convert_result_to_trec --input $RUN --output $TREC_RUN

