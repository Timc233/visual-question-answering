import os
import urllib
import wget
import zipfile


class DataDownloader:

    def __init__(self) -> None:
        if not os.path.exists('./Data/COCO'):
            os.makedirs('./Data/COCO/train')
            os.makedirs('./Data/COCO/val')
            os.makedirs('./Data/COCO/test')

    def download_all(self) -> None:
        self.download_train()
        self.download_val()
        self.download_test()

    
    def download_train(self) -> None:
        train_data_url = 'http://images.cocodataset.org/zips/train2014.zip'
        train_data_path = './Data/COCO/train2014.zip'
        wget.download(train_data_url, out=train_data_path)
        with zipfile.ZipFile(train_data_path) as train_zip:
            train_zip.extractall(path='./Data/COCO/train')

    def download_val(self) -> None:
        val_data_url = 'http://images.cocodataset.org/zips/val2014.zip'
        val_data_path = './Data/COCO/val2014.zip'
        wget.download(val_data_url, out=val_data_path)
        with zipfile.ZipFile(val_data_path) as val_zip:
            val_zip.extractall(path='./Data/COCO/val')

    
    def download_test(self) -> None:
        test_data_url = 'http://images.cocodataset.org/zips/test2015.zip'
        test_data_path = './Data/COCO/test2015.zip'
        wget.download(test_data_url, test_data_path)
        with zipfile.ZipFile(test_data_path)as test_zip:
            test_zip.extractall(path='./Data/COCO/test')
