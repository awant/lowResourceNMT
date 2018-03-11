# 1) download he-en data to DATA_DIR path (should exists: DATA_DIR/en.train.txt, DATA_DIR/en.test.txt for training)
# 2) set TRAIN_SIZE (in 1000, for example: 236 means 236k. 236 is about 80% of all dataset, set TRAIN_SIZE <= 236 or change test/dev sizes)
# 3) run this script

TRAIN_SIZE=236

PROBLEM=translate_he_to_en
MODEL=transformer
HPARAMS=transformer_enhe

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
ROOT_DATA_DIR=$SCRIPT_DIR/..

DATA_DIR=$ROOT_DATA_DIR/data/t2t_data
TMP_DIR=$ROOT_DATA_DIR/data/t2t_datagen
TRAIN_DIR=$ROOT_DATA_DIR/data/t2t_train/$PROBLEM/$MODEL-$HPARAMS
USR_DIR=$ROOT_DATA_DIR/translate_enhe
BEAM_SIZE=4
ALPHA=0.6

if [ ! -f $DATA_DIR/he.train.txt ] || [ ! -f $DATA_DIR/en.train.txt ]; then
    echo "Train data doesn't exist!"
    exit
fi

# Split train-dev-test data, train/dev/test in k: 10k means 10000
python3 $ROOT_DATA_DIR/scripts/make_small_datasets.py --datadir=$DATA_DIR --train_size=$TRAIN_SIZE --test_size=29 --dev_size=29

DATA_DIR=$ROOT_DATA_DIR/data/t2t_data-${TRAIN_SIZE}k
DECODE_FILE=$DATA_DIR/he.test.txt
TEST_REFS=$DATA_DIR/en.test.txt # several refs can be separated by tabs

# Generate data
T2T_DATAGEN_PATH=t2t-datagen
$T2T_DATAGEN_PATH \
  --data_dir=$DATA_DIR \
  --tmp_dir=$TMP_DIR \
  --problem=$PROBLEM \
  --t2t_usr_dir=$USR_DIR

# Train data
t2t-trainer \
  --data_dir=$DATA_DIR \
  --problems=$PROBLEM \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --output_dir=$TRAIN_DIR \
  --train_steps=10000 \
  --t2t_usr_dir=$USR_DIR

# Compute transliterations
t2t-decoder \
  --data_dir=$DATA_DIR \
  --problems=$PROBLEM \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --output_dir=$TRAIN_DIR \
  --decode_hparams="beam_size=$BEAM_SIZE,alpha=$ALPHA" \
  --decode_from_file=$DECODE_FILE \
  --decode_to_file=$DATA_DIR/he-to-en.translit.txt \
  --t2t_usr_dir=$USR_DIR

# Compute bleu
python3 $ROOT_DATA_DIR/scripts/compute_bleu.py --translation=$DATA_DIR/he-to-en.translit.txt --reference=$TEST_REFS

# For troubles:
# check that problem/hparams registered with (find your mods):
# t2t-trainer --t2t_usr_dir=$USR_DIR --registry_help
# If you run out of memory, when train: add --hparams='batch_size=1024'

