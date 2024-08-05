

def append_choice_item(choice, df):
    choice.Clear()

    for i in range(df.shape[0]):
        row = df.iloc[i]
        choice.Append(str(row.iloc[0]) + '  |  ' +  str(row.iloc[1]) + '  |  ' + str(row.iloc[2]))
    return 