import sys
import os
import json
import argparse

from pathlib import Path

from pycocotools.coco import COCO

def cheak_abs_name(name_list):
    for part_name in name_list:
        if (part_name >= '0' and part_name <= '9999999' and len(part_name) == 7):
          return part_name

    return 0


class custom_dataset:
    def __init__(self, info, licenses):
        self.cocoFormat = {'info': info, 'licenses': licenses, 'images': [], 'annotations': [], 'categories': []}
        self.categorieFlag = 1
        
        self.id_cnt = 1

    def invisible_data(self, inKey):
        pairName = {'images': 'images', 'categories': 'Categories', 'annotations': 'annotations'}
        for val in pairName.values():
            if val in inKey:
                continue
            else:
                print("error 0")
                exit()

    def count_keypoint(self, keypoints):
        cnt = 0
        i = 2
        while i < 50:
            if keypoints[i] == 0:
                cnt = cnt + 1
            i = i+3   

        return 17 - cnt

    def calc_area(self,bbox):
        return abs((bbox[2] - bbox[0]) * (bbox[3] - bbox[1]))

    def set_coco_format(self, data):

        
        image = dict()        
        for imagesData in data['images']:
            image['license'] = 0
            image['file_name'] = imagesData['file_name']
            image['coco_url'] = "NULL"
            image['height'] = imagesData['height']
            image['width'] = imagesData['width']
            #image['date_captured'] = imagesData['date_created']
            image['flickr_url'] = "NULL"
            #image['id'] = imagesData['id']
            image['id'] = int(cheak_abs_name(imagesData['file_name'].split('_')))
            self.cocoFormat['images'].append(image)
        
        annotation = dict()
        for annotations in data['annotations']:
            #if annotations['category_id'] != 1 or len(annotations['keypoints']) == 0:
            if len(annotations['keypoints']) == 0:
                continue
            #annotation['segmentation'] = 0
            annotation['num_keypoints'] = self.count_keypoint(annotations['keypoints'])
            annotation['area'] = self.calc_area(annotations['bbox'])
            annotation['iscrowd'] = 0
            for i in range(17):
                vible = annotations['keypoints'][i*3+2]
                if vible == 0:
                    continue
                annotations['keypoints'][i*3+2] = vible -1 
            annotation['keypoints'] = annotations['keypoints']
            #annotation['image_id'] = annotations['image_id']
            annotation['image_id'] = int(cheak_abs_name(imagesData['file_name'].split('_')))
            annotation['bbox'] = annotations['bbox']
            annotation['category_id'] = annotations['category_id']
            annotation['id'] = self.id_cnt
            self.cocoFormat['annotations'].append(annotation)
            self.id_cnt = self.id_cnt + 1

        if self.categorieFlag:
            categorie = dict()
            categorie['supercategory'] = data['Categories'][0]['supercategory']
            categorie['id'] = data['Categories'][0]['id']
            categorie['name'] = data['Categories'][0]['name']
            categorie['keypoints'] = data['Categories'][0]['keypoints']
            categorie['skeleton'] = data['Categories'][0]['skeleton']
            self.cocoFormat['categories'].append(categorie)
            self.categorieFlag = 0

    def push_json(self, jsonFile):
        with open(jsonFile, 'rt', encoding='UTF-8-sig') as file:
            data = json.load(file)
            assert type(data)==dict, 'annotation file format {} not supported'.format(type(data))
           
            #self.invisible_data(data.keys())
            self.set_coco_format(data)
        
    def compare_jpg_json(self):
        pass

    def save_json(self, abspath):
        filePath = abspath + "/../" + "person_keypoints_2017.json"
        #filePath = "/home/ubuntu/koreaData/kapao_custom/data/datasets/test/annotations" + "/" + "person_keypoints_val2017.json"
        with open(filePath, 'w') as outfile:
            json.dump(self.cocoFormat, outfile)

    def createIndex(self): # in coco
        # create index
        print('creating index...')
        anns, cats, imgs = {}, {}, {}
        imgToAnns,catToImgs = defaultdict(list),defaultdict(list)
        if 'annotations' in self.dataset:
            for ann in self.dataset['annotations']:
                imgToAnns[ann['image_id']].append(ann)
                anns[ann['id']] = ann

        if 'images' in self.dataset:
            for img in self.dataset['images']:
                imgs[img['id']] = img

        if 'categories' in self.dataset:
            for cat in self.dataset['categories']:
                cats[cat['id']] = cat

        if 'annotations' in self.dataset and 'categories' in self.dataset:
            for ann in self.dataset['annotations']:
                catToImgs[ann['category_id']].append(ann['image_id'])

        print('index created!')

        # create class members
        self.anns = anns
        self.imgToAnns = imgToAnns
        self.catToImgs = catToImgs
        self.imgs = imgs
        self.cats = cats




def get_json():
    pass

def find_jsonSet(path):
    jsonList=[]
    
    for dirpath, dirname, filename in os.walk(path, topdown=False):
        aliveSet = ['json']
        jsonList.extend([dirpath+'/'+i for i in filename if i[-4:] in aliveSet])

    return jsonList



if __name__ == '__main__':
    print("### Change NIA Format to COCO Format")
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', dest='datasetDir', default='data/datasets/test/annotations/train/', help='path to directory')

    args = parser.parse_args()

    basename = os.path.basename(args.datasetDir)
    abspath = os.path.abspath(args.datasetDir)
    
    
    info = dict()
    info["description"] = "NIA korea Dataset"
    info["url"] = "https://aihub.or.kr/"
    info["version"] = "1.0"
    info["year"] =  2022
    info["contributor"] = "COCO Consortium"
    info["date_created"] = "2022/09/01"


    jsonList = find_jsonSet(abspath)
    
    coco_keypoint = custom_dataset(info,'licenses')
    
    for file in jsonList:
        coco_keypoint.push_json(file)

    #coco_keypoint.compare_jpg_json()
    coco_keypoint.save_json(abspath)


    
    print("### Conversion complete")
    