PROBLEM=translate_he_to_en
MODEL=transformer
HPARAMS=transformer_enhe

ROOT_DATA_DIR=/media/roman/Elements/LowResourceNMT

DATA_DIR=$ROOT_DATA_DIR/data/t2t_data
TMP_DIR=$ROOT_DATA_DIR/data/t2t_datagen
TRAIN_DIR=$ROOT_DATA_DIR/data/t2t_train/$PROBLEM/$MODEL-$HPARAMS
USR_DIR=$ROOT_DATA_DIR/translate_enhe
DECODE_FILE=$DATA_DIR/he.test.txt
TEST_REFS=$DATA_DIR/en.test.txt
BEAM_SIZE=4
ALPHA=0.6

# # Generate data
T2T_DATAGEN_PATH=t2t-datagen
$T2T_DATAGEN_PATH \
  --data_dir=$DATA_DIR \
  --tmp_dir=$TMP_DIR \
  --problem=$PROBLEM \
  --t2t_usr_dir=$USR_DIR

# # Train data
t2t-trainer \
  --data_dir=$DATA_DIR \
  --problems=$PROBLEM \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --output_dir=$TRAIN_DIR \
  --t2t_usr_dir=$USR_DIR

# # Evaluate data
t2t-decoder \
  --data_dir=$DATA_DIR \
  --problems=$PROBLEM \
  --model=$MODEL \
  --hparams_set=$HPARAMS \
  --output_dir=$TRAIN_DIR \
  --decode_hparams="beam_size=$BEAM_SIZE,alpha=$ALPHA" \
  --decode_from_file=$DECODE_FILE \
  --decode_to_file=$DATA_DIR/translit.he \
  --t2t_usr_dir=$USR_DIR
t2t-bleu --translation=$DATA_DIR/translit.he --reference=$TEST_REFS


# For troubles:
# check that problem/hparams registered with (find your mods):
# t2t-trainer --t2t_usr_dir=$USR_DIR --registry_help
# If you run out of memory, when train: add --hparams='batch_size=1024'