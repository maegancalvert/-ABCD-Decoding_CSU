import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import json
import re
import params as p

### represent and interact with directories/folders in the operating system ###
from pathlib import Path
### structure data in an easy to consume way ###
from collections import namedtuple

data_path = Path(p.path_data)

files = sorted(data_path.glob("*.txt"))

data_elements = []
data_structures = {}
event_names = set()
StructureInfo = namedtuple("StructureInfo", field_names=["description", "eventnames", 'visit'])

for text_file in files:
    data_structure = Path(text_file).name.split('.txt')[0]
    data_structure_df = pd.read_csv(text_file, sep='\t', header=[0, 1], nrows=0)
    for data_element, metadata in data_structure_df.columns.values.tolist():
        data_elements.append([data_element, metadata, data_structure])
data_elements_df = pd.DataFrame(data_elements, columns=["element", "description", "structure"])
data_elements_df.to_csv(p.path_tsv, sep="\t", index=None)

data_structures_str = json.dumps(data_structures)
with open(p.path_json, 'w') as fh:
    fh.write('%s\n' % data_structures_str)

data_elements_df = pd.read_csv(p.path_tsv, sep='\t')

with open(p.path_json) as fh1:
    data = fh1.read()
data_structures = json.loads(data)

### developmental history element did not match other data files for eventname (devhx was named visit) ###
### Changed the name of the column to match to integrate data ###
file = pd.read_csv(p.path_data + 'dhx01.txt', delimiter='\t', low_memory=False,)
dhx = file.rename(columns={'visit':'eventname'})
dhx_change = dhx.to_csv(p.path_dhx, sep="\t", index=None)

common = ['subjectkey', 'interview_date', 'interview_age', 'sex', 'eventname']

demographic = ["site_id_l", 'rel_family_id']

exclusions = ['medhx_2c', 'medhx_6i', 'medhx_6p', 'medhx_6j', 'medhx_2m', 'medhx_2h','medhx_2f',
            'ksads_4_826_p', 'ksads_4_827_p','ksads_4_828_p','ksads_4_829_p','ksads_4_849_p','ksads_4_850_p','ksads_4_851_p',
            'ksads_4_852_p', 'devhx_8_tobacco', 'devhx_8_alcohol', 'devhx_8_marijuana', 'devhx_8_coc_crack', 'devhx_8_her_morph',
            'devhx_8_oxycont', 'devhx_8_other_drugs', 'devhx_9_tobacco', 'devhx_9_alcohol', 'devhx_9_marijuana', 'devhx_9_coc_crack',
            'devhx_9_her_morph', 'devhx_9_oxycont', 'devhx_9_other_drugs', 'devhx_12a_p']

# family = ['famhx_ss_fath_prob_alc_p', 'famhx_ss_moth_prob_alc_p', 'famhx_ss_fath_prob_dg_p', 'famhx_ss_moth_prob_dg_p', 'famhx_ss_fath_prob_dprs_p',
#           'famhx_ss_moth_prob_dprs_p', 'famhx_ss_fath_prob_ma_p', 'famhx_ss_moth_prob_ma_p', 'famhx_ss_fath_prob_vs_p', 'famhx_ss_moth_prob_vs_p',
#           'famhx_ss_fath_prob_trb_p', 'famhx_ss_moth_prob_trb_p', 'famhx_ss_fath_prob_nrv_p', 'famhx_ss_moth_prob_nrv_p', 'famhx_ss_fath_prob_scd_p',
#           'famhx_ss_moth_prob_scd_p', #these are yes/no
#           'asr_scr_anxdep_t', 'asr_scr_withdrawn_t', 'asr_scr_somaticpr_t',
#           'asr_scr_thought_t',	'asr_scr_attention_t', 'asr_scr_aggressive_t', 'asr_scr_rulebreak_t',
#           'asr_scr_intrusive_t', #these are t-scores
#           'fes_youth_q1', 'fes_youth_q2', 'fes_youth_q3', 'fes_youth_q4', 'fes_youth_q5', 'fes_youth_q6', 'fes_youth_q7', 'fes_youth_q8', 'fes_youth_q9', #these are yes/no
#           'fam_enviro1_p', 'fam_enviro2r_p', 'fam_enviro3_p', 'fam_enviro4r_p', 'fam_enviro5_p', 'fam_enviro6_p', 'fam_enviro7r_p', 'fam_enviro8_p', 'fam_enviro9r_p'] #thes
# resilience = ['crpbi_parent1_y', 'crpbi_parent2_y', 'crpbi_parent3_y', 'crpbi_parent4_y', 'crpbi_parent5_y',
#           'crpbi_caregiver1_y', 'crpbi_caregiver2_y', 'crpbi_caregiver12_y', 'crpbi_caregiver13_y', 'crpbi_caregiver14_y', 'crpbi_caregiver15_y',
#           'crpbi_caregiver16_y'] #rating scale
# exclusions = ["imgincl_rsfmri_include",]
# imaging = ["rsfmri_cor_ngd_fopa_scs_aglh", "rsfmri_cor_ngd_fopa_scs_agrh"]


