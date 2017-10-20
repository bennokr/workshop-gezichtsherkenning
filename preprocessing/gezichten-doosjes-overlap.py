import itertools
import csv

def overlap(face, box):
    f_x1, f_y1, f_x2, f_y2 = face
    b_x1, b_y1, b_x2, b_y2 = box
    if ~((f_x1 > b_x2)
        | (f_x2 < b_x1)
        | (f_y1 > b_y2)
        | (f_y2 < b_y1)):
        return max(0, min(f_x2, b_x2) - max(f_x1, b_x1)) * max(0, min(f_y2, b_y2) - max(f_y1, b_y1))
    else:
        return 0
                

if __name__ == '__main__':
    import sys
    try:
        _, mediatags, mediatags_mediafiles, mediatagrectangles, faces = sys.argv
    except Exception as e:
        print('Usage: python3 gezichten-opslaan.py <mediatags> <mediatags_mediafiles> <mediatagrectangles> <faces>\n')
        raise e
        
    
    with open(mediatags, 'rb') as fh:
        tag_names = {row['id']:row['name'] for row in csv.DictReader(l.decode('utf8') for l in fh)}

    with open(mediatags_mediafiles, 'rb') as fh:
        tag_tag = {row['id']:row['mediatag_id'] for row in csv.DictReader(l.decode('utf8') for l in fh)}

    tag_doosjes = {}
    with open(mediatagrectangles, 'rb') as fh:
        for row in csv.DictReader(l.decode('utf8') for l in fh):
            doosje = tuple(map(int, (row['x1'],row['y1'],row['x2'],row['y2'])))
            tag = tag_tag.get( row['mediatag_id'], None )
            tag_doosjes.setdefault(row['mediafile_id'], []).append( (doosje, tag) )
    
    with open(faces) as fh:
        for line in fh:
            collection_id, mediafile_id, x1,y1, x2,y2 = line.strip().split('\t')
            face = tuple(map(int, (x1,y1, x2,y2)))
            tag_scores = []
            for box, tag in tag_doosjes.get(mediafile_id, []):
                tag_scores.append( (tag, overlap(face, box)) )
            best_tag = max(tag_scores, default=None, key=lambda x:x[1])
            if best_tag:
                best_tag = best_tag[0]
                print(collection_id, mediafile_id, tag_names[best_tag], x1,y1, x2,y2, sep='\t')
            
            
            