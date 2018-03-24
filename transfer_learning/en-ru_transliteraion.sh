# 1) download he-en data to DATA_DIR path (should exists: DATA_DIR/en.train.txt, DATA_DIR/he.train.txt for training)
# 2) set TRAIN_SIZE (in 1000, for example: 236 means 236k. 236 is about 80% of all dataset, set TRAIN_SIZE <= 236 or change test/dev sizes)
# 3) run this script

PROBLEM=translate_en_to_ru
MODEL=transformer
HPARAMS=transformer_base_single_gpu
BATCH_SIZE=512

ROOT_DATA_DIR=/media/roman/Elements/LowResourceNMT
DATA_DIR=$ROOT_DATA_DIR/enru_data/t2t_data
TMP_DIR=$ROOT_DATA_DIR/enru_data/t2t_datagen
TRAIN_DIR=$ROOT_DATA_DIR/enru_data/t2t_train/$PROBLEM/$MODEL-$HPARAMS
USR_DIR=/home/roman/shad/NLP/project/lowResourceNMT/translate_enhe

BEAM_SIZE=4
ALPHA=0.6
TRAIN_STEPS=10
ITERATION_SIZE=1000
OTHER_PARAMS=""
DATAGEN=1
MOVE_MODEL=1


# T2T_DATAGEN_PATH=t2t-datagen
# $T2T_DATAGEN_PATH \
#   --data_dir=$DATA_DIR \
#   --tmp_dir=$TMP_DIR \
#   --problem=$PROBLEM \
#   --t2t_usr_dir=$USR_DIR


DEV=($DATA_DIR/ru.dev.txt $DATA_DIR/en.dev.txt)
TEST=($DATA_DIR/ru.test.txt $DATA_DIR/en.test.txt)

compute_bleu() {
  t2t-decoder \
    --data_dir=$DATA_DIR \
    --problems=$PROBLEM \
    --model=$MODEL \
    --hparams_set=$HPARAMS \
    --output_dir=$TRAIN_DIR \
    --decode_hparams="beam_size=$BEAM_SIZE,alpha=$ALPHA" \
    --decode_from_file=$2 \
    --decode_to_file=$DATA_DIR/en-to-ru.translit.txt \
    --hparams="batch_size=$BATCH_SIZE" \
    --t2t_usr_dir=$USR_DIR
  # t2t-bleu --translation=$DATA_DIR/en-to-ru.translit.txt --reference=$1 >> $3
  echo $1
  echo $2
  echo $3
}

TEST_LOG=$TRAIN_DIR/test_log.txt
DEV_LOG=$TRAIN_DIR/dev_log.txt
# for i in $TEST_LOG $DEV_LOG
# do
#   echo $i
#   if [[ -f $i ]]; then
#     echo "EXIST $i"
#     mv $i $i$STAMP
#   fi
# done
# if [[ ! -d $TRAIN_DIR ]]; then 
#     mkdir $TRAIN_DIR
# fi

t2t-trainer \
    --data_dir=$DATA_DIR \
    --problems=$PROBLEM \
    --model=$MODEL \
    --hparams_set=$HPARAMS \
    --hparams="batch_size=$BATCH_SIZE" \
    --output_dir=$TRAIN_DIR \
    --train_steps=25000 \
    --t2t_usr_dir=$USR_DIR

# TRAIN_STEPS=1
# for ((i=1;i<=$TRAIN_STEPS;i++)); do
#   echo $(($i * $ITERATION_SIZE));
#   #train step
#   t2t-trainer \
#     --data_dir=$DATA_DIR \
#     --problems=$PROBLEM \
#     --model=$MODEL \
#     --hparams_set=$HPARAMS \
#     --hparams="batch_size=$BATCH_SIZE" \
#     --output_dir=$TRAIN_DIR \
#     --train_steps=$ITERATION_SIZE \
#     --t2t_usr_dir=$USR_DIR

#   #eval steps
#   compute_bleu ${TEST[*]} $TEST_LOG
#   compute_bleu ${DEV[*]} $DEV_LOG
# done

# For troubles:
# check that problem/hparams registered with (find your mods):
# t2t-trainer --t2t_usr_dir=$USR_DIR --registry_help
# If you run out of memory, when train: add --hparams='batch_size=1024'

# compute_bleu ${TEST[*]} $TEST_LOG
# compute_bleu ${DEV[*]} $DEV_LOG

# Data loss: Checksum does not match: stored 3858684078 vs. calculated on the restored bytes 2123116135
