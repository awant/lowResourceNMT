# 1) download he-en data to DATA_DIR path (should exists: DATA_DIR/en.train.txt, DATA_DIR/he.train.txt for training)
# 2) set TRAIN_SIZE (in 1000, for example: 236 means 236k. 236 is about 80% of all dataset, set TRAIN_SIZE <= 236 or change test/dev sizes)
# 3) run this script

TRAIN_SIZE=236
TEST_SIZE=29
DEV_SIZE=29

PROBLEM=translate_he_to_en
MODEL=transformer
HPARAMS=transformer_enhe
BATCH_SIZE=4096

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DATA_DIR=$SCRIPT_DIR/..
DATA_DIR=$ROOT_DATA_DIR/data/t2t_data
TMP_DIR=$ROOT_DATA_DIR/data/t2t_datagen
TRAIN_DIR=$ROOT_DATA_DIR/data/t2t_train/$PROBLEM/$MODEL-$HPARAMS
USR_DIR=$ROOT_DATA_DIR/translate_enhe
BEAM_SIZE=4
ALPHA=0.6
TRAIN_STEPS=10
ITERATION_SIZE=1000
OTHER_PARAMS=""
DATAGEN=0
MOVE_MODEL=0

while [ -n "$1" ]
do
case "$1" in
--train_size) TRAIN_SIZE=$2
shift;;
--test_size) TEST_SIZE=$2
shift;;
--dev_size) DEV_SIZE=$2
shift;;

--model) MODEL=$2
shift;;
--problem) PROBLEM=$2
shift;;
--hparams) HPARAMS=$2
shift;;

--batch_size) BATCH_SIZE=$2
shift;;
--train_steps) TRAIN_STEPS=$2
shift;;
--iteration_size) ITERATION_SIZE=$2
shift;;
--other_params) OTHER_PARAMS=$2
shift;;


--data_dir) DATA_DIR=$2
shift;;
--usr_dir) USR_DIR=$2
shift;;

--beam_size) BEAM_SIZE=$2
shift;;

--alpha) ALPHA=$2
shift;;

--update_data) DATAGEN=1;;


--update_model) MOVE_MODEL=1;;

--new) DATAGEN=1
MOVE_MODEL=1;;

--epoch) TRAIN_STEPS=$2
let "ITERATION_SIZE = ($TRAIN_SIZE * 1000 + $BATCH_SIZE - 1) / $BATCH_SIZE";;

*) echo "$1 unknown option"
exit;;
esac
shift
done

if [ ! -f $DATA_DIR/he.train.txt ] || [ ! -f $DATA_DIR/en.train.txt ]; then
    echo "Train data doesn't exist!"
    exit
fi
# Split train-dev-test data, train/dev/test in k: 10k means 10000
if [[ $UPDATE_DATA -eq 1 ]]; then

    python3 $ROOT_DATA_DIR/scripts/make_small_datasets.py --datadir=$DATA_DIR --train_size=$TRAIN_SIZE --test_size=$TEST_SIZE --dev_size=$DEV_SIZE
    cp $DATA_DIR/en.test.txt $ROOT_DATA_DIR/data/t2t_data-${TRAIN_SIZE}k/en_old.test.txt
    cp $DATA_DIR/he.test.txt $ROOT_DATA_DIR/data/t2t_data-${TRAIN_SIZE}k/he_old.test.txt
    cp $DATA_DIR/en.dev.txt $ROOT_DATA_DIR/data/t2t_data-${TRAIN_SIZE}k/en_old.dev.txt
    cp $DATA_DIR/he.dev.txt $ROOT_DATA_DIR/data/t2t_data-${TRAIN_SIZE}k/he_old.dev.txt

    DATA_DIR=$ROOT_DATA_DIR/data/t2t_data-${TRAIN_SIZE}k
    DECODE_FILE=$DATA_DIR/he.test.txt
    TEST_REFS=$DATA_DIR/en.test.txt # several refs can be separated by tabs
    OLD_TEST=($DATA_DIR/en_old.test.txt $DATA_DIR/he_old.test.txt)
    OLD_DEV_EN=$DATA_DIR/en_old.dev.txt
    OLD_DEV_HE=$DATA_DIR/he_old.dev.txt
    # Generate data
    T2T_DATAGEN_PATH=t2t-datagen
    $T2T_DATAGEN_PATH \
      --data_dir=$DATA_DIR \
      --tmp_dir=$TMP_DIR \
      --problem=$PROBLEM \
      --t2t_usr_dir=$USR_DIR
        
