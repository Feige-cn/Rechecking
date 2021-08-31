'''
1、查询根目录下是否存在重复文件，删除；
2、比对两个根目录下是否存在重复文件，删除；
3、重新筛查两个根目录，删除空文件夹。

待更新：根目录下所有文件清洗，压缩包自解压，并过滤不需要的文件类型
'''
import json
import os
import time
from hashlib import md5

class Book_Rechecking():
    def __init__(self, base_path, test_path):
        self.base_path = base_path
        self.test_path = test_path

    def del_emp_dir(self, path):
        for x, y, z in os.walk(path):
            for i in y:
                if not os.listdir(os.path.join(x, i)):
                    os.rmdir(os.path.join(x, i))
                    print('删除空文件夹\t{}'.format(os.path.join(x, i)))

    def getmd5(self, path):
        print('正在读取文件{}……\n'.format(path))
        time.sleep(1)
        md5_path = os.path.join(path, 'md5.json')
        if os.path.isfile(md5_path):
            print('读取已有MD5数据')
        else:
            files = []
            files_path = []
            for x, y, z in os.walk(path):
                for i in z:
                    files.append(i)
                    files_path.append(os.path.join(x, i))

            book_md5 = {}
            book_repeat = []
            for n in range(len(files_path)):
                hash_value = md5()
                with open(files_path[n], 'rb') as f:
                    hash_value.update(f.read())
                md5_value = hash_value.hexdigest()
                if md5_value in list(book_md5.keys()):
                    book_repeat.append(files_path[n])
                    print('********{}\t内部重复********'.format(files[n]))
                else:
                    book_md5[md5_value] = files_path[n]
                    print('{}]\tMD5校验已完成'.format(files[n]))
            if len(book_repeat) != 0:
                print('\n********内部重复\t{}\t********'.format(len(book_repeat)))
                for i in book_repeat:
                    print(i)
                Y_or_N = input('是否删除\t{}\t个内部重复文件？(Y/N)'.format(len(book_repeat)))
                if Y_or_N == 'Y':
                    for i in book_repeat:
                        os.remove(i)
                        print('删除\t{}'.format(i))

            with open(md5_path, 'w', encoding='utf-8') as f:
                json.dump(book_md5, f, indent=4, sort_keys=True, ensure_ascii=False)
        return md5_path

    def check(self):
        print('---------------Analysis---------------')
        self.base_md5_path = self.getmd5(self.base_path)
        with open(self.base_md5_path, 'rt', encoding='utf-8') as f:
            md5_base = json.load(f)
        print('载入目标文件夹数据……\n')
        self.test_md5_path = self.getmd5(self.test_path)
        with open(self.test_md5_path, 'rt', encoding='utf-8') as f:
            md5_test = json.load(f)
        print('载入测试文件夹数据……\n')
        md5_repeat = {}
        for m in md5_test.keys():
            if m in md5_base.keys():
                print('[md5]{}    [base]{}   [test]{}'.format(m, md5_base[m], md5_test[m]))
                md5_repeat[m] = {'base': md5_base[m], 'test': md5_test[m]}
        if len(md5_repeat) !=0:
            repeat_md5_path = os.path.join(self.test_path, 'repeat_md5.json')
            with open(repeat_md5_path, 'w', encoding='utf-8') as f:
                json.dump(md5_repeat, f, indent=4, sort_keys=True, ensure_ascii=False)
            print('------------比对结果----------')
            print('目标文件数 {}      测试文件数 {}      Repeat {}'.format(len(md5_base), len(md5_test), len(md5_repeat)))
            Y_or_N = input('是否删除重复文件？(Y/N)')
            if Y_or_N == 'Y':
                for i, j in md5_repeat.items():
                    os.remove(j['test'])
                    print('删除\t{}'.format(j['test']))
                    del md5_test[i]
                with open(self.test_md5_path, 'w', encoding='utf-8') as f:
                    json.dump(md5_test, f, indent=4, sort_keys=True, ensure_ascii=False)
        else:
            print('****比对完成，没有重复****')

        self.del_emp_dir(self.base_path)
        self.del_emp_dir(self.test_path)

if __name__ == '__main__':
    base_path = input('请输入基础文件夹地址：')
    test_path = input('请输入测试文件夹地址：')
    app = Book_Rechecking(base_path, test_path)
    app.check()
