
import os
import argparse
import sys
import json
import os

from matplotlib import test
# sentence_path = './test/data/sent_new'
annotation_file = './test/annotations/gold.tab'
myprediction_file = './full_prediction.json'
out_file = './test/annotations/predictions.tab'
test_file = './11.2_test.json'

with open(annotation_file,'r') as template, open(myprediction_file,'r') as prediction, open(out_file,'w') as output, open(test_file,'r') as text:
    rows = [line.split('\t') for line in template]
    i = 0
    predictions = list(json.load(prediction).values())
    for idx, line in enumerate(text):
        mention = json.loads(line)['annotations'][0]["mention"]         
        while i<len(rows) and rows[i][2] != mention:
            i += 1
            rows[i][5] = 'ORG'
        rows[i][5] = ';'.join(predictions[idx])
        
    for row in rows:
        output.write('\t'.join(row))
    

        


    




