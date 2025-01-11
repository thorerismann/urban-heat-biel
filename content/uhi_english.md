## Urban Heat Island (UHI) and City Index Calculations

- The **UHI** is calculated by subtracting each station's temperature from the temperature at the rural reference station:
  - In **Biel** the rural reference is  Logger 206 and in **Bern:** the rural reference is Logger 98.
  - These stations have a UHI of **0** as they are the reference points.
  - Results may differ if a different rural reference station is chosen.

For every station i, the formula is: $UHI_i = T_i - T_{206}$

- The **City Index** is calculated by subtracting the mean temperature of all stations (including rural reference and forest sensors) from each station's temperature.
For every station i, the formula is $CI_i = T_i - T_{avg}$
- 
## Time Periods
- **Bern:** Data covers the period from **May 15th to September 15th, 2022**.
- **Biel:** Data covers the same dates in **2023**.

## Observational Notes
- The center of the city is relatively **over-sampled** in both Bern and Biel, potentially biasing the results toward urban areas.