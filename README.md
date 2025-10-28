# Amazon HydroViewer 🌍💧

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Shiny](https://img.shields.io/badge/Shiny-Python-orange.svg)](https://shiny.posit.co/py/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-available-brightgreen.svg)](https://blackteacatsu.github.io/dokkuments/)

> An interactive web-based visualization platform for exploring hydrometeorological forecasts and climatology across the Amazon Basin using ensemble-based Land Data Assimilation System (LDAS) outputs.

## 🌟 Overview

Amazon HydroViewer is a professional-grade Shiny for Python dashboard that provides real-time access to monthly meteorological and hydrological forecasts for the Amazon basin. Built on outputs from a Land Data Assimilation System, the application enables researchers, decision-makers, and stakeholders to visualize and analyze spatiotemporal patterns in key hydrometeorological variables.

The system is based on the framework described in [Recalde et al. (2022)](https://doi.org/10.1175/JHM-D-21-0081.1), with ongoing development and maintenance by Dr. Prakrut Kansara and visualizations designed by Kris Su under the direction of [Dr. Benjamin Zaitchik](https://eps.jhu.edu/directory/benjamin-zaitchik/) at Johns Hopkins University.

## ✨ Key Features

### 📊 Interactive Visualizations
- **Interactive Heatmap**: Spatially-resolved probabilistic forecasts displayed on an interactive map of the Amazon Basin using HydroBASINS Level 5 watersheds
- **Ensemble Box Plots**: Statistical distribution of ensemble forecasts with climatological reference lines
- **Time-series Animation**: Temporal evolution of forecasts with an animated slider
- **Click-based Exploration**: Interactive polygon selection for region-specific zonal statistics

### 🌡️ Supported Variables
The dashboard supports visualization of the following hydrometeorological variables:

| Variable | Description | Units |
|----------|-------------|-------|
| **Precipitation** | Rainfall rate | mm/day |
| **Air Temperature** | Near-surface air temperature | °C |
| **Specific Humidity** | Atmospheric moisture content | g/kg |
| **Evapotranspiration** | Combined evaporation and transpiration | mm/day |
| **Surface Runoff** | Water flow over land surface | mm/day |
| **Soil Moisture** | Volumetric soil water content (4 depth levels) | m³/m³ |
| **Soil Temperature** | Subsurface temperature (4 depth levels) | °C |

**Soil Profile Depths:**
- 0–10 cm (surface)
- 10–40 cm (shallow)
- 40–100 cm (intermediate)
- 100–200 cm (deep)

### 📈 Probabilistic Forecasting
- **Tercile-based Probability Categories**: Forecasts classified into Below Normal, Near Normal, and Above Normal categories
- **Ensemble Spread Visualization**: Full ensemble distribution displayed as box plots with median, quartiles, and outliers
- **Climatological Context**: Historical climatology overlaid for anomaly assessment
- **Exceedance Probabilities**: Maximum probability exceedance across tercile categories

### 🗺️ Spatial Coverage
- **Region**: Amazon Basin and surrounding areas
- **Spatial Resolution**: HydroBASINS Level 5 watershed delineation
- **Interactive Selection**: Click-to-select functionality for individual watersheds
- **Zonal Statistics**: Pre-computed regional averages for rapid visualization

## 🛠️ Technology Stack

### Core Framework
- **[Shiny for Python](https://shiny.posit.co/py/)**: Reactive web application framework
- **[Plotly](https://plotly.com/python/)**: Interactive scientific visualizations
- **[Shinywidgets](https://github.com/posit-dev/py-shinywidgets)**: Integration between Shiny and Plotly

### Data Processing
- **[xarray](https://xarray.dev/)**: NetCDF data handling and multidimensional arrays
- **[pandas](https://pandas.pydata.org/)**: Tabular data manipulation
- **[NumPy](https://numpy.org/)**: Numerical computing
- **[NetCDF4](https://unidata.github.io/netcdf4-python/)**: Network Common Data Form I/O

### Geospatial Tools
- **[GeoPandas](https://geopandas.org/)**: Geographic data manipulation
- **[regionmask](https://regionmask.readthedocs.io/)**: Spatial masking and region definition
- **GeoJSON**: Watershed boundary visualization

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection for accessing remote data

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AmazonHydroViewer.git
   cd AmazonHydroViewer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   shiny run app.py
   ```

4. **Access the dashboard**

   Open your web browser and navigate to `http://localhost:8000`

### Docker Deployment (Optional)
```bash
# Build the Docker image
docker build -t amazon-hydroviewer .

# Run the container
docker run -p 8000:8000 amazon-hydroviewer
```

## 📖 Usage Guide

### Basic Workflow

1. **Select a Variable**: Choose from meteorological or hydrological variables in the sidebar
2. **Choose Depth** (if applicable): For soil variables, select the desired depth profile
3. **Navigate Time**: Use the time slider to explore different forecast lead times
4. **Explore Regions**: Click on watershed polygons to view detailed ensemble statistics
5. **Analyze Trends**: Compare forecast distributions against climatological means

### Understanding the Visualizations

#### Heatmap Panel
- Displays tercile probability exceedance across the Amazon Basin
- Three color schemes represent Below Normal (Blues), Near Normal (Oranges), and Above Normal (Reds)
- Values range from 40–100% probability

#### Ensemble Box Plot Panel
- Shows full ensemble spread for the selected watershed
- Box represents interquartile range (25th–75th percentile)
- Whiskers extend to data extremes (excluding outliers)
- Black dashed line indicates historical climatology
- Mean value displayed as a line within each box

## 📊 Data Sources

### Forecast Data
- **Source**: Amazon LDAS ensemble forecasting system
- **Repository**: [Amazon-ARCHive GitHub](https://github.com/Amazon-ARCHive/amazon_hydroviewer_backend)
- **Update Frequency**: Monthly
- **Format**: NetCDF probabilistic tercile forecasts

### Climatology Data
- **Source**: Historical LDAS hindcast simulations
- **Time Period**: Multi-decadal reference period
- **Format**: CSV zonal statistics by watershed

### Spatial Boundaries
- **Dataset**: HydroBASINS Level 5
- **Source**: HydroSHEDS project
- **Format**: GeoJSON
- **Coverage**: South American Amazon Basin

## 🏗️ Project Structure

```
AmazonHydroViewer/
│
├── app.py                      # Main Shiny application entry point
├── shared.py                   # Shared configuration and constants
├── requirements.txt            # Python dependencies
├── styles.css                  # Custom CSS styling
│
├── modules/
│   ├── interface.py           # UI components and callbacks
│   └── mapping.py             # Data retrieval and processing functions
│
└── README.md                  # Project documentation
```

## 🤝 Contributing

We welcome contributions from the community! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style conventions
- Add docstrings to functions and classes
- Update documentation for new features
- Test thoroughly before submitting PRs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Development Team**: Dr. Prakrut Kansara (System Maintenance), Kris Su (Visualization Design)
- **Principal Investigator**: [Dr. Benjamin Zaitchik](https://eps.jhu.edu/directory/benjamin-zaitchik/), Johns Hopkins University
- **Original Framework**: Based on [Recalde et al. (2022)](https://doi.org/10.1175/JHM-D-21-0081.1)
- **Funding**: SERVIR Amazon Program
- **Data Infrastructure**: Amazon-ARCHive backend system

## 📞 Contact & Support

- **Documentation**: [https://blackteacatsu.github.io/dokkuments/](https://blackteacatsu.github.io/dokkuments/)
- **Data Repository**: [https://github.com/Amazon-ARCHive/amazon_hydroviewer_backend](https://github.com/Amazon-ARCHive/amazon_hydroviewer_backend)
- **Issues**: Please use the GitHub Issues tracker for bug reports and feature requests
- **Questions**: Direct inquiries to [Dr. Benjamin Zaitchik](https://eps.jhu.edu/directory/benjamin-zaitchik/)

## 📚 Citation

If you use this tool in your research, please cite:

```bibtex
@article{recalde2022,
  title={Original LDAS Framework},
  author={Recalde, et al.},
  journal={Journal of Hydrometeorology},
  year={2022},
  doi={10.1175/JHM-D-21-0081.1}
}
```

---

**Made with ❤️ on 🌎**