import gzip
import csv
import tarfile
import os
import ntpath
import numpy as np
import codecs
import shutil

def main():

    # FIRST STEPS
    # Improvement: download directly from website -> TCGA tools
    src_path = r"C:\Users\Sherry Wang\Documents\GitHub\CancerSubtypeClassification\unprocessed_data\gdc_download_20191206_062707.563269.tar.gz"
    dest_path = r"C:\Users\Sherry Wang\Documents\GitHub\CancerSubtypeClassification\unprocessed_data"
    # extractTarGZ(src_path, dest_path)
    newDir = r"C:\Users\Sherry Wang\Documents\GitHub\CancerSubtypeClassification\data"
    # moveFiles(dest_path, newDir)
    #TODO REMOVE ANNOTATIONS^ ?
    fname = r"C:\Users\Sherry Wang\Documents\GitHub\CancerSubtypeClassification\data"
    createDataset(fname)

# extract zipped folder containing all files from TCGA
def extractTarGZ(src_path, dest_path):
    tar = tarfile.open(src_path)
    tar.extractall(dest_path)
    tar.close()

def createDataset(path):
    new = []
    arr = []
    final = []

    filesList = os.listdir(path)
    print(filesList)
    # count = 0
    for x in filesList:
        # skip over files that don't actually provide data
        if (x == "MANIFEST.txt" or x == "annotations.txt"):
            continue
        count += 1
        # to ensure the base directory is not visited
        if count == 1:
            continue

        fpath = path + "//"+ x
        with gzip.open(fpath, 'r') as f:
        # k = r.read().decode('utf-8')
            arr = []
            for line in f:
                l = line.decode('utf-8')
                arr.append(l.split('\t'))
                # print(arr)
            new = [[x,y.replace('\n','')] for x,y in arr]
            arr = np.array(new)
            arr.transpose()
            # print(genes)
            # print(values)
            # print()
            # n = k.split('\n')
            # n = n.split('\t')
            # new = [[x,y] for x,y in zip(n[0::2], n[1::2])]

    print(np.array(new))
    return np.array(new)

def logarithm_transform_filter(arr):
    tarr = np.log10(arr)
    return tarr



def moveFiles(dir, newDir):

    # move manifest file over to data folder
    manifest_path = dir + "//MANIFEST.txt"
    new_manifest_path = newDir + "//MANIFEST.txt"
    if not os.path.exists(new_manifest_path):
        os.rename(manifest_path, new_manifest_path)

    # get all subdirectories of dir
    folders = [x[0] for x in os.walk(dir)]
    count = 0
    for x in folders:
        count += 1
        # to ensure the base directory is not visited
        if count == 1:
            continue
        # get all the files within the subdirectory (includes gene quantification file and annotations)
        dirs = os.listdir(x)
        # print(dirs)
        # move over all gene quantification files within subdirectories to one directory
        for fname in dirs:
            prevFilePath =  x+ '\\' + fname
            print(prevFilePath)
            newFilePath = newDir + "\\" + fname
            print(newFilePath)
            if not os.path.exists(newFilePath):
                os.rename(prevFilePath, newFilePath)

    # remove dir
    shutil.rmtree(dir)

def preprocess(path):

    extractTarGZ(path)
    # oldDir = r"C:\Users\Sherry Wang\Documents\GitHub\CancerSubtypeClassification\unprocessed_data"
    # newDir = r"C:\Users\Sherry Wang\Documents\GitHub\CancerSubtypeClassification\data"
    # moveFiles(oldDir, newDir)

    # with open(path) as m:
    #     reader = csv.reader(m, delimiter='\t')
    #     count = 0
    #     for row in reader:
    #         count += 1
    #         if (count == 1):
    #             continue
    #         print(row[1])
    #         with gzip.open(fname) as f:
    #             print(f.read())

    # files = os.listdir(path)
    #
    # for x in files:
    #     filePath = "C://Users//Sherry Wang//Documents//GitHub//CancerSubtypeClassification//TCGA_GBM_data//" + x
    #     # print(filePath)
    #     extractGZIP(filePath)
    #     # print("next")
    #     # break

if __name__ == '__main__':
    main()
