import os
from sys import argv


def clear_dir_files(dir_path:str):
    '''
    디렉토리 경로의 파일 제거
    '''
    if dir_path == '':
        return 0
    else:
        if os.listdir(dir_path) == []:
            return
        
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                return e
        return e



def find_project_root():
    '''
    프로젝트의 최상위 경로를 반환(파라미터 X)
    '''
    current_dir = os.path.abspath(argv[0])
    while current_dir != os.path.dirname(current_dir):

        if os.path.isdir(os.path.join(current_dir, 'config')):

            return current_dir
        current_dir = os.path.dirname(current_dir)
    return current_dir


def get_resources_path(root_path, div:str, file_name:str):
    '''
    리소스 불러올 경로 반환(img, font 등)
    '''
    return os.path.join(root_path, 'resources', div, file_name)


def get_json_path(root_path):
    '''
    config.json 파일 경로를 반환
    '''
    return os.path.join(root_path, 'config', 'config.json')


