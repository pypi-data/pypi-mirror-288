import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.concurrent_processor import MULTI_PROCESS, THREAD, parallel_process
import cv2
import numpy as np

def norm_single(img, dtype=np.float32, method='linear'):
    """
    단일 이미지를 정규화합니다.

    Parameters:
    img (numpy.ndarray): 입력 이미지
    dtype: 출력 이미지의 데이터 타입
    method (str or int): 정규화 방법. 'linear'/'1' 또는 'divide'/'0'

    Returns:
    numpy.ndarray: 정규화된 이미지
    """
    img = img.astype(dtype)
    
    if isinstance(method, str):
        method = method.lower()

    if method in ['l', 'linear', '1', 1]:
        min_val = img.min()
        max_val = img.max()
        if max_val > min_val:
            img = (img - min_val) / (max_val - min_val)
        else:
            img = img - min_val  # 모든 픽셀이 같은 값일 경우
    elif method in ['d', 'divide', '0', 0]:
        img = img / 255.0
    else:
        raise ValueError("Unsupported normalization method. Use 'linear'/'1' or 'divide'/'0'.")
    
    return img

def norm(img_set:np.ndarray, dtype=np.float32, method='linear', parallel_method=THREAD):
    """
    이미지 셋의 모든 이미지를 정규화합니다.

    Parameters:
    img_set (list of numpy.ndarray): 입력 이미지 셋
    dtype: 출력 이미지의 데이터 타입
    method (str or int): 정규화 방법. 'linear'/'1' 또는 'divide'/'0'
    parallel_method: 병렬 처리 방법 (THREAD 또는 MULTI_PROCESS)

    Returns:
    numpy.ndarray: 정규화된 이미지 셋
    """
    norm_args = [(img, dtype, method) for img in img_set]
    normed_imgs = parallel_process(norm_single, norm_args, executor_class=parallel_method)
    return np.array(normed_imgs, dtype=dtype)

def to_uint8(img):
    """
    이미지를 uint8 형식으로 변환합니다.
    """
    if img.dtype != np.uint8:
        if np.issubdtype(img.dtype, np.floating):
            img = (img * 255).clip(0, 255).astype(np.uint8)
        else:
            img = img.astype(np.uint8)
    return img

def resize_single(img, size):
    """
    단일 이미지를 주어진 크기로 재조정합니다.

    Parameters:
    img (numpy.ndarray): 입력 이미지
    size (tuple): (width, height)의 형태로 주어진 새로운 크기

    Returns:
    numpy.ndarray: 재조정된 이미지
    """
    original_dtype = img.dtype
    img = to_uint8(img)
    resized_img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    return resized_img.astype(original_dtype)

def resize(img_set, size, dtype=None, parallel_method=THREAD):
    """
    이미지 셋의 모든 이미지를 주어진 크기로 재조정합니다.

    Parameters:
    img_set (list of numpy.ndarray or numpy.ndarray): 입력 이미지 셋
    size (tuple): (width, height)의 형태로 주어진 새로운 크기
    dtype: 출력 이미지의 데이터 타입
    parallel_method: 병렬 처리 방법 (THREAD 또는 MULTI_PROCESS)

    Returns:
    numpy.ndarray: 재조정된 이미지 셋
    """
    if isinstance(img_set, np.ndarray) and img_set.ndim == 3:
        img_set = [img_set]
    elif isinstance(img_set, np.ndarray) and img_set.ndim == 4:
        img_set = [img for img in img_set]
    elif not isinstance(img_set, list):
        raise ValueError("img_set must be a list of images or a numpy array")

    resize_args = [(img, size) for img in img_set]
    resized_imgs = parallel_process(resize_single, resize_args, executor_class=parallel_method)
    
    if dtype is None:
        dtype = img_set[0].dtype
    return np.array(resized_imgs, dtype=dtype)

def equalize_hist_single(img, color_space='ycrcb'):
    """
    단일 이미지에 대해 히스토그램 평활화를 수행합니다.

    Parameters:
    img (numpy.ndarray): 입력 이미지 (RGB)
    color_space (str or int): 사용할 색상 공간 ('ycrcb'/0 또는 'lab'/1)

    Returns:
    numpy.ndarray: 히스토그램 평활화된 이미지 (RGB)
    """
    original_dtype = img.dtype
    img = to_uint8(img)

    if isinstance(color_space, str):
        color_space = color_space.lower()

    if color_space in ['y', 'ycrcb', '0', 0]:
        img_color = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
        channels = cv2.split(img_color)
        cv2.equalizeHist(channels[0], channels[0])
        img_eq = cv2.merge(channels)
        img_eq = cv2.cvtColor(img_eq, cv2.COLOR_YCrCb2RGB)
    elif color_space in ['l', 'lab', '1', 1]:
        img_color = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
        channels = cv2.split(img_color)
        cv2.equalizeHist(channels[0], channels[0])
        img_eq = cv2.merge(channels)
        img_eq = cv2.cvtColor(img_eq, cv2.COLOR_LAB2RGB)
    else:
        raise ValueError("Unsupported color space. Use 'ycrcb'/0 or 'lab'/1.")
    
    if np.issubdtype(original_dtype, np.floating):
        img_eq = img_eq.astype(np.float32) / 255.0
    
    return img_eq.astype(original_dtype)

def equalize_hist(img_set, color_space='ycrcb', dtype=None, parallel_method=THREAD):
    """
    이미지 셋의 모든 이미지에 대해 히스토그램 평활화를 수행합니다.

    Parameters:
    img_set (list of numpy.ndarray or numpy.ndarray): 입력 이미지 셋 (RGB 이미지들)
    color_space (str or int): 사용할 색상 공간 ('ycrcb'/0 또는 'lab'/1)
    dtype: 출력 이미지의 데이터 타입
    parallel_method: 병렬 처리 방법 (THREAD 또는 MULTI_PROCESS)

    Returns:
    numpy.ndarray: 히스토그램 평활화된 이미지 셋
    """
    if isinstance(img_set, np.ndarray) and img_set.ndim == 3:
        img_set = [img_set]
    elif isinstance(img_set, np.ndarray) and img_set.ndim == 4:
        img_set = [img for img in img_set]
    elif not isinstance(img_set, list):
        raise ValueError("img_set must be a list of images or a numpy array")

    eq_args = [(img, color_space) for img in img_set]
    eq_imgs = parallel_process(equalize_hist_single, eq_args, executor_class=parallel_method)
    
    if dtype is None:
        dtype = img_set[0].dtype
    return np.array(eq_imgs, dtype=dtype)