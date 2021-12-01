import os

import pandas as pd
from scrapy.utils.project import get_project_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_list_of_inns():
    settings = get_project_settings()
    input_file = os.path.join(os.path.join(settings.get('BASE_DIR'),
                                           'input'), 'inns.txt')
    with open(input_file, 'r') as file:
        incoming_inns = file.read().splitlines()
    return incoming_inns


def results_to_csv():
    engine = create_engine(get_project_settings().get('CONNECTION_STRING'))
    session = sessionmaker()
    session.configure(bind=engine)
    session = session()

    reestr_df = pd.read_sql_table('reestr', engine)
    certificates_df = pd.read_sql_table('certificates', engine)
    registration_dates_df = pd.read_sql_table('registration_dates', engine)
    rights_df = pd.read_sql_table('rights', engine)
    dfs = [reestr_df, registration_dates_df, rights_df, certificates_df]

    final_df = dfs[0]
    for df_ in dfs[1:]:
        df_.set_index('uid', inplace=True)
        df_.drop(columns=['id'], inplace=True)
        final_df = final_df.merge(df_, on='uid',
                                  how='right')

    final_df.reset_index(inplace=True)
    final_df.index = final_df.index + 1
    final_df.drop(columns=['uid', 'full_name_of_sro_member', 'ogrn',
                           'comments'],
                  inplace=True)

    new_columns_names = ['№ п/п',
                         'Сокращенное наименование члена СРО',
                         'ИНН',
                         'Статус',
                         'Тип',
                         'Рег. Номер СРО',
                         'Дата регистрации в реестре',
                         'Дата прекращения членства в СРО',
                         'Стоимость работ по одному договору подряда',
                         'Размер обязательств по договорам подряда',
                         'Дата',
                         'статус',
                         'номер свидетельства',
                         'дата выдачи',
                         'стоимость работ по одному ГП',
                         'Статус действия свидетельства']

    final_df.columns = new_columns_names
    final_df.set_index('№ п/п', inplace=True)

    base_dir = get_project_settings().get('BASE_DIR')
    final_csv_path = os.path.join(os.path.join(base_dir, 'output'),
                                  'reestr.csv')

    with open(final_csv_path, 'wb') as file:
        final_df.to_csv(path_or_buf=file)
