# Foods Vendor Analytics System

## Project Overview
An ETL and analytics system for a Foods' B2B platform that processes vendor order data to provide actionable business insights.

### Business Context
- Processes data for 140,000+ small retailers
- Handles 12,000+ deliveries
- Works with 1,000+ farmers
- Supports Soko Yetu (super app) and Soko Loan (BNPL)

## Features
1. **ETL Pipeline**
   - Data extraction from CSV sources
   - Data transformation and cleaning
   - Loading into SQLite database
   - Automated processing

2. **Analytics Capabilities**
   - Location performance analysis
   - Daily sales trends
   - Payment method distribution
   - Product performance metrics

3. **Visualizations**
   - Sales by location charts
   - Daily trends analysis
   - Payment method distribution
   - Product revenue analysis

## Technical Stack
- Python 3.8+
- Pandas & NumPy for data processing
- SQLite3 for database
- Matplotlib & Seaborn for visualization

## Project Structure
```
TWIGA_VENDOR_ANALYTICS/
├── data/               # Data files
├── db/                # Database
├── reports/           # Generated visualizations
└── src/              # Source code
```

## Setup Instructions
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```
3. Run the pipeline:
   ```bash
   python src/generate_sample_data.py
   python src/etl_pipeline.py
   python src/analysis_script.py
   ```

## Business Impact
1. **Operational Efficiency**
   - Track order patterns
   - Optimize delivery locations
   - Monitor product demand

2. **Vendor Management**
   - Identify top-performing vendors
   - Analyze location performance
   - Track vendor preferences

3. **Business Growth**
   - Data-driven expansion decisions
   - Product performance insights
   - Market penetration analysis

4. **Financial Planning**
   - Payment pattern analysis
   - Sales trend monitoring
   - BNPL optimization

## Future Enhancements
- Real-time data processing
- Predictive analytics
- Mobile app integration
- Advanced security features

## Contact Information
[Your Name]
[Your Email]
[Project Repository Link]
