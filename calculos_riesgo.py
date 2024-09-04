
import numpy as np
import pandas as pd

def check_T1_T2_consistency(data):
    set_T1_missing = data.T1.values.copy().astype(float)
    set_T2_missing = data.T2.values.copy().astype(float)
    set_T1_missing[(data.T1 < 20) | (data.T1 >= 90) | (data.T1 >= data.T2)] = np.nan
    set_T2_missing[(data.T2 > 90) | (data.T1 >= data.T2)] = np.nan
    return set_T1_missing, set_T2_missing

def recode_NB_Cat(data, Error_Ind):
    NB_Cat = np.repeat(-1., data.shape[0])
    mask_a = ((data.N_Biop == 0) | (data.N_Biop == 99)) & (data.HypPlas != 99)
    NB_Cat[mask_a] = -100
    Error_Ind[mask_a] = 1
    mask_b = ((data.N_Biop > 0) & (data.N_Biop < 99)) & (~data.HypPlas.isin([0, 1, 99]))
    NB_Cat[mask_b] = -200
    Error_Ind[mask_b] = 1
    mask_c = (NB_Cat == -1) & ((data.N_Biop == 0) | (data.N_Biop == 99))
    NB_Cat[mask_c] = 0
    mask_d = (NB_Cat == -1) & (data.N_Biop == 1)
    NB_Cat[mask_d] = 1
    mask_e = (NB_Cat == -1) & ((data.N_Biop >= 2) & (data.N_Biop != 99))
    NB_Cat[mask_e] = 2
    hispanic_mask = data.Race.isin([3, 5])
    NB_Cat[hispanic_mask & (NB_Cat == 2)] = 1
    NB_Cat[NB_Cat == -1] = np.nan
    return NB_Cat, Error_Ind

def recode_AM_Cat(data):
    AM_Cat = np.repeat(np.nan, data.shape[0])
    mask_0 = ((data.AgeMen >= 14) & (data.AgeMen <= data.T1)) | (data.AgeMen == 99)
    AM_Cat[mask_0] = 0
    mask_1 = (data.AgeMen >= 12) & (data.AgeMen < 14)
    AM_Cat[mask_1] = 1
    mask_2 = (data.AgeMen > 0) & (data.AgeMen < 12)
    AM_Cat[mask_2] = 2
    mask_nan = (data.AgeMen > data.T1) & (data.AgeMen != 99)
    AM_Cat[mask_nan] = np.nan
    african_american_mask = (data.Race == 2) & (AM_Cat == 2)
    AM_Cat[african_american_mask] = 1
    hispanic_mask = (data.Race == 3) & (AM_Cat == 2)
    AM_Cat[hispanic_mask] = 0
    return AM_Cat

def recode_AF_Cat(data):
    AF_Cat = np.repeat(np.nan, data.shape[0])
    AF_Cat[(data.Age1st < 20) | (data.Age1st == 99)] = 0
    AF_Cat[(data.Age1st >= 20) & (data.Age1st < 25)] = 1
    AF_Cat[((data.Age1st >= 25) & (data.Age1st < 30)) | (data.Age1st == 98)] = 2
    AF_Cat[(data.Age1st >= 30) & (data.Age1st < 98)] = 3
    AF_Cat[(data.Age1st < data.AgeMen) & (data.AgeMen != 99)] = np.nan
    AF_Cat[(data.Age1st > data.T1) & (data.Age1st < 98)] = np.nan
    AF_Cat[data.Race == 2] = 0
    hispanic_mask = data.Race.isin([3, 5])
    af_cat_2_mask = (AF_Cat == 2)
    af_cat_3_mask = (AF_Cat == 3)
    AF_Cat[hispanic_mask & af_cat_2_mask] = 1
    AF_Cat[hispanic_mask & af_cat_3_mask] = 2
    return AF_Cat

def recode_NR_Cat(data):
    NR_Cat = np.repeat(np.nan, data.shape[0])
    NR_Cat[(data.N_Rels == 0) | (data.N_Rels == 99)] = 0
    NR_Cat[data.N_Rels == 1] = 1
    NR_Cat[(data.N_Rels >= 2) & (data.N_Rels < 99)] = 2
    NR_Cat[((data.Race >= 6) & (data.Race <= 11)) & (NR_Cat == 2)] = 1
    return NR_Cat

