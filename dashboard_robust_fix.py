# --- COPY AND PASTE THIS INTO YOUR NOTEBOOK CELL ---

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

# 1. RE-PROCESS DATA to fix the "drop_duplicates" bug
# We use 'demographics_dfs' which should be available from previous cells
if 'demographics_dfs' in locals() and demographics_dfs:
    print("🔄 Re-processing demographics data from source list...")
    merged_demographics_df = pd.concat(demographics_dfs, ignore_index=True)
    
    pct_col = "Percentage"
    # Clean percentage column
    if pct_col in merged_demographics_df.columns:
        s = merged_demographics_df[pct_col].astype(str).str.strip()
        s = s.str.extract(r'([0-9]+(?:\\.[0-9]+)?)', expand=False)
        merged_demographics_df[pct_col] = pd.to_numeric(s, errors="coerce") / 100
    
    # CRITICAL FIX: Drop duplicates using ONLY [Top Demographics, Value]
    # Previous code dropped by "Value" only, which deleted categories sharing values like "Other"
    merged_demographics_df = merged_demographics_df.drop_duplicates(subset=["Top Demographics", "Value"])
    
    print(f"✅ Data re-processed. Total rows: {len(merged_demographics_df)}")
else:
    print("⚠️ 'demographics_dfs' not found. Using existing 'merged_demographics_df' if available.")

# 2. DASHBOARD CREATION
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

if 'merged_demographics_df' in locals() and len(merged_demographics_df) > 0:
    
    # Debug: Print available categories to be sure
    available_cats = merged_demographics_df['Top Demographics'].unique()
    print(f"📊 Available Categories in Data: {available_cats}")

    # Robust Mapping: Map possible variations to 'pie'
    # This handles both "Location" and "Locations", "Company size" vs "Company distribution" etc.
    desired_charts = {
        'Job titles': 'pie',
        'Job title': 'pie',
        'Locations': 'pie',
        'Location': 'pie',
        'Industries': 'pie',
        'Industry': 'pie',
        'Companies': 'pie',
        'Company distribution': 'pie',
        'Company': 'pie',
        'Seniority': 'pie'
    }
    
    figures = []
    
    # Iterate through all available categories in the data
    for category in available_cats:
        # Check if this category is one involved in our desired list
        if category in desired_charts:
            
            category_data = merged_demographics_df[
                merged_demographics_df['Top Demographics'] == category
            ].copy()
            
            # Calculate Percentage (0.25 -> 25.0)
            if 'Percentage' in category_data.columns:
                category_data['Percentage_Pct'] = category_data['Percentage'] * 100
                
            category_data = category_data.sort_values('Percentage_Pct', ascending=False)
            top_values = category_data.nlargest(10, 'Percentage_Pct')
            
            # Always Pie chart
            fig = go.Figure()
            fig.add_trace(go.Pie(
                labels=top_values['Value'],
                values=top_values['Percentage_Pct'],
                textinfo='label+percent',
                textposition='outside',
                hovertemplate='<b>%{label}</b><br>Percentage: %{percent:.2f}%<extra></extra>'
            ))
            
            fig.update_layout(
                title=f'{category} Distribution',
                template="plotly_white",
                height=500,
                margin=dict(l=50, r=50, t=50, b=50)
            )
            
            figures.append({
                'category': category,
                'figure': fig
            })
            
    if not figures:
        print("❌ No matching categories found to plot! Check the category names above.")

    # Layout
    chart_rows = []
    for i in range(0, len(figures), 2):
        row_charts = figures[i:i+2]
        cols = []
        for fig_data in row_charts:
            cols.append(dbc.Col([
                dbc.Card([dbc.CardBody([
                    dcc.Graph(figure=fig_data['figure'], id=f"chart-{i}")
                ])], className="mb-4")
            ], width=6))
        while len(cols) < 2:
            cols.append(dbc.Col([], width=6))
        chart_rows.append(dbc.Row(cols))
    
    app.layout = dbc.Container([
        dbc.Row([dbc.Col([html.H1("LinkedIn Demographics Dashboard", className="text-center mb-4 mt-4"), html.Hr()])]),
        *chart_rows
    ], fluid=True)
    
    try:
        app.run(host='127.0.0.1', port=8050, debug=False)
    except Exception as e:
        print(f"Server error: {e}")

else:
    print("❌ No data available to plot.")