data_elements_of_interest = demographic + exclusions

structures2read = {}
for element in data_elements_of_interest:
    item = data_elements_df.query(f"element == '{element}'").structure.values[0]
    if item not in structures2read:
        structures2read[item] = []
    structures2read[item].append(element)

all_df = None
for structure, elements in structures2read.items():
    data_structure_filtered_df = pd.read_csv(p.path_dhx, sep='\t', skiprows=[1],
                                             low_memory=False, usecols=common + elements)
    data_structure_filtered_df = pd.read_csv(data_path / f"{structure}.txt", sep='\t', skiprows=[1],
                                             low_memory=False, usecols=common + elements)
    # ### filtering for only baseline data  - may need to change later ###
    data_structure_filtered_df = data_structure_filtered_df.query("eventname == 'baseline_year_1_arm_1'")
    if all_df is None:
        all_df = data_structure_filtered_df[["subjectkey", "interview_date", "interview_age", "sex"] + elements]
    else:
        all_df = all_df.merge(data_structure_filtered_df[['subjectkey'] + elements], how='outer')

# print(all_df['subjectkey'].value_counts())
print(all_df.shape, all_df.subjectkey.unique().shape)
print(all_df.columns)
#
# #
exclusion_df = pd.DataFrame()
### keep only if ksads = 0 ###
exclusion_df = all_df[all_df['ksads_4_826_p'].isin([0])] # hallucinations present
exclusion_df = all_df[all_df['ksads_4_827_p'].isin([0])] # hallucinations past
exclusion_df = all_df[all_df['ksads_4_828_p'].isin([0])] # delusions present
exclusion_df = all_df[all_df['ksads_4_829_p'].isin([0])] # delusions past
exclusion_df = all_df[all_df['ksads_4_849_p'].isin([0])] # assoc. psychotic symptoms present
exclusion_df = all_df[all_df['ksads_4_850_p'].isin([0])] # assoc. psychotic symptoms past
exclusion_df = all_df[all_df['ksads_4_851_p'].isin([0])] # diagnosis scizophrenia spectrum present
exclusion_df = all_df[all_df['ksads_4_852_p'].isin([0])] # diagnosis scizophrenia spectrum past
#
print(exclusion_df.shape, exclusion_df.subjectkey.unique().shape)
#
# ### keep only if med history 0=no ###
exclusion_df = all_df[all_df["medhx_6i"].isin([0])]  # head injury
exclusion_df = all_df[all_df["medhx_6p"].isin([0])]  # seizure
exclusion_df = all_df[all_df["medhx_6j"].isin([0])]  # knocked unconscious
exclusion_df = all_df[all_df["medhx_2m"].isin([0])]  # MS
exclusion_df = all_df[all_df["medhx_2h"].isin([0])]  # epilepsy or seizures
exclusion_df = all_df[all_df["medhx_2f"].isin([0])]  # cerebral palsy
exclusion_df = all_df[all_df["medhx_2c"].isin([0])]  # brain injury
print(exclusion_df.shape, exclusion_df.subjectkey.unique().shape)

###
# print(all_df[all_df['tbi_ss_ntbiloc']])
