from argparse import RawTextHelpFormatter
from .models import *
import argparse

def main():

    header = """LAMBDA - Laboratório Multiusuário e Analise de Dados

    Júlio César Albuquerque Xavier
    Edson Luiz Folador"""

    parser = argparse.ArgumentParser(description=header,formatter_class=RawTextHelpFormatter)
    parser.add_argument('-v','--version', action='version', version='admetscore 3.3.0')

    subparsers = parser.add_subparsers(dest='tool', required=True, help="""The ADMETSCORE is a software that aims to facilitate the ADMET analysis of molecules resulting from pharmacophore research. The tool is divided into two main parts:
                                       """)

    # SDF PARSER:

    parser_sdf = subparsers.add_parser('sdf',description=header + '\n''\nThis module partitions the Pharmit docking file. This is necessary to submit each partitioned file to the ADMETlab 3.0 screening, allowing for ADMET analysis of these molecules. Each part will need to be screened individually.',formatter_class=RawTextHelpFormatter, help="""This component allows the splitting of an SDF file resulting from Pharmit Search docking (https://pharmit.csb.pitt.edu/search.html) into multiple smaller files. Each SDF file contains 299 molecules by default, though this number can be adjusted via a parameter. This splitting is necessary for screening in ADMETLab 3.0 (https://admetlab3.scbdd.com/). Users can then upload each file to the ADMETLab site and download the results, proceeding to the second component of the tool, SCORE.
  ↳  More information about the parameters: admetscore sdf -h
                                       """)
    parser_sdf.add_argument('-i', '--sdf_file', type=str, required=True, help='(required): The Pharmit docking file (SDF) that will be partitioned.\n''\n')
    parser_sdf.add_argument('-db', '--database', type=str, required=True, help='(required): The database used for docking in Pharmit. Enter the name exactly as it appears on the website. Each partition will be named with the database name and a numerical identifier\n''\n')
    parser_sdf.add_argument('-n', '--batch_number', type=int, default=299, help='(optional): Use this parameter if you want to change the number of molecules in each part. This is useful if the ADMETlab 3.0 website accepts more or fewer molecules per screening. The default is set to 300\n''\n')
    parser_sdf.add_argument('-ps', '--pharmit_score_docking', type=float, help=' (optional): Use this parameter to work with a specific docking score from Pharmit. This will reduce the number of partitions created from the SDF, as by default the entire SDF file is partitioned.\n''\n')

    # SCORE PARSER:

    parser_score = subparsers.add_parser('score',description=header+ '\n''\n''After using the SDF module and screening each partition with ADMETlab 3.0, you can then provide this module with one partition of the SDF along with the CSV result file for that partition from ADMETlab 3.0. This will create a folder named score, which will contain a spreadsheet with the ADMET analysis for each molecule in the partition. This spreadsheet assigns a score from 0 to 10 to each molecule, where a higher score indicates better performance in the ADMET analysis. The spreadsheet is cumulative and will accumulate results from each partition you process.',formatter_class=RawTextHelpFormatter, help="""This component uses the results from ADMETLab 3.0 to create an analysis spreadsheet. It assigns scores to each ADMET analysis group, weights these groups, and ranks the best molecules. Additionally, it integrates information from the SDF file downloaded from Pharmit into the spreadsheet, generating a file with details. There is also a parameter to generate a new file with only the top-performing molecules, and another parameter to adjust the weights of each group.
  ↳  More information about the parameters: admetscore score -h
                                         """)
    parser_score.add_argument('-i', '--csv_file', type=str, required=True, help='(required): The CSV file resulting from the ADMETlab 3.0 analysis of the partition to be analyzed.\n''\n')
    parser_score.add_argument('-s', '--sdf_batch_file', type=str, required=True, help='(required): The SDF partition that was analyzed by ADMETlab 3.0. The module will not accept any other partition if the CSV file does not match the corresponding ADMETlab 3.0 analysis for that partition.\n''\n')
    parser_score.add_argument('-t', '--best_hits_number', type=int, default=50, help='(optional): Specify the number of top-scoring molecules you want to view. The spreadsheet will be non-cumulative and a separate file will be created in the score folder. By default, a spreadsheet is created with the 50 best results\n''\n')


    # AUTO PARSER:

    parser_auto = subparsers.add_parser('auto',description=header+'\n''\n''After',formatter_class=RawTextHelpFormatter, help=""" Module that incorporates the functionalities of sdf and score, performing screening directly on the admetlab3.0 website
    ↳  More information about the parameters: admetscore auto -h""")

    parser_auto.add_argument('-i','--sdf_file',type=str, required=True, help='(required): The Pharmit docking file (SDF) that will be partitioned.\n''\n')
    parser_auto.add_argument('-db', '--database', type=str, required=True, help='(required): The database used for docking in Pharmit. Enter the name exactly as it appears on the website. Each partition will be named with the database name and a numerical identifier\n''\n')
    parser_auto.add_argument('-n', '--batch_number', type=int, default=299, help='(optional): Use this parameter if you want to change the number of molecules in each part. This is useful if the ADMETlab 3.0 website accepts more or fewer molecules per screening. The default is set to 300\n''\n')
    parser_auto.add_argument('-ps', '--pharmit_score_docking', type=float, help=' (optional): Use this parameter to work with a specific docking score from Pharmit. This will reduce the number of partitions created from the SDF, as by default the entire SDF file is partitioned.\n''\n')
    parser_auto.add_argument('-t', '--best_hits_number', type=int, default=None, help='(optional): Specify the number of top-scoring molecules you want to view. The spreadsheet will be non-cumulative and a separate file will be created in the score folder. By default, a spreadsheet is created with the 50 best results\n''\n')


    args = parser.parse_args()

    if args.tool == 'sdf':
        process_sdf(args.sdf_file, args.database, args.batch_number, args.pharmit_score_docking)

    elif args.tool == 'score':
        process_score(args.csv_file, args.sdf_batch_file, args.best_hits_number)
    
    elif args.tool == 'auto':
        process_auto(args.sdf_file, args.database, args.batch_number, args.pharmit_score_docking, args.best_hits_number)