def set_R_Hyp(NB_Cat, data):
    R_Hyp = np.repeat(np.nan, data.shape[0])
    R_Hyp[NB_Cat == 0] = 1.00
    R_Hyp[((NB_Cat != -100) & (NB_Cat > 0)) & (data.HypPlas == 0)] = 0.93
    R_Hyp[((NB_Cat != -100) & (NB_Cat > 0)) & (data.HypPlas == 1)] = 1.82
    R_Hyp[((NB_Cat != -100) & (NB_Cat > 0)) & (data.HypPlas == 99)] = 1.00
    return R_Hyp

def get_HyperP_and_R_Hyp_missing(NB_Cat, data):
    set_HyperP_missing = data.HypPlas.values.copy()
    set_R_Hyp_missing = set_R_Hyp(NB_Cat, data).copy()
    set_HyperP_missing[NB_Cat == -100] = -100
    set_R_Hyp_missing[NB_Cat == -100] = -100
    set_HyperP_missing[NB_Cat == -200] = -200
    set_R_Hyp_missing[NB_Cat == -200] = -200
    return set_HyperP_missing, set_R_Hyp_missing

def set_Race(data):
    set_Race_missing = data.Race.values.copy()
    Race_range = np.array(range(1, 12))
    set_Race_missing[~data.Race.isin(Race_range)] = -300
    return set_Race_missing

def set_CharRace(data):
    CharRace = np.repeat('??', data.shape[0])
    race_dict = {
        1: "Wh", 2: "AA", 3: "HU", 4: "NA", 5: "HF", 6: "Ch", 7: "Ja", 8: "Fi", 9: "Hw",
        10: "oP", 11: "oA"
    }
    for key, value in race_dict.items():
        CharRace[data.Race == key] = value
    return CharRace

def recode_check(data, Raw_Ind=1):
    Error_Ind = np.zeros(data.shape[0])
    set_T1_missing, set_T2_missing = check_T1_T2_consistency(data)
    Error_Ind[np.isnan(set_T1_missing)] = 1
    Error_Ind[np.isnan(set_T2_missing)] = 1

    if Raw_Ind == 1:
        NB_Cat, Error_Ind = recode_NB_Cat(data, Error_Ind)
        AM_Cat = recode_AM_Cat(data)
        AF_Cat = recode_AF_Cat(data)
        NR_Cat = recode_NR_Cat(data)
    else:
        NB_Cat = data.N_Biop
        AM_Cat = data.AgeMen
        AF_Cat = data.Age1st
        NR_Cat = data.N_Rels

    R_Hyp = set_R_Hyp(NB_Cat, data)
    set_HyperP_missing, set_R_Hyp_missing = get_HyperP_and_R_Hyp_missing(NB_Cat, data)
    set_Race_missing = set_Race(data)
    CharRace = set_CharRace(data)

    Error_Ind[(np.isnan(NB_Cat)) | (np.isnan(AM_Cat)) | (np.isnan(AF_Cat)) |
              (np.isnan(NR_Cat)) | (set_Race_missing == -300)] = 1

    recode_check_df = pd.DataFrame({
        'Error_Ind': Error_Ind, 'set_T1_missing': set_T1_missing,
        'set_T2_missing': set_T2_missing, 'NB_Cat': NB_Cat,
        'AM_Cat': AM_Cat, 'AF_Cat': AF_Cat, 'NR_Cat': NR_Cat,
        'R_Hyp': R_Hyp, 'set_HyperP_missing': set_HyperP_missing,
        'set_R_Hyp_missing': set_R_Hyp_missing, 'set_Race_missing': set_Race_missing,
        'CharRace': CharRace
    })

    return recode_check_df

def cargar_betas(file_path):
    df = pd.read_csv(file_path, index_col=0)
    betas = {
        'White_Beta': df['Wh.Gail'].values,
        'Black_Beta': df['AA.CARE'].values,
        'Hspnc_Beta': df['HU.Gail'].values,
        'Other_Beta': df['NA.Gail'].values,
        'FHspnc_Beta': df['HF.Gail'].values,
        'Asian_Beta': df['Asian.AABCS'].values
    }
    Wrk_Beta_all = np.vstack((
        betas['White_Beta'],
        betas['Black_Beta'],
        betas['Hspnc_Beta'],
        betas['Other_Beta'],
        betas['FHspnc_Beta'],
        betas['Asian_Beta'],
        betas['Asian_Beta'],
        betas['Asian_Beta'],
        betas['Asian_Beta'],
        betas['Asian_Beta'],
        betas['Asian_Beta']
    ))
    return Wrk_Beta_all

