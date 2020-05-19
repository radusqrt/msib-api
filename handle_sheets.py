import pandas as pd


def handle_df(df):
    df = df[df['Iti place'] == 'DA']

    dfs = {}
    dfs['angio'] = df[(df['Antiangiogeneza'] == 'DA')
                      | (df['Angiogeneza'] == 'DA')]
    dfs['regenerare'] = df[df['Regenerare'] == 'DA']
    dfs['microbiom'] = df[df['Microbiom'] == 'DA']
    dfs['adn'] = df[df['ADN'] == 'DA']
    dfs['imunitate'] = df[df['Imunitate'] == 'DA']

    try:
        sampled_dfs = {key: dfs[key].sample(3) for key in dfs}
    except:
        return "E nevoie de cel puțin trei alimente din fiecare tip", 400

    response = {key: [sampled_dfs[key].iloc[idx].to_dict()
                      for idx in range(sampled_dfs[key].shape[0])] for key in sampled_dfs}

    return response


def handle_xlsx(filename):
    df = list(pd.read_excel(filename, sheet_name=None).values())[0]
    return handle_df(df), 200


def handle_csv(filename):
    df = pd.read_csv(filename)
    return handle_df(df), 200