def making_top_best_file(df, best_hits, output_instance):
    if best_hits is not None:
        excel_top_path = os.path.join(f'scoreadmet_{best_hits}_tops.xlsx')
        top_df = df.head(best_hits)
        output_instance.conditional_formatting(top_df, excel_top_path)
        print(f'↳ File with the {best_hits} best molecules was created\n')

def process_sdf(sdf_file, database, batch_number, pharmit_score_docking):

    sdf_instance = Sdf()
    file = sdf_instance.removing_duplicates(sdf_file,database)
    sdf_instance.process_sdf(file, database, batch_number, pharmit_score_docking)

def process_score(csv_file, sdf_batch_file, best_hits_number):

    extract_instance = Extract()
    analysis_instance = AdmetSpreadsheet()
    output_instance = Output()


    df = extract_instance.extract(csv_file, sdf_batch_file)
    print('')
    df = analysis_instance.process_data(df)
    df = output_instance.output(df)

    if best_hits_number is not None:
        making_top_best_file(df, best_hits_number, output_instance)

def process_auto(sdf_file,database,sdf_batch_file,pharmit_score_docking,best_hits_number):

    sdf_instance = Sdf()
    extract_instance = Extract()
    analysis_instance = AdmetSpreadsheet()
    output_instance = Output()
    selenium_instance = Selenium()
    csv_directory = 'admetlab3_files'
    sdf_directory = 'sdf'

    file = sdf_instance.removing_duplicates(sdf_file, database)
    sdf_instance.process_sdf(file, database, sdf_batch_file, pharmit_score_docking)
    selenium_instance.automation()
    print("Processing of sdf files on admetlab 3.0 website done\n")

    for csv_file in os.listdir(csv_directory):
        if csv_file.endswith('.csv'):

            input_file = os.path.join(csv_directory, csv_file)
            sdf_file = os.path.join(sdf_directory, csv_file.replace('.csv', '.sdf'))
            print(f'The files {input_file} and {sdf_file} have been processed')

            if os.path.exists(sdf_file):

                df = extract_instance.extract(input_file, sdf_file)
                df = analysis_instance.process_data(df)
                output_instance.output(df)
            else:
                print(f"Arquivo SDF correspondente não encontrado para {csv_file}")

    if best_hits_number is not None:
        making_top_best_file(df, best_hits_number, output_instance)

if __name__ == '__main__':
    main()