def calcular_numero_patron(NB_Cat, AM_Cat, AF_Cat, NR_Cat):
    PatternNumber = np.full(len(NB_Cat), np.nan)
    PNID = np.where((~np.isnan(NB_Cat)) & (~np.isnan(AM_Cat)) & (~np.isnan(AF_Cat)) & (~np.isnan(NR_Cat)))[0]
    PatternNumber[PNID] = NB_Cat[PNID] * 36 + AM_Cat[PNID] * 12 + AF_Cat[PNID] * 3 + NR_Cat[PNID] * 1 + 1
    return PatternNumber, PNID

def relative_risk(file_path4, data, Raw_Ind=1):
    Wrk_Beta_all = cargar_betas(file_path4)
    LP1 = np.full(data.shape[0], np.nan)
    LP2 = np.full(data.shape[0], np.nan)
    check_cov = recode_check(data, Raw_Ind)
    NB_Cat = check_cov.NB_Cat.values
    NB_Cat[(NB_Cat == -100) | (NB_Cat == -200)] = np.nan
    AM_Cat = check_cov.AM_Cat.values
    AF_Cat = check_cov.AF_Cat.values
    NR_Cat = check_cov.NR_Cat.values
    R_Hyp = check_cov.R_Hyp.values
    CharRace = check_cov.CharRace.values
    PatternNumber, PNID = calcular_numero_patron(NB_Cat, AM_Cat, AF_Cat, NR_Cat)

    for i in PNID:
        if CharRace[i] != "??":
            Beta = Wrk_Beta_all[int(data.Race[i]) - 1]
            LP1[i] = NB_Cat[i] * Beta[0] + AM_Cat[i] * Beta[1] + AF_Cat[i] * Beta[2] + NR_Cat[i] * Beta[3] + AF_Cat[i] * NR_Cat[i] * Beta[5] + np.log(R_Hyp[i])
            LP2[i] = LP1[i] + NB_Cat[i] * Beta[4]

    RR_Star1 = np.exp(LP1)
    RR_Star2 = np.exp(LP2)
    RR_Star = pd.DataFrame({'RR_Star1': RR_Star1, 'RR_Star2': RR_Star2, 'PatternNumber': PatternNumber})
    return RR_Star

def cargar_lambda1(file_path):
    df = pd.read_csv(file_path)
    lambda_dict = {
        'White_lambda1': np.array([df['Wh.1983_87'].values]),
        'Black_lambda1': np.array([df['AA.1994_98'].values]),
        'Hspnc_lambda1': np.array([df['HU.1995_04'].values]),
        'Other_lambda1': np.array([df['NA.1983_87'].values]),
        'FHspnc_lambda1': np.array([df['HF.1995_04'].values]),
        'Chnes_lambda1': np.array([df['Ch.1998_02'].values]),
        'Japns_lambda1': np.array([df['Ja.1998_02'].values]),
        'Filip_lambda1': np.array([df['Fi.1998_02'].values]),
        'Hawai_lambda1': np.array([df['Hw.1998_02'].values]),
        'OtrPI_lambda1': np.array([df['oP.1998_02'].values]),
        'OtrAs_lambda1': np.array([df['oA.1998_02'].values]),
        'White_lambda1Avg': np.array([df['Wh_Avg.1992_96'].values]),
        'White_nlambda1': np.array([[0.0000120469, 0.0000746893, 0.0002437767, 0.0005878291, 0.0012069622, 0.0019762053, 0.0026200977,
                                    0.0033401788, 0.0039743676, 0.0044875763, 0.0048945499, 0.0051610641, 0.0048268456, 0.0040407389]])
    }
    lambda_array = np.concatenate(
        [lambda_dict['White_lambda1'], lambda_dict['Black_lambda1'], lambda_dict['Hspnc_lambda1'], lambda_dict['Other_lambda1'],
         lambda_dict['FHspnc_lambda1'], lambda_dict['Chnes_lambda1'], lambda_dict['Japns_lambda1'], lambda_dict['Filip_lambda1'],
         lambda_dict['Hawai_lambda1'], lambda_dict['OtrPI_lambda1'], lambda_dict['OtrAs_lambda1']], axis=0)
    return lambda_array

