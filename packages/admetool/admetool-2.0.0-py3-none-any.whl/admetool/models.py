from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from rdkit import Chem, RDLogger
from selenium import webdriver
import pandas as pd
import threading
import tempfile
import shutil
import time
import json
import sys
import os

class Sdf:
    '''receives the sdf file from the docking result made on the pharmit website, and divides it into several sdfs to be uploaded at a time to admetlab3.0'''

    def removing_duplicates (self,input_file, database,):
        '''removes duplicates from the original sdf before going to the split function, so the final amount of files is smaller and more efficient'''
        # This part reads the sdf and creates a temporary sdf to place unique molecules, without duplicates.
        with open(input_file,'r') as file, tempfile.NamedTemporaryFile(mode='w',delete=False,suffix='.sdf')as temp_sdf:
            molecules = set()
            current_molecule = []
            write_molecule = False

            for line in file:
                if line.startswith(database):
                    mol_id = line.strip()
                    if mol_id not in molecules:
                        molecules.add(mol_id)
                        write_molecule = True
                    else:
                        write_molecule = False
                if write_molecule:
                    current_molecule.append(line)
                if line.startswith('$$$$'):
                    if write_molecule:
                        temp_sdf.writelines(current_molecule)
                    current_molecule = []
            temp_file_name = temp_sdf.name

        # The function returns the temporary file to be split
        return temp_file_name

    def save_batch(self, batch, database, index):
        '''Function that will be used in process sdf to save each division in files'''
        with open(os.path.join("sdf", f"{database}_{index:04d}.sdf"), 'w') as f:
            f.writelines(batch)

    def process_sdf(self, input_file, database, batch_size, affinity_cutoff=None):
        '''function that will create the folder called sdf to place the divisions of the original sdf there, it will give the possibility of filtering through pharmitscoredocking, in addition to giving the option to change the amount of molecules in each division'''
    
        if os.path.exists("sdf"):
            existing_files = [f for f in os.listdir("sdf") if f.startswith(database)]
            if existing_files:
                return print(f'There are already {database} files in the folder.\n')
        else:
            os.makedirs("sdf")
        try:
            with open(input_file, 'r') as file:
                lines = file.readlines()
        except:
            return print('\nFILE NOT FOUND\n')

        current_molecule = []
        current_affinity = None
        first_database_name = None

        batch = []
        file_index = 1
        molecule_count = 0

        for i, line in enumerate(lines):
            if not current_molecule:
                first_database_name = line.split()[0] if line.strip() else None
                if first_database_name:
                    current_molecule.append(first_database_name + '\n')
            else:
                current_molecule.append(line)

            if line.startswith('>  <minimizedAffinity>'):
                current_affinity = float(lines[i + 1].strip())

            if line.strip() == '$$$$':
                if affinity_cutoff is None or (current_affinity is not None and current_affinity <= affinity_cutoff):
                    batch.extend(current_molecule)
                    molecule_count += 1

                current_molecule = []
                current_affinity = None
                first_database_name = None

                if molecule_count == batch_size:
                    self.save_batch(batch, database, file_index)
                    file_index += 1
                    batch = []
                    molecule_count = 0

        if batch:
            self.save_batch(batch, database, file_index)

        print(f"{file_index} batch(es) saved in folder 'sdf'.\n")

