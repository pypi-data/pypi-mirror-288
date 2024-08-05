from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

MULTI_PROCESS = ProcessPoolExecutor
THREAD = ThreadPoolExecutor

def parallel_process(func, iterable, executor_class=THREAD):
    """
    주어진 함수를 병렬로 처리하고 원래 순서를 유지합니다.

    Parameters:
    func (callable): 병렬로 실행할 함수
    iterable (iterable): 함수에 전달할 인자들의 이터러블
    executor_class (class): 사용할 Executor 클래스 (MULTI_PROCESS 또는 THREAD)

    Returns:
    list: 처리 결과의 리스트 (원래 순서 유지)
    """
    with executor_class() as executor:
        results = list(executor.map(lambda x: (x[0], func(*x[1])), enumerate(iterable)))
    return [result for _, result in sorted(results, key=lambda x: x[0])]