def cargar_lambda2(file_path):
    df = pd.read_csv(file_path)
    lambda_dict = {
        'White_lambda2': df['Wh.1983_87'].astype(float).values,
        'Black_lambda2': df['AA.1994_98'].astype(float).values,
        'Hspnc_lambda2': df['HU.1995_04'].astype(float).values,
        'Other_lambda2': df['NA.1983_87'].astype(float).values,
        'FHspnc_lambda2': df['HF.1995_04'].astype(float).values,
        'Chnes_lambda2': df['Ch.1998_02'].astype(float).values,
        'Japns_lambda2': df['Ja.1998_02'].astype(float).values,
        'Filip_lambda2': df['Fi.1998_02'].astype(float).values,
        'Hawai_lambda2': df['Hw.1998_02'].astype(float).values,
        'OtrPI_lambda2': df['oP.1998_02'].astype(float).values,
        'OtrAs_lambda2': df['oA.1998_02'].astype(float).values,
        'White_lambda2Avg': df['Wh_Avg.1992_96'].astype(float).values,
        'White_nlambda2': np.array([0.0004000377, 0.0004280396, 0.0005656742, 0.0008474486, 0.0012752947,
                                    0.0018601059, 0.0028780622, 0.0046903348, 0.0078835252, 0.0127434461,
                                    0.0208586233, 0.0335901145, 0.0575791439, 0.1377327125])
    }
    lambda_array = np.vstack([
        lambda_dict['White_lambda2'], lambda_dict['Black_lambda2'], lambda_dict['Hspnc_lambda2'],
        lambda_dict['Other_lambda2'], lambda_dict['FHspnc_lambda2'], lambda_dict['Chnes_lambda2'],
        lambda_dict['Japns_lambda2'], lambda_dict['Filip_lambda2'], lambda_dict['Hawai_lambda2'],
        lambda_dict['OtrPI_lambda2'], lambda_dict['OtrAs_lambda2']
    ])
    return lambda_array

def cargar_1_AR(file_path):
    df = pd.read_csv(file_path)
    White_1_AR = df['Wh.Gail'].values.reshape(-1, 2)
    Black_1_AR = df['AA.CARE'].values.reshape(-1, 2)
    Hspnc_1_AR = df['HU.Gail'].values.reshape(-1, 2)
    Other_1_AR = df['NA.Gail'].values.reshape(-1, 2)
    FHspnc_1_AR = df['HF.Gail'].values.reshape(-1, 2)
    Asian_1_AR = df['Asian.AABCS'].values.reshape(-1, 2)
    repeated_Asian_1_AR = np.tile(Asian_1_AR, (6, 1))
    all_1_AR = np.concatenate((White_1_AR, Black_1_AR, Hspnc_1_AR, Other_1_AR, FHspnc_1_AR, repeated_Asian_1_AR))
    return all_1_AR

