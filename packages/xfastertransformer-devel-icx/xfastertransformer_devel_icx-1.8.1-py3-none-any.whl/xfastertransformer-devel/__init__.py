import os
from ctypes import cdll

def with_mpirun():
    return any(os.getenv(env) for env in ["MPI_LOCALRANKID", "MPI_LOCALNRANKS", "PMI_RANK", "PMI_SIZE", "PMIX_RANK"])

if os.getenv("SINGLE_INSTANCE", "0") == "0" and with_mpirun():
    cdll.LoadLibrary(os.path.dirname(os.path.abspath(__file__)) + "/lib/libxft_comm_helper.so")
    
cdll.LoadLibrary(os.path.dirname(os.path.abspath(__file__)) + "/lib/libxfastertransformer.so")