from experiments.utils import pickle_load, pickle_dump


def result_alap(backend, simulator, job_file_path, save_path=None): 
    job_sim, jobs, jobs_alap, job_dict = parse_job_files(job_file_path, backend, simulator)
    
    result_sim = job_sim.result()
    count_sim = result_sim.get_counts()

    result_list = [_job.result() for _job in jobs]
    count_list = [_result.get_counts() for _result in result_list]

    result_alap_list = [_job_alap.result() for _job_alap in jobs_alap]
    count_alap_list = [_result_alap.get_counts() for _result_alap in result_alap_list]
    
    
    if save_path:
        qc_sim = job_dict["simulator"]["qc"]
        qc = job_dict["non_scheduling"]["qc"]
        qc_alap = job_dict["alap"]["qc"]
        qc_names = job_dict["qc_names"] or None
        try:
            date = job_dict["date"]
        except: 
            date = None
        save_results(qc_sim, qc, qc_alap, result_sim, result_list, result_alap_list, count_sim, count_list, count_alap_list, qc_names, date, save_path)

    return result_sim, result_list, result_alap_list, count_sim, count_list, count_alap_list, qc_names    

def parse_job_files(job_file_path, backend, simulator):
    """
    experiments_data = {
        "simulator": {
            "qc": qc_sim,
            "job_id": job_id_sim, 
        }, 
        "non_scheduling": {
            "qc": qc,
            "job_id": job_id,
            "nseed": nseed,
        }, 
        "alap": {
            "qc": qc_alap,
            "job_id": job_id_alap,
            "nseed": nseed, 
        }, 
        "qc_names": names,
    }
    """
    job_dict = pickle_load(job_file_path)
    job_sim = simulator.retrieve_job(job_dict["simulator"]["job_id"])
    jobs = [backend.retrieve_job(_job) for _job in job_dict["non_scheduling"]["job_id"]]
    jobs_alap = [backend.retrieve_job(_job_alap) for _job_alap in job_dict["alap"]["job_id"]]
    qc_names = job_dict["qc_names"]
    
    return job_sim, jobs, jobs_alap, job_dict
    
def save_results(
    qc_sim, qc, qc_alap, 
    result_sim, result_list, result_alap_list, 
    count_sim, count_list, count_alap_list, 
    qc_names, date, save_path
    ):
    data = {
        "simulator": {
            "qc": qc_sim,
            "result": result_sim,
            "count": count_sim,
        }, 
        "non_scheduling": {
            "qc": qc,
            "result": result_list,
            "count": count_list,
        }, 
        "alap": {
            "qc": qc_alap,
            "result": result_alap_list,
            "count": count_alap_list, 
        }, 
        "qc_names": qc_names,
        "date": date, 
    }
    pickle_dump(data, save_path)