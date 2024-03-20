set -x
metadata=$1
output_dir=$2
mkdir -p $output_dir && cd $output_dir
/haplox/users/donglf/tcr_scripts/get_VJ_stat_from_metadata.py $metadata total_V.csv total_J.csv score
/haplox/users/donglf/tcr_data_analysis/other_scripts/tcr_AA_freq.py $metadata aa_stat.csv
/haplox/users/donglf/tcr_data_analysis/other_scripts/tcr_length_freq_group.py $metadata length_stat.csv
/haplox/users/donglf/tcr_data_analysis/other_scripts/tcr_convergence_calculation.py $metadata convergence_stat.csv
mkdir -p vdjtools_stat && cd vdjtools_stat
java -jar /x03_haplox/users/donglf/tcr_hapyun/envs/bin/vdjtools-1.2.1/vdjtools-1.2.1.jar CalcDiversityStats -x 1000000  -m $metadata . > vdjtools_calstat.log 2>&1 &
cd ..
/x03_haplox/users/donglf/tcr_data_analysis/enriched_cdr3aa/enriched_score_calculation_batch.py $metadata enrich_stat 10 enriched_cdr3aa.csv
bash enrich_stat/run.sh > enrich_stat/run.log 2>&1 &
/x03_haplox/users/donglf/tcr_hapyun/cdr3aa_summary.py $metadata cdr3aa_stat_summary.csv
wait
/haplox/users/donglf/tcr_hapyun/combine_all_stat2.py . all_combined_stat.csv