def absolute_riskreal(file_path, file_path2, file_path3, file_path4, data, Raw_Ind=1, Avg_White=0):
    #print("Iniciando cálculo de absolute_riskreal")
    Wrk_lambda1_all = cargar_lambda1(file_path)
    Wrk_lambda2_all = cargar_lambda2(file_path2)
    Wrk_1_AR_all = cargar_1_AR(file_path3)
    AbsRisk = np.repeat(np.nan, data.shape[0])

    check_cov = recode_check(data, Raw_Ind)
    #print(f"check_cov: {check_cov}")
    Error_Ind = check_cov.Error_Ind.values.copy()
    IDwoERR = np.argwhere(Error_Ind == 0).T[0]

    for i in IDwoERR:
        obs = data.loc[i]
        RR_Star = relative_risk(file_path4, data, Raw_Ind)
        rrstar1 = RR_Star.RR_Star1[i]
        rrstar2 = RR_Star.RR_Star2[i]
        One_AR_RR = np.repeat(np.nan, 70)
        Strt_Intvl = int(np.floor(obs['T1']) - 20 + 1)
        End_Intvl = int(np.ceil(obs['T2']) - 20)
        NumbrIntvl = int(np.ceil(obs['T2']) - np.floor(obs['T1']))
        RskWrk = 0
        Cum_lambda = 0
        lambda1_temp = np.zeros((14, 5))
        lambda2_temp = np.zeros((14, 5))

        if Avg_White == 0:
            One_AR1 = Wrk_1_AR_all[int(obs['Race']) - 1, 0]
            One_AR2 = Wrk_1_AR_all[int(obs['Race']) - 1, 1]
            One_AR_RR1 = One_AR1 * rrstar1
            One_AR_RR2 = One_AR2 * rrstar2
            One_AR_RR[0:30] = One_AR_RR1
            One_AR_RR[30:70] = One_AR_RR2
            for v in range(lambda1_temp.shape[1]):
                lambda1_temp[:, v] = Wrk_lambda1_all[int(obs['Race']) - 1, :]
                lambda2_temp[:, v] = Wrk_lambda2_all[int(obs['Race']) - 1, :]
            lambda1 = lambda1_temp.flatten()
            lambda2 = lambda2_temp.flatten()

        for j in range(NumbrIntvl):
            j_intvl = Strt_Intvl + j - 1
            if NumbrIntvl > 1 and 0 < j < NumbrIntvl - 1:
                IntgrlLngth = 1
            elif NumbrIntvl > 1 and j == 0:
                IntgrlLngth = 1 - float(obs['T1'] - np.floor(obs['T1']))
            elif NumbrIntvl > 1 and j + 1 == NumbrIntvl:
                IntgrlLngth = float(obs['T2'] - np.floor(obs['T2'])) if obs['T2'] > np.floor(obs['T2']) else 1
            else:
                IntgrlLngth = float(obs['T2'] - obs['T1'])

            lambdaj = lambda1[j_intvl] * One_AR_RR[j_intvl] + lambda2[j_intvl]
            PI_j = ((One_AR_RR[j_intvl] * lambda1[j_intvl] / lambdaj) * np.exp(-Cum_lambda)) * (1 - np.exp(-lambdaj * IntgrlLngth))
            RskWrk += PI_j
            Cum_lambda += lambdaj * IntgrlLngth

        AbsRisk[i] = 100 * RskWrk
        #print(f"AbsRisk[{i}]: {AbsRisk[i]}")

    return AbsRisk

def corregir_datos(data):
    data_corregida = data.copy()
    mask_biopsia = (data_corregida['N_Biop'] == 0) & (data_corregida['HypPlas'] != 99)
    if mask_biopsia.any():
        print("Corrigiendo HypPlas a 99 donde N_Biop es 0.")
    data_corregida.loc[mask_biopsia, 'HypPlas'] = 99

    mask_age1st_men = data_corregida['Age1st'] < data_corregida['AgeMen']
    if mask_age1st_men.any():
        print("Corrigiendo Age1st a NaN donde Age1st es menor que AgeMen.")
    data_corregida.loc[mask_age1st_men, 'Age1st'] = np.nan

    mask_age1st_t1 = data_corregida['Age1st'] > data_corregida['T1']
    if mask_age1st_t1.any():
        print("Corrigiendo Age1st a NaN donde Age1st es mayor que T1.")
    data_corregida.loc[mask_age1st_t1, 'Age1st'] = np.nan

    if not (20 <= data_corregida['T1'].iloc[0] < 90 and 20 <= data_corregida['T2'].iloc[0] <= 90 and data_corregida['T1'].iloc[0] < data_corregida['T2'].iloc[0]):
        print("Corrigiendo T1 y T2 para cumplir con las condiciones de rango y orden.")
        if not (20 <= data_corregida['T1'].iloc[0] < 90):
            data_corregida['T1'] = np.clip(data_corregida['T1'], 20, 89)
        if not (20 <= data_corregida['T2'].iloc[0] <= 90):
            data_corregida['T2'] = np.clip(data_corregida['T2'], 20, 90)
        if data_corregida['T1'].iloc[0] >= data_corregida['T2'].iloc[0]:
            data_corregida['T2'] = data_corregida['T1'] + 5

    mask_race_invalid = ~data_corregida['Race'].isin(range(1, 12))
    if mask_race_invalid.any():
        print("Corrigiendo valores inválidos en Race.")
    data_corregida.loc[mask_race_invalid, 'Race'] = np.nan

    return data_corregida
