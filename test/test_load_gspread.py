from experiments.xtalk_compiler.load_gspread import load_gspread


def test_load_gspread(): 
    bench_list = load_gspread(worksheet_name='set_4', num_set=14, num_qc=4)
    print(bench_list)