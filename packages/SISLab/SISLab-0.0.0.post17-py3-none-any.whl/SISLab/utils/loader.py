import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.concurrent_processor import MULTI_PROCESS, THREAD, parallel_process
from PIL import Image
import cv2, numpy as np

def load_image(file_path, index, as_ndarray):
    """
    단일 이미지를 로드하여 반환합니다.

    Parameters:
    file_path (str): 이미지 파일의 경로
    index (int): 파일의 인덱스
    as_ndarray (bool): True로 설정하면 이미지를 numpy ndarray로 로드합니다. False로 설정하면 cv2 이미지 객체로 로드합니다.

    Returns:
    tuple: (index, img) 형태의 튜플
    """
    try:
        img = cv2.imread(file_path)
        if img is None:
            raise Exception("이미지를 로드할 수 없습니다.")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if not as_ndarray:
            img = cv2.UMat(img)  # cv2의 이미지 객체로 변환
        return (index, img)
    except Exception as e:
        print(f"이미지 {file_path}을(를) 로드하는 중 에러 발생: {e}")
        return (index, None)


def load_images(folder_path: str, as_ndarray: bool = True, parallel_method=THREAD):
    """
    주어진 폴더 경로에서 jpg, jpeg, png 파일을 모두 로드하여 반환합니다.

    Parameters:
    folder_path (str): 이미지 파일이 저장된 폴더의 경로
    as_ndarray (bool): True로 설정하면 이미지를 numpy ndarray로 로드합니다. False로 설정하면 cv2 이미지 객체로 로드합니다.
    parallel_method: 병렬 처리 방법 (THREAD 또는 MULTI_PROCESS)

    Returns:
    images (list): cv2 이미지 객체 또는 numpy ndarray 객체의 리스트
    """
    valid_extensions = ('.jpg', '.jpeg', '.png')

    # 폴더가 존재하는지 확인
    if not os.path.exists(folder_path):
        raise ValueError("해당 경로에 폴더가 존재하지 않습니다.")

    # 모든 파일 경로 수집
    file_paths = [os.path.join(folder_path, filename) 
                  for filename in os.listdir(folder_path)
                  if filename.lower().endswith(valid_extensions)]

    # 병렬 처리로 이미지 로드
    load_image_args = [(file_path, index, as_ndarray) for index, file_path in enumerate(file_paths)]
    results = parallel_process(load_image, load_image_args, executor_class=parallel_method)

    # 인덱스 순으로 정렬
    results.sort(key=lambda x: x[0])
    images = [img for index, img in results]

    return images