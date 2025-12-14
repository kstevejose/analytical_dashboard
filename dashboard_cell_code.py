from dash import Dash, dcc, html
import dash_bootstrap_components as dbc  # pyright: ignore[reportMissingImports]
import plotly.graph_objects as go
import plotly.express as px

# Create Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Check if demographics data exists
if 'merged_demographics_df' in locals() and len(merged_demographics_df) > 0:
    # Define chart type mapping - FORCE PIE CHARTS for requested categories
    chart_type_mapping = {
        'Job titles': 'pie',
        'Locations': 'pie',
        'Industries': 'pie',
        'Seniority': 'pie',
        'Companies': 'pie'
    }
    
    # Get unique demographics categories
    all_categories = merged_demographics_df['Top Demographics'].unique()
    
    # Filter for requested categories ONLY
    target_categories = ['Job titles', 'Locations', 'Industries', 'Companies', 'Seniority']
    
    # Filter available categories to match targets
    demographics_categories = [c for c in all_categories if c in target_categories]
    
    # Create figures for each category with specified chart types
    figures = []
    
    for idx, category in enumerate(demographics_categories):
        category_data = merged_demographics_df[
            merged_demographics_df['Top Demographics'] == category
        ].copy()
        
        # Convert percentage to percentage format
        if 'Percentage' in category_data.columns: 
             # Check if already converted or not (notebook logic varies, assuming decimal based on previous code)
             # In the notebook it was: merged_demographics_df[pct_col] = pd.to_numeric(s) / 100
             category_data['Percentage_Pct'] = category_data['Percentage'] * 100
        
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
    # Arrange charts in a grid: 2 columns
    chart_rows = []
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
        # If odd number of charts, add empty column to maintain layout
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
    
    # Run the app
    print("✅ Dash app created successfully!")
    print("\n" + "="*60)
    print("🚀 Starting Dash server...")
    print("="*60)
    print("\n🌐 Dashboard URL: http://127.0.0.1:8050")
    print("📊 Open this URL in your browser to view the dashboard")
    print("⚠️  This cell will keep running to serve the dashboard")
    print("   To stop the server, interrupt the kernel (Kernel > Interrupt)\n")
    print("="*60 + "\n")
    
    try:
        app.run(host='127.0.0.1', port=8050, debug=False)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n❌ Port 8050 is already in use!")
            print("   Try stopping any other Dash apps or use a different port.")
        else:
            print(f"\n❌ Error starting server: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
    
else:
    print("Demographics data not found. Please run the demographics processing cells first.")