class AdmetSpreadsheet:
    ''' Analyzes the AdmetLab 3.0 spreadsheet '''

    def replace_interval(self, value, intervals, values):
        for interval, replaced_value in zip(intervals, values):
            if interval[0] <= value <= interval[1]:
                return replaced_value
        return value

    def replace_values(self, df, columns, intervals, values):
        replace = lambda x: self.replace_interval(pd.to_numeric(x, errors='coerce'), intervals, values)
        for col in columns:
            df[col] = df[col].apply(replace)
        return df

    def replace_string(self, value, string, value1, value2):
        return value1 if value == string else value2
    
    def normalize_values(self, value):
        if value <= 1.0:
            return float(value * 1000)
        return float(value)
    
    def rename(self,df):
        df = df.rename(columns={
            'cl-plasma': 'cl_plasma',
            't0.5': 't_0_5',
            'MCE-18': 'MCE_18',
            })
        return df

    def json_file(self):
        weights = {
            "ABSORTION": 2,
            "DISTRIBUTION": 1,
            "TOXICITY": 8,
            "TOX21_PATHWAY": 3,
            "METABOLISM": 2,
            "TOXICOPHORE_RULES": 3,
            "EXCRETION": 1,
            "MEDICINAL_CHEMISTRY": 5
        }
    
        with open('weights.json', 'w') as json_file:
            json.dump(weights, json_file, indent=4)

    def process_data(self, df, weights):
        # Opening the json with the weights for calculation
        with open('weights.json', 'r') as json_file:
            weights = json.load(json_file)

        df = self.rename(df)
        try:
            df.drop('molstr',axis=1,inplace=True)
        except:
            pass
        df_original = df.copy()

        # New columns that will be added to the analysis
        new_cols_to_move = ['SCORE', 'ABSORTION', 'DISTRIBUTION', 'TOXICITY', 'TOX21_PATHWAY', 'METABOLISM', 'TOXICOPHORE_RULES', 'EXCRETION', 'MEDICINAL_CHEMISTRY']
    
        # Absorption
        absorption_columns_float = ['PAMPA', 'pgp_inh', 'pgp_sub', 'hia', 'f20', 'f30', 'f50']
        absorption_columns_str = ['FAF-Drugs4 Rule']
        absorption_columns = absorption_columns_float + absorption_columns_str

        # Distribution
        distribution_columns = ['OATP1B1', 'OATP1B3', 'BCRP', 'BSEP', 'BBB', 'MRP1']
        toxicity_columns = ['hERG', 'hERG-10um', 'DILI', 'Ames', 'ROA', 'FDAMDD', 'SkinSen', 'Carcinogenicity', 'EC', 'EI', 'Respiratory', 'H-HT', 'Neurotoxicity-DI', 'Ototoxicity', 'Hematotoxicity', 'Nephrotoxicity-DI', 'Genotoxicity', 'RPMI-8226', 'A549', 'HEK293']
        tox21_columns = ['NR-AhR', 'NR-AR', 'NR-AR-LBD', 'NR-Aromatase', 'NR-ER', 'NR-ER-LBD', 'NR-PPAR-gamma', 'SR-ARE', 'SR-ATAD5', 'SR-HSE', 'SR-MMP', 'SR-p53']
        metabolism_columns = ['CYP1A2-inh', 'CYP1A2-sub', 'CYP2C19-inh', 'CYP2C19-sub', 'CYP2C9-inh', 'CYP2C9-sub', 'CYP2D6-inh', 'CYP2D6-sub', 'CYP3A4-inh', 'CYP3A4-sub', 'CYP2B6-inh', 'CYP2B6-sub', 'CYP2C8-inh', 'LM-human']
        toxicophore_columns = ['NonBiodegradable', 'NonGenotoxic_Carcinogenicity', 'SureChEMBL', 'Skin_Sensitization', 'Acute_Aquatic_Toxicity', 'Genotoxic_Carcinogenicity_Mutagenicity']

        # Medicinal Chemistry
        medicinal_chemistry_columns_str = ['Alarm_NMR', 'BMS', 'Chelating', 'PAINS']
        medicinal_chemistry_columns_float_divergent = ['gasa', 'QED', 'Synth', 'Fsp3', 'MCE_18', 'Lipinski', 'Pfizer', 'GSK', 'GoldenTriangle']
        medicinal_chemistry_columns_float_similar = ['Aggregators', 'Fluc', 'Blue_fluorescence', 'Green_fluorescence', 'Reactive', 'Promiscuous']
        medicinal_chemistry = medicinal_chemistry_columns_str + medicinal_chemistry_columns_float_divergent + medicinal_chemistry_columns_float_similar

        # normalization
        to_normalize = ['caco2','PPB', 'Fu','logVDss','cl_plasma', 't_0_5', 'QED', 'Synth', 'Fsp3', 'MCE_18']
        normalize = absorption_columns_float + distribution_columns + toxicity_columns + tox21_columns + metabolism_columns + medicinal_chemistry_columns_float_similar + to_normalize
        for coluna in normalize:
            df[coluna] = df[coluna].apply(self.normalize_values)

        # calculation of columns that have equal check intervals
        common_intervals = [(0, 300), (300, 700), (700, 1000)]
        replacement_values = {
            tuple(absorption_columns_float): [1.1, 0.55, 0.0],
            tuple(distribution_columns): [1.1, 0.55, 0.0],
            tuple(toxicity_columns): [0.5, 0.25, 0.0],
            tuple(tox21_columns): [0.83, 0.41, 0.0],
            tuple(metabolism_columns): [0.71, 0.35, 0.0],
            tuple(medicinal_chemistry_columns_float_similar):[0.52, 0.26, 0.0],
        }        
        for columns, values in replacement_values.items():
            df = self.replace_values(df, columns, common_intervals, values)

        # Dealing with columns that are str
        for col in toxicophore_columns:
            df[col] = df[col].apply(self.replace_string, args=("['-']", 1.66, 0))

        for col in medicinal_chemistry_columns_str:
            df[col] = df[col].apply(self.replace_string, args=("['-']", 0.5, 0))

        for col in absorption_columns_str:
            df[col] = df[col].apply(self.replace_string, args=("['-']", 1.2, 0))

        # Calculation of columns of different parameters
        df = (
            df.assign(
                caco2=pd.to_numeric(df['caco2'], errors='coerce').apply(lambda x: 1.1 if x > -5150 else 0),
                PPB=pd.to_numeric(df['PPB'], errors='coerce').apply(lambda x: 1.1 if x <= 90 else 0),
                Fu=pd.to_numeric(df['Fu'], errors='coerce').apply(lambda x: 1.2 if x >= 5 else 0),
                logVDss=pd.to_numeric(df['logVDss'], errors='coerce').apply(lambda x: 1.1 if 40 <= x <= 200 else 0),
                cl_plasma=pd.to_numeric(df['cl_plasma'], errors='coerce').apply(lambda x: 5 if 0 <= x <= 5 else (2.5 if 5 < x <= 15 else 0)),
                t_0_5=pd.to_numeric(df['t_0_5'], errors='coerce').apply(lambda x: 5 if x > 8 else (2.5 if 1 <= x <= 8 else 0)),
                Lipinski=pd.to_numeric(df['Lipinski'], errors='coerce').apply(lambda x: 0.526 if x == 0 else 0),
                Pfizer=pd.to_numeric(df['Pfizer'], errors='coerce').apply(lambda x: 0.52 if x == 0 else 0),
                GSK=pd.to_numeric(df['GSK'], errors='coerce').apply(lambda x: 0.52 if x == 0 else 0),
                GoldenTriangle=pd.to_numeric(df['GoldenTriangle'], errors='coerce').apply(lambda x: 0.5 if x == 0 else 0),
                gasa=pd.to_numeric(df['gasa'], errors='coerce').apply(lambda x: 0.52 if x == 1 else 0),
                QED=pd.to_numeric(df['QED'], errors='coerce').apply(lambda x: 0.52 if x > 670 else (0.26 if 490 <= x <= 670 else 0)),
                Synth=pd.to_numeric(df['Synth'], errors='coerce').apply(lambda x: 0.64 if x <= 6000 else 0),
                Fsp3=pd.to_numeric(df['Fsp3'], errors='coerce').apply(lambda x: 0.52 if x >= 420 else 0),
                MCE_18=pd.to_numeric(df['MCE_18'], errors='coerce').apply(lambda x: 0.52 if x >= 45000 else 0)
            ))

        # sum of columns
        new_cols = pd.DataFrame({
            'ABSORTION': df[absorption_columns + ['caco2']].sum(axis=1, skipna=True),
            'DISTRIBUTION': df[['PPB', 'Fu','logVDss'] + distribution_columns].sum(axis=1, skipna=True),
            'TOXICITY': df[toxicity_columns].sum(axis=1, skipna=True),
            'TOX21_PATHWAY': df[tox21_columns].sum(axis=1, skipna=True),
            'METABOLISM': df[metabolism_columns].sum(axis=1, skipna=True),
            'TOXICOPHORE_RULES': df[toxicophore_columns].sum(axis=1, skipna=True),
            'EXCRETION': df[['cl_plasma', 't_0_5']].sum(axis=1, skipna=True),
            'MEDICINAL_CHEMISTRY': df[medicinal_chemistry].sum(axis=1, skipna=True)
        })

        df = pd.concat([df, new_cols], axis=1)

        # calculates the average with the weights
        df['SCORE'] = (df['ABSORTION'] * weights['ABSORTION'] +
                        df['DISTRIBUTION'] * weights ['DISTRIBUTION'] +
                        df['TOXICITY'] * weights ['TOXICITY'] +
                        df['TOX21_PATHWAY'] * weights ['TOX21_PATHWAY'] +
                        df['METABOLISM'] * weights['METABOLISM'] +
                        df['TOXICOPHORE_RULES'] * weights ['TOXICOPHORE_RULES'] +
                        df['EXCRETION'] * weights['EXCRETION'] +
                        df['MEDICINAL_CHEMISTRY'] * weights['MEDICINAL_CHEMISTRY']) / sum(weights.values())

        # After use, remove the json with the weights
        os.remove('weights.json')

        df = pd.merge(df_original, df[['smiles'] + new_cols_to_move], on='smiles', how='left')

        new_cols = ['ID_Molecula', 'Afinidade'] + new_cols_to_move + ['smiles'] + [col for col in df.columns if col not in new_cols_to_move and col not in ['ID_Molecula', 'Afinidade', 'smiles']]
        
        df = df[new_cols]
        
        df[new_cols_to_move] = df[new_cols_to_move].round(2)
        
        try:
            df.drop('molstr',axis=1,inplace=True)
        except:
            pass
        
        df = self.rename(df)      
        
        for coluna in normalize:
            df[coluna] = df[coluna].apply(self.normalize_values)
        
        return df

