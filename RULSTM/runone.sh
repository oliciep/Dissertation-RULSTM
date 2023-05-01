#!/usr/bin/bash

modality=rgb
hidden=256
epochs=100
classes=234

echo
date
echo "SCP:$modality:$hidden:$epochs:$classes"
python main.py train data/ek55 models/ek55 --task anticipation --sequence_completion --feat_in 1024 --modality $modality --hidden $hidden --epochs $epochs --num_class $classes

echo
date
echo "training:$modality:$hidden:$epochs:$classes"
python main.py train data/ek55 models/ek55 --task anticipation --feat_in 1024 --modality $modality --hidden $hidden --epochs $epochs --num_class $classes

echo
date
echo "validation:$modality:$hidden:$epochs:$classes"
python main.py validate data/ek55 models/ek55 --task anticipation --feat_in 1024 --modality $modality --hidden $hidden --num_class $classes

echo
date
echo "done:$modality:$hidden:$epochs:$classes"
