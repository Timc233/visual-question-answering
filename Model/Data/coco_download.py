import os
import urllib
import wget
import zipfile


class DataDownloader:

    def __init__(self) -> None:
        self.data_folder = './Data/COCO'

    def download_all(self) -> None:
        self.download_train()
        self.download_val()
        self.download_test()

    
    def download_train(self) -> None:
        train_folder = os.path.join(self.data_folder + 'train')
        train_data_url = 'http://images.cocodataset.org/zips/train2014.zip'
        train_data_path = os.path.join(train_folder, 'train2014.zip')
        wget.download(train_data_url, out=train_data_path)
        print('training data downloaded at ' + train_data_path)
        with zipfile.ZipFile(train_data_path) as train_zip:
            train_zip.extractall(path=train_folder)
            print('Training data extracted to' + train_folder)

    def download_val(self) -> None:
        val_folder = os.path.join(self.data_folder + 'val')
        val_data_url = 'http://images.cocodataset.org/zips/val2014.zip'
        val_data_path = os.path.join(val_folder, 'val2014.zip')
        wget.download(val_data_url, out=val_data_path)
        with zipfile.ZipFile(val_data_path) as val_zip:
            val_zip.extractall(path=val_folder)

    
    def download_test(self) -> None:
        test_folder = os.path.join(self.data_folder, 'test')
        test_data_url = 'http://images.cocodataset.org/zips/test2015.zip'
        test_data_path = os.path.join(test_folder, 'test2015.zip')
        wget.download(test_data_url, test_data_path)
        with zipfile.ZipFile(test_data_path) as test_zip:
            test_zip.extractall(path=test_folder)