class Extract:

    RDLogger.DisableLog('rdApp.*')

    def extract_ids_affinities_from_sdf(self, sdf_file):
        ids_affinity = []
        with Chem.SDMolSupplier(sdf_file) as suppl:
            for mol in suppl:
                if mol is not None:
                    mol_id = mol.GetProp('_Name')
                    affinity = mol.GetDoubleProp('minimizedAffinity')
                    smiles = Chem.MolToSmiles(mol)
                    ids_affinity.append((mol_id, affinity, smiles))
        df = pd.DataFrame(ids_affinity, columns=['ID_Molecula', 'Afinidade', 'smiles'])
        return df

    def extract (self,csv_file, sdf_file ):

        try:
            df_final = self.extract_ids_affinities_from_sdf(sdf_file)
        except:
            print('\nSDF NOT FOUND\n')
            sys.exit()

        try:
            df_csv = pd.read_csv(csv_file)

        except:
            print('\nCSV NOT FOUND\n')
            sys.exit()
    
        df_merged = pd.merge(df_final, df_csv, on='smiles', how='left')

        df_merged.drop_duplicates(subset=['smiles'], inplace=True)
        
        return df_merged

class Output:

    def get_column_letter(self, col_idx):
        letter = ''
        while col_idx > 0:
            col_idx, remainder = divmod(col_idx - 1, 26)
            letter = chr(65 + remainder) + letter
        return letter

    def conditional_formatting(self,df,excel_path):

        writer = pd.ExcelWriter(excel_path, engine="xlsxwriter")

        df.to_excel(writer, sheet_name="Sheet1", index=False)

        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        (max_row, max_col) = df.shape

        green_format = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})
        yellow_format = workbook.add_format({'bg_color': '#FFEB9C', 'font_color': '#9C5700'})
        red_format = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
        gray_format = workbook.add_format({'bg_color': '#D3D3D3'})
        number_format = workbook.add_format({'num_format': '0.00'})
        center_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'}) 


        columns = [49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 125, 126, 127, 128, 129, 131]

        string_columns = [32, 33, 34, 35, 117, 118, 119, 120, 121, 122, 123, 124]

        gray_columns = [0,1,11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 31, 40, 41, 42, 43, 44, 45, 46, 48, 81, 82, 83, 84, 130]

        scores_columns = [2,3,4,5,6,7,8,9,10]

        special_conditions = {
            38: [(0, 0, green_format), (1, float('inf'), red_format)],
            39: [(0, 0, green_format), (1, float('inf'), red_format)],
            26: [(1, 1, green_format), (0, 0, red_format)],
            28: [(float('-inf'), 6000, green_format), (6000.01, float('inf'), red_format)],
            36: [(float('-inf'), 0, green_format), (1, float('inf'), red_format)],
            37: [(float('-inf'), 0, green_format), (1, float('inf'), red_format)],
            47: [(-5150, float('inf'), green_format), (float('-inf'), -5150.01, red_format)],
            27: [(670, float('inf'), green_format), (490, 669.99, yellow_format), (float('-inf'), 489.99, red_format)],
            80: [(8, float('inf'), green_format), (1, 7.9, yellow_format), (float('-inf'), 0, red_format)],
            62: [(float('-inf'), 90, green_format), (90.01, float('inf'), red_format)],
            29: [(420, float('inf'), green_format), (float('-inf'), 419, red_format)],
            30: [(45000, float('inf'), green_format), (float('-inf'), 44999.99, red_format)],
            64: [(5, float('inf'), green_format), (float('-inf'), 4.99, red_format)],
            79: [(0, 5, green_format), (5.01, 15, yellow_format), (15.01, float('inf'), red_format)],
            63: [(40, 200, green_format), (float('-inf'), 39.99, red_format), (200.01, float('inf'), red_format)]
        }

        numeric_cols = df.select_dtypes(include=['number']).columns
        for col_name in numeric_cols:
            col_idx = df.columns.get_loc(col_name)
            col_letter = self.get_column_letter(col_idx + 1)
            cell_range = f'{col_letter}2:{col_letter}{max_row + 1}'
            worksheet.set_column(f'{col_letter}:{col_letter}', None, number_format)


        for col in columns:
            col_letter = self.get_column_letter(col + 1)
            cell_range = f'{col_letter}2:{col_letter}{max_row + 1}'
            
            worksheet.conditional_format(cell_range, {'type': 'cell', 'criteria': 'between', 'minimum': 0, 'maximum': 300, 'format': green_format})
            worksheet.conditional_format(cell_range, {'type': 'cell', 'criteria': 'between', 'minimum': 300.01, 'maximum': 700, 'format': yellow_format})
            worksheet.conditional_format(cell_range, {'type': 'cell', 'criteria': 'between', 'minimum': 700.01, 'maximum': 1000, 'format': red_format})



        for col in scores_columns:
            col_letter = self.get_column_letter(col + 1)
            cell_range = f'{col_letter}2:{col_letter}{max_row + 1}'
            
            worksheet.conditional_format(cell_range, {'type': 'cell', 'criteria': 'between', 'minimum': 7, 'maximum': 10, 'format': green_format})
            worksheet.conditional_format(cell_range, {'type': 'cell', 'criteria': 'between', 'minimum': 4, 'maximum': 6.9, 'format': yellow_format})
            worksheet.conditional_format(cell_range, {'type': 'cell', 'criteria': 'between', 'minimum': 0, 'maximum': 3.9, 'format': red_format})

        for col in string_columns:
            col_letter = self.get_column_letter(col + 1)
            cell_range = f'{col_letter}2:{col_letter}{max_row + 1}'

            worksheet.conditional_format(cell_range, {'type': 'text', 'criteria': 'containing', 'value': "['-']", 'format': green_format})
            worksheet.conditional_format(cell_range, {'type': 'text', 'criteria': 'not containing', 'value': "['-']", 'format': red_format})

        for col, conditions in special_conditions.items():
            col_letter = self.get_column_letter(col + 1) 
            cell_range = f'{col_letter}2:{col_letter}{max_row + 1}'

            for min_val, max_val, fmt in conditions:
                criteria = 'between'
                if min_val == float('-inf'):
                    criteria = 'less than or equal to'
                    min_val = max_val
                elif max_val == float('inf'):
                    criteria = 'greater than or equal to'
                    max_val = min_val

                worksheet.conditional_format(cell_range, {'type': 'cell', 'criteria': criteria, 'minimum': min_val, 'maximum': max_val, 'format': fmt})
    
        for col in gray_columns:
            col_letter = self.get_column_letter(col + 1)  # Adicionar 1 porque as colunas são 1-indexadas no Excel
            cell_range = f'{col_letter}2:{col_letter}{max_row + 1}'

            worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': gray_format})

        worksheet.set_column(f'{col_letter}:{col_letter}', None, workbook.add_format({'num_format': '0.00'}))

        #for col_idx in range(max_col):
        #    col_letter = self.get_column_letter(col_idx + 1)
        #    worksheet.set_column(f'{col_letter}:{col_letter}', None, center_format)

        writer.close()

    def output(self, df):

        #if ((df['SCORE'] == 0).any() or (df['ABSORTION'] == 0).any() or (df['DISTRIBUTION'] == 0).any()):
        #    print('\nInput files are not correlated\n')
        #    return None

        excel_path = os.path.join('scoreadmet.xlsx')

        if os.path.exists(excel_path):
            existing_df = pd.read_excel(excel_path, sheet_name='Sheet1')
            initial_count = len(existing_df)
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df = updated_df.sort_values(by='SCORE', ascending=False)
            updated_df.drop_duplicates(subset='smiles', keep="first", inplace=True)
            final_count = len(updated_df)
            new_entries = final_count - initial_count
            print(f'{new_entries} new molecules were added.\n')
        else:
            updated_df = df
            updated_df = updated_df.sort_values(by='SCORE', ascending=False)
            updated_df.drop_duplicates(subset='smiles', keep='first', inplace=True)
            final_count = len(updated_df)
            print(f'The spreadsheet was created with {final_count} molecules.\n')

        self.conditional_formatting(updated_df,excel_path)

        return updated_df

