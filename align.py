import os
import argparse
import sys
import json
import os
sentence_path = './test/data/sent_new'
annotation_file = './test/annotations/gold.tab'
annotation_dict = {}
output_data = []
output_dict = {}

def gather_annotations():
    with open(annotation_file) as annotation:
        rows = ( line.split('\t') for line in annotation)
        for row in rows:
            token = row[2]
            data_file_name_and_location = row[3]
            entity_type = row[5]
            mention_type = row[6]
            annotation_dict[row[1]] = row

            file_name, entity_location = data_file_name_and_location.split(':')
            start,end = entity_location.split('-')
            if file_name not in output_dict.keys():
                output_dict[file_name] = []
                with open(os.path.join(sentence_path, file_name)) as f:
                    # data = f.read().replace('\n', '')
                    data = f.read().split('\n')
                    for idx, sentence in enumerate(data):
                        data[idx] = sentence.split(' ')
                        sentence_start, sentence_end = data[idx][0].split('-')
                        data[idx][0] = (int(sentence_start),int(sentence_end))
                    for i in range(len(data)):
                        output_dict[file_name].append([])
                        output_dict[file_name][i] = {}
                        output_dict[file_name][i]['tokens'] = data[i]
                        output_dict[file_name][i]['annotations'] = []
                f.close()

            temp_dict = {}
            temp_dict['mention'] = row[2]
            temp_dict['mention_id'] = '1234'
            temp_dict['start'] = int(start)
            temp_dict['end'] = int(end)
            temp_dict['labels'] = entity_type.split(';')
            for j in range(len(output_dict[file_name])):
                if int(start) >= output_dict[file_name][j]['tokens'][0][0] and int(end) <= output_dict[file_name][j]['tokens'][0][1]:
                    mentions = temp_dict['mention'].split(' ')
                    try:
                        temp_dict['start'] = output_dict[file_name][j]['tokens'].index(mentions[0])-1
                        temp_dict['end'] = output_dict[file_name][j]['tokens'].index(mentions[-1])
                        output_dict[file_name][j]['annotations'].append(temp_dict)
                    except:
                        output_dict[file_name][j]['annotations'].append({})

                    break


            
    for key in output_dict.keys():
        for k in range(len(output_dict[key])):
            output_dict[key][k]['tokens'].pop(0)
        output_data.append(output_dict[key])
    
    with open('test_align.json', 'w') as result:
        for each in output_data:
            for sent in each:
                while len(sent['annotations'])>=1:
                    temp = sent.copy()
                    temp_annotation = sent['annotations'].pop(0)
                    temp['annotations'] = [temp_annotation]
                    json.dump(temp, result)
                    result.write('\n')

gather_annotations()


