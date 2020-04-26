basedir = '/home/aniruddha/Dropbox/Openedsdata2020/openEDS2020-SparseSegmentation/participant/'

image_paths = open(basedir+'/images.txt').read().split()
label_paths = open(basedir+'/labels.txt').read().split()

labelled_image_paths = []

labelled_image_dict = {}

for lbl in label_paths:
    folder, label_file = lbl.split('/')
    image_file = label_file[6:-4]
    image_path = '/'.join([folder,image_file]) + '.png'
    
    if image_path not in image_paths: 
        print('Error! We seem to have made a wrong image path: ', image_path)
    
    labelled_image_paths.append(image_path)

unlabelled_image_paths = list(set(image_paths).difference(set(labelled_image_paths)))
