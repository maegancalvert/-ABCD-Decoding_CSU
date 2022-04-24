import pandas as pd

base_path = '/home/mcalvert/'
data_name = 'ABCD4'
base_name = 'ABCD-Decoding_CSU'
study_list = {'ABCD-Decoding_CSU'}

# Primary paths
path_code = base_path + 'workspace/code/' + base_name + '/'
path_data = base_path + 'workspace/data/' + data_name + '/'
#path_bids = base_path + 'workspace/bids/' + base_name + '/'

# Paths
path_json = path_data + 'data_struct_json.json'
path_tsv = path_data + 'data_elements.tsv'
path_dhx = path_data + 'developmental_hx_changed.tsv'  ### This change was made as the visit column was not consistent with the eventname column###
                                                        ### Changed the visit name to eventname to merge data ###
f = pd.read_csv(path_dhx, sep='\t')
print(f.dtypes)
print(f.columns.tolist())

# path_subjs = path_code + 'subj_list/'
# path_log = path_code + 'log/'
# path_fig = path_code + 'fig/'
# path_fmriprep = path_data + 'fmriprep/'
# path_pipe = path_data + 'pipeline/'
# path_tmp = path_pipe + 'tmp/'
#
# path_mri = path_pipe + 'mri/'
# path_mri_clean = path_mri + 'mri_clean/'
# path_mri_gm_mask = path_mri + 'mri_gm_mask/'
#
# path_betas = path_pipe + 'betas/'
# path_betas_mri_ex = path_betas + 'mri_ex/'
#
# path_labels = path_pipe + 'labels/'
# path_labels_ex = path_labels + 'ex/'
#
# path_mvpa = path_pipe + 'mvpa/'
# path_mvpa_mri_ex = path_mvpa + 'mri_ex/'
#
# path_analysis = path_pipe + 'analysis/'
# path_analysis_mvpa_mri_ex = path_mvpa + 'mri_ex/'
#
# # MRI sequence parameters & sequence specific preprocessing parameters
# mri_params = dict()
#
# mri_params['space'] = 'MNI152NLin2009cAsym_res-2'
# mri_params['desc'] = 'preproc_bold'
