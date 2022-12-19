## copy symbolic link
ln -s /home/ubuntu/data/nia/221118 /home/ubuntu/kapao_custom/data

## create dir
cd /home/ubuntu/kapao_custom/data

mkdir -p annotations/train2017
mkdir -p annotations/val

mkdir -p images/train
mkdir -p images/val

## data
find 06.품질검증 -name '*.jpg' -exec cp {} images/val/ \;
find 06.품질검증 -name '*.jpg' -exec cp {} images/train/ \;

find 06.품질검증 -name '*.json' -exec cp {} annotations/val/ \;
find 06.품질검증 -name '*.json' -exec cp {} annotations/train/ \;

## json fusion
cd /home/ubuntu/kapao_custom/

python3 nia2coco.py -d data/datasets/221216/annotations/val --type val
python3 nia2coco.py -d data/datasets/221216/annotations/train/ --type train