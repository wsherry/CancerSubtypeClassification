import gzip
import csv
import tarfile
import os
import ntpath
import numpy as np
import codecs
import shutil
import pandas as pd

def main():

    # FIRST STEPS
    # Improvement: download directly from website -> TCGA tools
    # src_path = r"C:\Users\Sherry Wang\Documents\GitHub\CancerSubtypeClassification\unprocessed_data\gdc_download_20191206_062707.563269.tar.gz"
    # dest_path = r"C:\Users\Sherry Wang\Documents\GitHub\CancerSubtypeClassification\unprocessed_data"
    # extractTarGZ(src_path, dest_path)
    # newDir = r"C:\Users\Sherry Wang\Documents\GitHub\CancerSubtypeClassification\data"
    # moveFiles(dest_path, newDir)
    # TODO REMOVE ANNOTATIONS file^ ?
    path = r"C:\Users\Sherry Wang\Documents\GitHub\CancerSubtypeClassification\unprocessed_data"
    x, y = createDataset(path)
    

# extract zipped folder containing all files from TCGA
def extractTarGZ(src_path, dest_path):
    tar = tarfile.open(src_path)
    tar.extractall(dest_path)
    tar.close()

def checkGenesSame(header, header_verify):

    if len(header) != len(header_verify):
        return False
    for x in range(0,len(header)):
        if header[x] != header_verify[x]:
            return False
    
    return True

def createDataset(path):
    sample = []
    data = []
    # variables for verification
    # header = []

    ################################################################################################
    files_uuids = []
    gene_headers = []
    # move manifest file over to data folder
    # manifest_path = dir + "//MANIFEST.txt"
    
    # get all subdirectories of dir
    folders = [x[0] for x in os.walk(path)]
    count = 0
    for x in folders:
        count += 1
        # to ensure the base directory is not visited
        if count == 1:
            continue
        # get all the files within the subdirectory (includes gene quantification file and annotations)
        dirs = os.listdir(x)
        print(dirs)
        # move over all gene quantification files within subdirectories to one directory
        for fname in dirs:
            print(fname)
            if (fname == "annotations.txt"):
                continue
            
            # save file containing gene quantification data
            fpath =  x+ '\\' + fname
            print(fpath)
            print("DIRNAME")
            print(os.path.basename(x))
            files_uuids.append([os.path.basename(x)])

            with gzip.open(fpath, 'r') as f:
                sample = []
                for line in f:
                    l = line.decode('utf-8')
                    sample.append(l.split('\t'))
                # print(sample)
                if (count == 2):
                    gene_headers = [x[0] for x in sample]
                sample = [x[1].replace('\n','') for x in sample]
                # # for verification purposes
                # genes = [x[0] for x in arr]
                # isSame = checkGenesSame(header, genes)
                # if (!isSame):
                #     continue              
            data.append(sample)
    
    files_uuids = pd.DataFrame(files_uuids, columns=['file_id'])
    subtype_data = pd.read_csv('gbm_subtype_data.csv')
    merged_data = pd.merge(files_uuids, subtype_data, on="file_id")
    label = merged_data['subtype'].to_numpy()
    print(data)
    print(label)
    return data, label

            




    #####################################################################################
    
    # filesList = os.listdir(path)
    # # print(filesList)
    # count = 0
    # for x in filesList:
    #     # skip over files that don't actually provide data
    #     if (x == "MANIFEST.txt" or x == "annotations.txt"):
    #         continue
    #     count += 1
    #     # to ensure the base directory is not visited
    #     if count == 1:
    #         continue

    #     fpath = path + "//"+ x
    #     with gzip.open(fpath, 'r') as f:
    #         sample = []
    #         for line in f:
    #             l = line.decode('utf-8')
    #             sample.append(l.split('\t'))
    #         # print(sample)
    #         # add first header to dataset
    #         if count == 2:
    #             header = [x[0] for x in sample]
    #             data.append(header)                
    #         sample = [x[1].replace('\n','') for x in sample]
    #         # # for verification purposes
    #         # genes = [x[0] for x in arr]
    #         # isSame = checkGenesSame(header, genes)
    #         # if (!isSame):
    #         #     continue              
    #     data.append(sample)
    # # print(data)
    return np.array(data)

def logarithm_transform_filter(dataset):
    header = dataset[0:1]
    print(header)
    print(dataset[1])
    print(dataset[2])
    transformed_dataset = np.log10(dataset[1:])
    complete_dataset = header.append(transformed_dataset)
    return complete_dataset

# filter out genes with average of less than 5.0 and
# a variance less than 1.0
def filter_dataset(dataset):
    # take average & variance of columns (values of all samples over one gene)
    sample_data = dataset[1:]
    avg = np.mean(sample_data , axis = 0)
    var = np.var(sample_data , axis = 0)
    n_samples = len(sample_data)
    indices = []

    for i in range(0, n_samples):
        if(avg[i] < 5 or var[i]<1):
            indices.append(i)
    fltr_dataset = np.delete(sample_data, indices, axis=0)
    data = np.delete(dataset[0:1], indices)
    data.append(fltr_dataset)
    return data


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
