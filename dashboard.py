import pandas as pd
import glob
import os
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px

def load_data():
    print("Loading data...")
    file_paths = glob.glob('Content_*.xlsx')
    if not file_paths:
        print("No 'Content_*.xlsx' files found.")
        return pd.DataFrame()

    sheet_name = "DEMOGRAPHICS"
    demographics_dfs = []

    for i, f in enumerate(file_paths):
        try:
            # Read excel file
            df = pd.read_excel(f, sheet_name=sheet_name)
            # keep header only from first file
            if i > 0:
                df = df.iloc[1:]
            demographics_dfs.append(df)
        except Exception as e:
            print(f"Error reading {f}: {e}")

    if not demographics_dfs:
        print("No demographics data loaded.")
        return pd.DataFrame()

    # Merge all demographics DataFrames
    merged_demographics_df = pd.concat(demographics_dfs, ignore_index=True)

    pct_col = "Percentage"
    # Ensure column exists and clean it
    if pct_col in merged_demographics_df.columns:
        s = merged_demographics_df[pct_col].astype(str).str.strip()
        # extract numeric part from strings like "< 1%", "23%", etc.
        s = s.str.extract(r'([0-9]+(?:\\.[0-9]+)?)', expand=False)
        # convert to decimal percentage
        merged_demographics_df[pct_col] = pd.to_numeric(s, errors="coerce") / 100
    
    # Clean duplicates based on Value
    merged_demographics_df = merged_demographics_df.drop_duplicates(subset="Value")
    
    print(f"Data loaded successfully. {len(merged_demographics_df)} rows.")
    return merged_demographics_df

def create_app(merged_demographics_df):
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # Define chart type mapping - FORCE PIE CHARTS for requested categories
    chart_type_mapping = {
        'Job titles': 'pie',
        'Locations': 'pie',
        'Industries': 'pie',
        'Seniority': 'pie',
        'Companies': 'pie'
    }

    # Get unique demographics categories
    if 'Top Demographics' not in merged_demographics_df.columns:
         print("Column 'Top Demographics' not found.")
         return app

    all_categories = merged_demographics_df['Top Demographics'].unique()
    # print(f"DEBUG: Available categories in data: {all_categories}")
    
    # Filter for requested categories ONLY
    # "job title pie chart, locatiion pie chart, industry piechart, company pie chart, seniority pie chart"
    target_categories = ['Job titles', 'Locations', 'Industries', 'Companies', 'Seniority']
    
    # Filter available categories to match targets
    demographics_categories = [c for c in all_categories if c in target_categories]
    
    print(f"Generatng charts for: {demographics_categories}")

    figures = []

    for idx, category in enumerate(demographics_categories):
        category_data = merged_demographics_df[
            merged_demographics_df['Top Demographics'] == category
        ].copy()

        # Convert percentage to percentage format (e.g. 0.25 -> 25.0)
        if 'Percentage' in category_data.columns:
            category_data['Percentage_Pct'] = category_data['Percentage'] * 100
        else:
            continue

        category_data = category_data.sort_values('Percentage_Pct', ascending=False)
        top_values = category_data.nlargest(10, 'Percentage_Pct')

        # Determine chart type (default to pie as requested)
        chart_type = chart_type_mapping.get(category, 'pie')

        if chart_type == 'pie':
            # Create pie chart
            fig = go.Figure()
            fig.add_trace(go.Pie(
                labels=top_values['Value'],
                values=top_values['Percentage_Pct'],
                textinfo='label+percent',
                textposition='outside',
                hovertemplate='<b>%{label}</b><br>Percentage: %{percent}<extra></extra>'
            ))
            fig.update_layout(
                title=f'{category} Distribution',
                template="plotly_white",
                height=500,
                margin=dict(l=50, r=50, t=50, b=50)
            )
            figures.append({
                'category': category,
                'chart_type': 'pie',
                'figure': fig
            })
            
    # Create app layout with Bootstrap components
    chart_rows = []
    # 2 columns per row
    for i in range(0, len(figures), 2):
        row_charts = figures[i:i+2]
        cols = []
        for fig_data in row_charts:
            cols.append(
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(figure=fig_data['figure'], id=f"chart-{fig_data['category']}")
                        ])
                    ], className="mb-4")
                ], width=6)
            )
        # If odd number of charts, add empty column
        while len(cols) < 2:
            cols.append(dbc.Col([], width=6))
        chart_rows.append(dbc.Row(cols))

    app.layout = dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("LinkedIn Demographics Dashboard", className="text-center mb-4 mt-4"),
                html.Hr()
            ])
        ]),
        *chart_rows
    ], fluid=True)
    
    return app

if __name__ == "__main__":
    df = load_data()
    if not df.empty:
        app = create_app(df)
        print("Starting Dash server...")
        try:
            app.run(host='127.0.0.1', port=8050, debug=True)
        except Exception as e:
            print(f"Error starting server: {e}")
    else:
        print("Failed to start dashboard due to missing data.")