class Selenium:

    def wait_for_download(self, directory, timeout=600):
        end_time = time.time() + timeout
        while time.time() < end_time:
            files = [f for f in os.listdir(directory) if not f.endswith('.crdownload')]
            if files:
                return os.path.join(directory, files[0])
            time.sleep(1)
        return None

    def animate(self):
        animation = "|/-\\"
        idx = 0
        while not stop_animation:
            print(animation[idx % len(animation)], end="\r")
            idx += 1
            time.sleep(0.3)

    def automation(self):

        global stop_animation
        stop_animation = False

        animation_thread = threading.Thread(target=self.animate)
        animation_thread.start()

        print('  Starting processing on the admetlab3.0 website',end='\r')

        try:

            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            download_dir = os.path.join(os.getcwd(), 'temp')
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            options.add_experimental_option('prefs', {
                'download.default_directory': download_dir,
                'download.prompt_for_download': False,
                'download.directory_upgrade': True,
                'safebrowsing.enabled': True
            })

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

            driver.get('https://admetlab3.scbdd.com/server/screening')
            input_dir = 'sdf'
            output_dir = 'admetlab3_files'

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

            for file in files:
                file_path = os.path.join(input_dir, file)
                absolute_file_path = os.path.abspath(file_path)

                upload_element = driver.find_element(By.ID, 'molecule-file')
                upload_element.send_keys(absolute_file_path)

                print(f'  Processing the {file} file in admetlab3.0 ..',end='\r')

                submit_button = driver.find_element(By.XPATH, "//button[@class='btn btn-success' and @onclick='submit1()']")
                submit_button.click()

                download_button = WebDriverWait(driver, 999).until(
                    EC.visibility_of_element_located((By.XPATH, "//button[@class='btn btn-outline-success' and @onclick='download()']"))
                )
                print(f'Processing the {file} file in admetlab3. Done')

                print(f'  Download admet analysis of file {file} ..',end='\r')

                download_button.click()

                downloaded_file_path = self.wait_for_download(download_dir)
                if downloaded_file_path:

                    new_file_name = os.path.splitext(file)[0] + '.csv'
                    new_file_path = os.path.join(output_dir, new_file_name)
                    os.rename(downloaded_file_path, new_file_path)
                    print(f'Download completed. {new_file_path} file created\n')

                else:
                    print(f'Erro no arquivo: {file}')

                driver.get('https://admetlab3.scbdd.com/server/screening')

            driver.quit()

            shutil.rmtree(download_dir)

        finally:    
            stop_animation = True
            animation_thread.join()
            print("Processing of sdf files on admetlab 3.0 website done\n")


