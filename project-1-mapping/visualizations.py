import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

class EdTechVisualizer:
    """
    Creates interactive visualizations of EdTech ecosystem data
    """
    
    def __init__(self, data_path='data/edtech_organizations_clean.csv'):
        """
        Initialize the visualizer
        
        Args:
            data_path: Path to the cleaned CSV file
        """
        self.data_path = data_path
        self.df = None
        self.output_dir = 'outputs'
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
    def load_data(self):
        """Load cleaned data"""
        print("Loading data for visualization...")
        try:
            self.df = pd.read_csv(self.data_path)
            print(f"✅ Loaded {len(self.df)} organizations")
            return self.df
        except FileNotFoundError:
            print(f"❌ Error: File not found at {self.data_path}")
            print("💡 Tip: Make sure to run data_collector.py first!")
            return None
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def create_interactive_map(self):
        """Create interactive geographic map of EdTech organizations"""
        if self.df is None:
            print("❌ No data loaded. Run load_data() first.")
            return None
        
        print("\n📍 Creating interactive map...")
        
        # Define color scheme for funding stages
        color_map = {
            'Seed': '#FFA07A',
            'Series A': '#98D8C8',
            'Series B': '#6CB4EE',
            'Series C': '#4169E1',
            'Series D': '#0047AB',
            'Late Stage': '#002366',
            'Public': '#FFD700',
            'Private Equity': '#8B008B',
            'Acquired': '#A9A9A9'
        }
        
        # Create the map
        fig = px.scatter_mapbox(
            self.df,
            lat='Latitude',
            lon='Longitude',
            hover_name='Organization',
            hover_data={
                'Country': True,
                'City': True,
                'Category': True,
                'Funding stage': True,
                'Total funding (€)': ':,.0f',
                'Employee count': ':,.0f',
                'Founded year': True,
                'Latitude': False,
                'Longitude': False
            },
            color='Funding stage',
            color_discrete_map=color_map,
            size='Total funding (€)',
            size_max=25,
            zoom=3,
            center={'lat': 50, 'lon': 10},
            title='European EdTech Ecosystem Map',
            height=700
        )
        
        # Update layout
        fig.update_layout(
            mapbox_style='carto-positron',
            margin={'r': 0, 't': 50, 'l': 0, 'b': 0},
            font=dict(family='Arial', size=12),
            legend=dict(
                title='Funding Stage',
                orientation='v',
                yanchor='top',
                y=0.99,
                xanchor='left',
                x=0.01,
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='rgba(0, 0, 0, 0.2)',
                borderwidth=1
            )
        )
        
        # Save to HTML
        output_path = os.path.join(self.output_dir, 'map_visualization.html')
        fig.write_html(output_path)
        print(f"✅ Map saved to: {output_path}")
        
        return fig
    
    def create_funding_chart(self):
        """Create bar chart of funding by country"""
        if self.df is None:
            print("❌ No data loaded. Run load_data() first.")
            return None
        
        print("\n💰 Creating funding analysis chart...")
        
        # Calculate funding by country
        funding_by_country = self.df.groupby('Country').agg({
            'Total funding (€)': 'sum',
            'Organization': 'count'
        }).sort_values('Total funding (€)', ascending=False).head(15)
        
        funding_by_country.columns = ['Total Funding (€)', 'Number of Organizations']
        funding_by_country = funding_by_country.reset_index()
        
        # Create bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=funding_by_country['Country'],
            y=funding_by_country['Total Funding (€)'],
            text=funding_by_country['Total Funding (€)'],
            texttemplate='€%{text:,.0f}M',
            textposition='outside',
            marker=dict(
                color=funding_by_country['Total Funding (€)'],
                colorscale='Blues',
                showscale=False
            ),
            hovertemplate='<b>%{x}</b><br>' +
                         'Total Funding: €%{y:,.0f}<br>' +
                         '<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title='Total EdTech Funding by Country (Top 15)',
            xaxis_title='Country',
            yaxis_title='Total Funding (€)',
            height=600,
            font=dict(family='Arial', size=12),
            plot_bgcolor='rgba(240, 240, 240, 0.5)',
            hovermode='x unified',
            margin=dict(t=80, b=100)
        )
        
        # Rotate x-axis labels
        fig.update_xaxes(tickangle=-45)
        
        # Save to HTML
        output_path = os.path.join(self.output_dir, 'funding_chart.html')
        fig.write_html(output_path)
        print(f"✅ Funding chart saved to: {output_path}")
        
        return fig
    
    def create_category_chart(self):
        """Create pie chart of category distribution"""
        if self.df is None:
            print("❌ No data loaded. Run load_data() first.")
            return None
        
        print("\n📚 Creating category distribution chart...")
        
        # Get top 10 categories and group others
        category_counts = self.df['Category'].value_counts()
        top_10 = category_counts.head(10)
        others_count = category_counts[10:].sum()
        
        if others_count > 0:
            top_10['Others'] = others_count
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=top_10.index,
            values=top_10.values,
            hole=0.3,
            textinfo='label+percent',
            textposition='auto',
            hovertemplate='<b>%{label}</b><br>' +
                         'Organizations: %{value}<br>' +
                         'Percentage: %{percent}<br>' +
                         '<extra></extra>',
            marker=dict(
                colors=px.colors.qualitative.Set3,
                line=dict(color='white', width=2)
            )
        )])
        
        # Update layout
        fig.update_layout(
            title='EdTech Categories Distribution (Top 10 + Others)',
            height=600,
            font=dict(family='Arial', size=12),
            showlegend=True,
            legend=dict(
                orientation='v',
                yanchor='middle',
                y=0.5,
                xanchor='left',
                x=1.05
            )
        )
        
        # Save to HTML
        output_path = os.path.join(self.output_dir, 'category_chart.html')
        fig.write_html(output_path)
        print(f"✅ Category chart saved to: {output_path}")
        
        return fig
    
    def create_funding_stage_chart(self):
        """Create bar chart of organizations by funding stage"""
        if self.df is None:
            print("❌ No data loaded. Run load_data() first.")
            return None
        
        print("\n💵 Creating funding stage distribution chart...")
        
        # Count by funding stage
        stage_counts = self.df['Funding stage'].value_counts().sort_values(ascending=True)
        
        # Define colors for funding stages
        color_map = {
            'Seed': '#FFA07A',
            'Series A': '#98D8C8',
            'Series B': '#6CB4EE',
            'Series C': '#4169E1',
            'Series D': '#0047AB',
            'Late Stage': '#002366',
            'Public': '#FFD700',
            'Private Equity': '#8B008B',
            'Acquired': '#A9A9A9'
        }
        
        colors = [color_map.get(stage, '#808080') for stage in stage_counts.index]
        
        # Create horizontal bar chart
        fig = go.Figure(data=[go.Bar(
            y=stage_counts.index,
            x=stage_counts.values,
            orientation='h',
            text=stage_counts.values,
            textposition='outside',
            marker=dict(color=colors),
            hovertemplate='<b>%{y}</b><br>' +
                         'Organizations: %{x}<br>' +
                         '<extra></extra>'
        )])
        
        # Update layout
        fig.update_layout(
            title='Organizations by Funding Stage',
            xaxis_title='Number of Organizations',
            yaxis_title='Funding Stage',
            height=500,
            font=dict(family='Arial', size=12),
            plot_bgcolor='rgba(240, 240, 240, 0.5)',
            margin=dict(l=150)
        )
        
        # Save to HTML
        output_path = os.path.join(self.output_dir, 'funding_stage_chart.html')
        fig.write_html(output_path)
        print(f"✅ Funding stage chart saved to: {output_path}")
        
        return fig
    
    def create_dashboard(self):
        """Create comprehensive dashboard with all visualizations"""
        if self.df is None:
            print("❌ No data loaded. Run load_data() first.")
            return None
        
        print("\n📊 Creating comprehensive dashboard...")
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Geographic Distribution',
                'Top 10 Countries by Funding',
                'Category Distribution (Top 10)',
                'Funding Stage Distribution'
            ),
            specs=[
                [{'type': 'mapbox'}, {'type': 'bar'}],
                [{'type': 'pie'}, {'type': 'bar'}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Map (simplified for dashboard)
        funding_stage_colors = {
            'Seed': '#FFA07A',
            'Series A': '#98D8C8',
            'Series B': '#6CB4EE',
            'Series C': '#4169E1',
            'Series D': '#0047AB',
            'Late Stage': '#002366',
            'Public': '#FFD700',
            'Private Equity': '#8B008B',
            'Acquired': '#A9A9A9'
        }
        
        for stage in self.df['Funding stage'].unique():
            df_stage = self.df[self.df['Funding stage'] == stage]
            fig.add_trace(
                go.Scattermapbox(
                    lat=df_stage['Latitude'],
                    lon=df_stage['Longitude'],
                    mode='markers',
                    marker=dict(
                        size=8,
                        color=funding_stage_colors.get(stage, '#808080')
                    ),
                    name=stage,
                    text=df_stage['Organization'],
                    hovertemplate='<b>%{text}</b><br>' +
                                 f'{stage}<br>' +
                                 '<extra></extra>',
                    showlegend=True
                ),
                row=1, col=1
            )
        
        # 2. Funding by country (top 10)
        funding_by_country = self.df.groupby('Country')['Total funding (€)'].sum().sort_values(ascending=False).head(10)
        
        fig.add_trace(
            go.Bar(
                x=funding_by_country.index,
                y=funding_by_country.values,
                marker=dict(color='#4169E1'),
                showlegend=False,
                hovertemplate='<b>%{x}</b><br>' +
                             'Funding: €%{y:,.0f}<br>' +
                             '<extra></extra>'
            ),
            row=1, col=2
        )
        
        # 3. Category distribution (top 10)
        category_counts = self.df['Category'].value_counts().head(10)
        
        fig.add_trace(
            go.Pie(
                labels=category_counts.index,
                values=category_counts.values,
                marker=dict(colors=px.colors.qualitative.Set3),
                showlegend=False,
                hovertemplate='<b>%{label}</b><br>' +
                             'Count: %{value}<br>' +
                             '<extra></extra>'
            ),
            row=2, col=1
        )
        
        # 4. Funding stage distribution
        stage_counts = self.df['Funding stage'].value_counts().sort_values()
        colors = [funding_stage_colors.get(stage, '#808080') for stage in stage_counts.index]
        
        fig.add_trace(
            go.Bar(
                y=stage_counts.index,
                x=stage_counts.values,
                orientation='h',
                marker=dict(color=colors),
                showlegend=False,
                hovertemplate='<b>%{y}</b><br>' +
                             'Count: %{x}<br>' +
                             '<extra></extra>'
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text='European EdTech Ecosystem Dashboard',
            title_font_size=20,
            height=900,
            showlegend=True,
            font=dict(family='Arial', size=10),
            mapbox=dict(
                style='carto-positron',
                zoom=3,
                center={'lat': 50, 'lon': 10}
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=-0.15,
                xanchor='center',
                x=0.5
            )
        )
        
        # Update axes
        fig.update_xaxes(tickangle=-45, row=1, col=2)
        
        # Save to HTML
        output_path = os.path.join(self.output_dir, 'dashboard.html')
        fig.write_html(output_path)
        print(f"✅ Dashboard saved to: {output_path}")
        
        return fig
    
    def generate_all_visualizations(self):
        """Generate all visualizations at once"""
        print("="*60)
        print("GENERATING ALL VISUALIZATIONS")
        print("="*60)
        
        # Load data
        if self.load_data() is None:
            return False
        
        # Create all visualizations
        self.create_interactive_map()
        self.create_funding_chart()
        self.create_category_chart()
        self.create_funding_stage_chart()
        self.create_dashboard()
        
        print("\n" + "="*60)
        print("✅ ALL VISUALIZATIONS COMPLETE!")
        print("="*60)
        print(f"\n📁 Check the '{self.output_dir}' folder for all HTML files")
        print("\n📊 Generated files:")
        print("  1. map_visualization.html - Interactive map")
        print("  2. funding_chart.html - Funding by country")
        print("  3. category_chart.html - Category distribution")
        print("  4. funding_stage_chart.html - Funding stages")
        print("  5. dashboard.html - All-in-one dashboard")
        
        return True


# Main execution
if __name__ == "__main__":
    # Initialize visualizer
    visualizer = EdTechVisualizer()
    
    # Generate all visualizations
    visualizer.generate_all_visualizations()
    
    print("\n💡 Tip: Open any HTML file in your browser to view interactive visualizations!")