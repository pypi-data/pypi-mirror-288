# gen_fake_term task

gen_fake_term
--fwd_i 'use fwdi as original data' 
--start_date 'start_date' 
--end_date 'end_date '
--ret_type 'return type, e.g. v2vm, v2v'
--freq 'Frequency' 
--univ 'univ' 
--output_path 'the path that save fake term' 
--high_corr 'generate fake term with high correlation or not'
--n_term 'number of fake term'

Examples:
1. Generate 100 fake terms with high correlation
gen_fake_term --fwd_i 2 --start_date 20191220 --end_date 20191220 --freq M30 --univ ZZQZ --ret_type v2v --output_path /nfs/ssd/share/fake_term/high --n_term 100 --high_corr True
2. Generate 100 fake terms with low correlation
gen_fake_term --fwd_i 2 --start_date 20191220 --end_date 20191220 --freq M30 --univ ZZQZ --ret_type v2v --output_path /nfs/ssd/share/fake_term/high --n_term 100