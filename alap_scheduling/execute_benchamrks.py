from typing import List

from utils import get_IBM_backend, pickle_dump
from palloq.compiler import multi_transpile

def execute_benchmarks(benchmarks: List[str]):
