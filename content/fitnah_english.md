The FITNAH data comes from a **10x10 meter raster grid** of Urban Heat Island (UHI) data at 5:00 AM, modeled by the German company **Geonet** under commission by the **Canton of Bern**.

## Data Overview
The model provides:
1. **UHI Space (fitnah_ss)**: UHI data for open spaces.
2. **UHI Street (fitnah_sv)**: UHI data for streets.
3. **Temperature Layer**: Used to calculate the UHI layers.

The **UHI Space** and **UHI Street** layers are publicly available, while the temperature layer is proprietary. For more details, see my thesis or consult Geonet's reports, which are available for numerous Swiss cantons.

## Data Aggregation
For each station, raster data from the surrounding area (within a defined buffer) is aggregated using:
- **Min**, **Max**, **Mean**, **Median**, and **Count**.

The **Count** is particularly important because the UHI Space and UHI Street layers often have limited valid cells.

This aggregation is useful for comparing the **empirical data** from stations to the **modeled UHI data**.

## Zoom Note
Note that you have to zoom in to see the 10 meter buffers - it may look like nothing is appearing !