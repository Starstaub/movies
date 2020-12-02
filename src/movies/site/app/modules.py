def get_results(df, choice, search_query):

    results = df[df[choice] == search_query]
    if results.empty:
        print("No such movie in our database.")
    return
