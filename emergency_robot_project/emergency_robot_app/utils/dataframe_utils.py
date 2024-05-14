import pandas as pd
def create_dataframe_from_model(model:str) -> str:
    data = model.objects.all().values()
    df = pd.DataFrame(data)
    html_table = df.to_html(classes='table table-dark table-striped')
    return html_table