import os
import wget
import zipfile
import urllib



class DataDownloader:

    # TODO Put every link in init
    # TODO check file integrity
    # TODO download after interrupted




    def __init__(self, data_folder) -> None:
        cwd = os.getcwd()
        # self.data_folder = os.path.join(cwd, 'Data/COCO')
        self.data_folder = data_folder
        print('COCO folder is at ' + self.data_folder)

    def download_all(self) -> None:
        self.download_annotations()
        self.download_questions()
        self.download_images()

    def download_images(self) -> None:
        train_image_url = 'http://images.cocodataset.org/zips/train2014.zip'
        val_image_url = 'http://images.cocodataset.org/zips/val2014.zip'
        test_image_url = 'http://images.cocodataset.org/zips/test2015.zip'

        image_folder = os.path.join(self.data_folder, 'image')
        train_folder = os.path.join(image_folder, 'train')
        val_folder = os.path.join(image_folder, 'val')
        test_folder = os.path.join(image_folder, 'test')

        self.download(train_image_url, train_folder)
        self.download(val_image_url, val_folder)
        self.download(test_image_url, test_folder)
    
    def download_train(self) -> None:
        train_folder = os.path.join(self.data_folder, 'train')
        if not os.path.exists(train_folder):
            os.makedirs(train_folder)
        train_data_url = 'http://images.cocodataset.org/zips/train2014.zip'
        train_data_path = os.path.join(train_folder, 'train2014.zip')
        print('Training data path is at ' + train_data_path)
        wget.download(train_data_url, out=train_data_path)
        print('training data downloaded at ' + train_data_path)
        with zipfile.ZipFile(train_data_path) as train_zip:
            train_zip.extractall(path=train_folder)
            print('Training data extracted to' + train_folder)

    def download_val(self) -> None:
        val_folder = os.path.join(self.data_folder, 'val')
        if not os.path.exists(val_folder):
            os.makedirs(val_folder)
        val_data_url = 'http://images.cocodataset.org/zips/val2014.zip'
        val_data_path = os.path.join(val_folder, 'val2014.zip')
        wget.download(val_data_url, out=val_data_path)
        with zipfile.ZipFile(val_data_path) as val_zip:
            val_zip.extractall(path=val_folder)

    
    def download_test(self) -> None:
        test_folder = os.path.join(self.data_folder, 'test')
        if not os.path.exists(test_folder):
            os.makedirs(test_folder)
        test_data_url = 'http://images.cocodataset.org/zips/test2015.zip'
        test_data_path = os.path.join(test_folder, 'test2015.zip')
        wget.download(test_data_url, test_data_path)
        with zipfile.ZipFile(test_data_path) as test_zip:
            test_zip.extractall(path=test_folder)
    
    def download_annotations(self) -> None:
        annotation_folder = os.path.join(self.data_folder, 'annotation')
        train_folder = os.path.join(annotation_folder, 'train')
        val_folder = os.path.join(annotation_folder, 'val')

        train_annotation_url='https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Annotations_Train_mscoco.zip'
        val_annotation_url='https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Annotations_Val_mscoco.zip'
        
        self.download(train_annotation_url, train_folder)
        self.download(val_annotation_url, val_folder)

    def download_questions(self) -> None:
        train_question_url = 'https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Questions_Train_mscoco.zip'
        val_question_url = 'https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Questions_Val_mscoco.zip'
        test_question_url = 'https://s3.amazonaws.com/cvmlp/vqa/mscoco/vqa/v2_Questions_Test_mscoco.zip'

        question_folder = os.path.join(self.data_folder, 'question')
        train_folder = os.path.join(question_folder, 'train')
        val_folder = os.path.join(question_folder, 'val')
        test_folder = os.path.join(question_folder, 'test')

        self.download(train_question_url, train_folder)
        self.download(val_question_url, val_folder)
        self.download(test_question_url, test_folder)
        

    def download(self, link:str, des_path) -> None:
        if not os.path.exists(des_path):
            os.makedirs(des_path)
        file_name = link.split('/')[-1]
        file_path = os.path.join(des_path, file_name)
        if not self.check_if_downloaded:
            print(file_name + ' will be downloaded at ' + des_path)
            wget.download(link, file_path)
            print('File downloaded')
            print(file_name + ' will be extraxted to ' + des_path)
            with zipfile.ZipFile(file_path) as zip_object:
                zip_object.extractall(path=des_path)
            print('Files are extraxted to ' + des_path)
        else:
            print("File is downloaded at" + file_path)

    def check_if_downloaded(self, download_path:str, download_url:str):
        if os.path.exists(download_path):
            url_size = urllib.request.urlopen(download_url).length
            file_size = os.path.getsize(download_path)
            # Clean partially downloaded file
            if url_size > file_size:
                os.remove(download_path)
                print("Partial file is deleted at " + download_path )
                return False
            elif url_size == file_size:
                print('File is already downloaded at ' + download_path)
                return True
        return False