fi
STAMP=$(date  "+_%Y_%m_%d_%H_%M_%S")
if [[ $MOVE_MODEL -eq 1 ]]; then 
    echo "MOVING MODE FROM $TRAIN_DIR"  
    if [[ -d $TRAIN_DIR ]]; then 
      mv $TRAIN_DIR "$TRAIN_DIR$STAMP"
      echo "MODEL MOVED"
    fi
fi
DATA_DIR=$ROOT_DATA_DIR/data/t2t_data-${TRAIN_SIZE}k
DECODE_FILE=$DATA_DIR/he.test.txt
TEST_REFS=$DATA_DIR/en.test.txt # several refs can be separated by tabs
DEV=($DATA_DIR/en.dev.txt $DATA_DIR/he.dev.txt)
TEST=($DATA_DIR/en.test.txt $DATA_DIR/he.test.txt)
OLD_TEST=($DATA_DIR/en_old.test.txt $DATA_DIR/he_old.test.txt)
OLD_DEV=($DATA_DIR/en_old.dev.txt $DATA_DIR/he_old.dev.txt)


compute_bleu() {
  t2t-decoder \
    --data_dir=$DATA_DIR \
    --problems=$PROBLEM \
    --model=$MODEL \
    --hparams_set=$HPARAMS \
    --output_dir=$TRAIN_DIR \
    --decode_hparams="beam_size=$BEAM_SIZE,alpha=$ALPHA" \
    --decode_from_file=$2 \
    --decode_to_file=$DATA_DIR/he-to-en.translit.txt \
    --t2t_usr_dir=$USR_DIR
  python3 $ROOT_DATA_DIR/scripts/compute_bleu.py --translation=$DATA_DIR/he-to-en.translit.txt --reference=$1 >> $3
  echo $1
  echo $2
  echo $3
}

TEST_LOG=$TRAIN_DIR/test_log.txt
DEV_LOG=$TRAIN_DIR/dev_log.txt
OLD_TEST_LOG=$TRAIN_DIR/old_test_log.txt
OLD_DEV_LOG=$TRAIN_DIR/old_dev_log.txt
for i in $TEST_LOG $DEV_LOG $OLD_DEV_LOG $OLD_TEST_LOG
do 
  echo $i
  if [[ -f $i ]]; then
    echo "EXIST $i"
    mv $i $i$STAMP
  fi
done
mkdir $TRAIN_DIR
for ((i=1;i<=$TRAIN_STEPS;i++)); do
  echo $(($i * $ITERATION_SIZE));
  #train step
  t2t-trainer \
    --data_dir=$DATA_DIR \
    --problems=$PROBLEM \
    --model=$MODEL \
    --hparams_set=$HPARAMS \
    --hparams="batch_size=$BATCH_SIZE $OTHER_PARAMS" \
    --output_dir=$TRAIN_DIR \
    --train_steps=$ITERATION_SIZE     \
    --t2t_usr_dir=$USR_DIR

  
  #eval steps
  compute_bleu ${TEST[*]} $TEST_LOG
  compute_bleu ${DEV[*]} $DEV_LOG
  compute_bleu ${OLD_TEST[*]} $OLD_TEST_LOG
  compute_bleu ${OLD_DEV[*]} $OLD_DEV_LOG  
  python3  $TRAIN_DIR/plot.png $TEST_LOG $DEV_LOG $OLD_TEST_LOG $OLD_DEV_LOG
done 

# For troubles:
# check that problem/hparams registered with (find your mods):
# t2t-trainer --t2t_usr_dir=$USR_DIR --registry_help
# If you run out of memory, when train: add --hparams='batch_size=1024'
