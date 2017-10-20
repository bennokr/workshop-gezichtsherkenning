from scipy.ndimage import imread
from scipy.misc import imsave
from skimage.transform import resize

if __name__ == '__main__':
    import sys
    try:
        _, taggedfaces, input_dir, output_dir = sys.argv
    except Exception as e:
        print('Usage: python3 gezichten-opslaan.py <taggedfaces> <input-dir> <output-dir>\n')
        raise e
    
    with open(taggedfaces) as fh:
        for line in fh:
            collection, mediafile, x1,y1, x2,y2 = line.strip().split('\t')
            

    with open(taggedfaces, 'rb') as fh:
        for line in (l.decode('utf8') for l in fh):
            collection, mediafile, tag, x1,y1, x2,y2 = line.strip().split('\t')
            x1,y1, x2,y2 = tuple(map(int, (x1,y1, x2,y2)))
            
            fpath = os.path.join(input_dir, collection, 'normal', mediafile)
            im = imread(fpath, flatten=True)
            face = im[y1:y2, x1:x2]

            face = resize(face / 256, (100,100))

            tag = tag.encode('utf8', errors='ignore').decode('ascii', errors='ignore')
            os.makedirs(os.path.join(output_dir, tag), exist_ok=True)
            fout = os.path.join(output_dir, tag, mediafile + '.png')
            imsave(fout, face)


