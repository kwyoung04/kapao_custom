## copy symbolic link
ln -s /home/ubuntu/data/nia/221118 /home/ubuntu/kapao_custom/data

## create dir
cd /home/ubuntu/kapao_custom/data
mkdir raw && mv image/ raw/ && mv json/ raw/

mkdir -p annotations/train
mkdir -p annotations/val

mkdir -p images/train
mkdir -p images/val

## data
find raw/image/ -name '*.jpg' -exec cp {} images/val/ \;
find raw/image/ -name '*.jpg' -exec cp {} images/train/ \;

find raw/json/ -name '*.json' -exec cp {} annotations/val/ \;
find raw/json/ -name '*.json' -exec cp {} annotations/train/ \;

## json fusion
cd /home/ubuntu/kapao_custom/

python3 nia2coco.py -d data/221118/annotations/val/ --type val
python3 nia2coco.py -d data/221118/annotations/train/ --type train