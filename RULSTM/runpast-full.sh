#!/usr/bin/bash

hidden=1024
epochs=100
classes=2513

for po in 1 4 15 60; do

for md in rgb flow obj; do

if [ $md = 'obj' ]; then
	feat=352
else
	feat=1024
fi

echo
date
echo "scp:$md:$hidden:$epochs:$classes:past_offset=$po"
python main.py train data/ek55 models/ek55 --task anticipation --sequence_completion --feat_in $feat --modality $md --hidden $hidden --epochs $epochs --num_class $classes --past_offset $po

echo
date
echo "training:$md:$hidden:$epochs:$classes:past_offset=$po"
python main.py train data/ek55 models/ek55 --task anticipation --feat_in $feat --modality $md --hidden $hidden --epochs $epochs --num_class $classes --past_offset $po

echo
date
echo "validation:$md:$hidden:$epochs:$classes:past_offset=$po"
python main.py validate data/ek55 models/ek55 --task anticipation --feat_in $feat --modality $md --hidden $hidden --num_class $classes --past_offset $po

echo
date
echo "done:$md:$hidden:$epochs:$classes:past_offset=$po"

done

md=fusion
feat=352

echo
date
echo "training:$md:$hidden:$epochs:$classes:past_offset=$po"
python main.py train data/ek55 models/ek55 --task anticipation --feat_in $feat --modality $md --hidden $hidden --epochs $epochs --num_class $classes --past_offset $po

echo
date
echo "validation:$md:$hidden:$epochs:$classes:past_offset=$po"
python main.py validate data/ek55 models/ek55 --task anticipation --feat_in $feat --modality $md --hidden $hidden --num_class $classes --past_offset $po

done
