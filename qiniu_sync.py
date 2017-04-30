from qiniu import Auth, put_file, etag, urlsafe_base64_encode, BucketManager
from typing import List, Dict
import os

from qiniu import build_batch_delete


class Sync:
    """
    同步目录至七牛云
    """
    def __init__(self, access_key: str, secret_key: str, bucket_name: str, sync_dir: str, exclude: List,
                 cover: bool, remove_redundant: bool):
        self.bucket_name = bucket_name
        self.q = Auth(access_key, secret_key)
        self.bucket = BucketManager(self.q)
        self.sync_dir = sync_dir
        self.exclude = exclude
        self.cover = cover
        self.remove_redundant = remove_redundant

        self.sync()

    def sync(self):
        """
        同步操作
        :return:
        """
        remote_files = self.list_remote()
        local_files = self.list_local()

        # 首先删除远端多余的文件
        remove_remote_files = []
        for remote_filename in remote_files:
            if remote_filename not in local_files:
                remove_remote_files.append(remote_filename)
        self.bucket.batch(build_batch_delete(self.bucket_name, remove_remote_files))

        # 上传本地文件到远端(未出现过的)
        for local_filename in local_files:
            if local_filename not in remote_files or local_files[local_filename]['hash'] != remote_files[local_filename]['hash']:
                print('puting ' + local_filename)
                ret, info = put_file(
                    self.q.upload_token(self.bucket_name, local_filename, 3600),
                    local_filename,
                    local_files[local_filename]['fullpath']
                )
        #
        #
        # print(remote_files)
        # print(local_files)

        # 首先把远程有名字而本地没有那个名字的删除掉
        # 然后执行覆盖或者不覆盖的上传
        # remove_remote_files = []
        # for file in remote_files:
        #     if
        #
        #
        # remove_remote_files = [file if file not in local_files else None for file in remote_files]
        #
        #
        # # 首先上传本地到远程
        # print(self.list_local())
        # 然后删除远程多余的remove_redundant
        pass

    def list_remote(self) -> Dict:
        """
        列出远程仓库所有的文件信息
        :return: List
        """
        result = {}
        for file in self.bucket.list(self.bucket_name)[0]['items']:
            result[file['key']] = file

        return result

    def list_local(self) -> Dict:
        """
        列出本地仓库所有的文件信息
        """
        files = {}

        def get_files(path):
            for filename in os.listdir(path):
                if filename in self.exclude:
                    continue
                fullpath = os.path.join(path, filename)
                if os.path.isfile(fullpath):
                    key = fullpath.split(self.sync_dir)[1]
                    files[key] = {
                        'fullpath': fullpath,
                        'hash': etag(fullpath)
                    }
                    # files[fullpath.split()] = {
                    #     'path': fullpath,
                    #     'hash': etag(fullpath)
                    # }
                    #
                    # upload(key, file)
                    # upload(key.split('index.html')[0], file)
                    # upload(key.split('/index.html')[0], file)
                else:
                    get_files(fullpath)
        get_files(self.sync_dir)
        return files

if __name__ == '__main__':
    Sync(

    )