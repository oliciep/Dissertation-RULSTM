echo %TIME%
python main.py train data/ek55 models/ek55 --task anticipation --modality rgb --feat_in 1024 --hidden 128 --epochs 10 --num_class 234 --sequence_completion --meter loss
echo %TIME%