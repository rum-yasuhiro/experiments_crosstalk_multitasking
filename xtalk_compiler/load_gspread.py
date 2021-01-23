from experiments.utils.gspread_access import get_api

def load_gspread(worksheet_name, num_set, num_qc, shift=4, key=None): 
    gc = get_api()
    
    workbook = gc.open_by_key('1Tigim9_mWoMzgZidchelOQ52J589LjuXPIBgBfKOymE')
    if key: 
        workbook = gc.open_by_key(key)

    worksheet = workbook.worksheet(worksheet_name) 
    
    # cell_dict = worksheet.get_all_records(empty2zero=False, head=1, default_blank='')
    bench_list = []
    for i in range(num_set): 
        row_list = worksheet.row_values(i+2)
        name_list = []
        for j in range(num_qc):
            name_list.append(row_list[j] + '_n' + row_list[j+shift])
        bench_list.append(name_list)
    return bench_list