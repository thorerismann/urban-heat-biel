Summer Days & Tropical Nights Visualization
---
## Overview

Analyze the distribution of **Summer Days** and **Tropical Nights** based on customizable temperature thresholds.

- **Summer Days**: Days where the **daily max temperature** exceeds **30 °C**.
  - $T_{max} > 30$ 
- **Tropical Nights**: Nights where the **daily min temperature** exceeds **20 °C**.
  - $T_{min} > 20$
- These are the default thresholds used, the distribution and magnitude can change signficantly if different threhsolds are used. Feel free to explore !
- Both of these are **common indicators** used by organizations ranging from **The Lancet** to **MeteoSwiss** for understanding the impacts of heatwaves and climate change.

---

## Notes on the Data

### Temperature Bias
- **Daytime Bias**: A consistent **1 - 1.5 °C bias** is often observed during the day.
- **Nighttime Bias**: The nighttime bias is typically smaller but can reach up to **0.5 °C**.

### Missing Data
- Several stations have incomplete data, which may affect the results:
  - **Notable Stations**: 230, 231, 239, 214, and 240.
  - **Critical Gaps**: Station **230** lacks data during the **crucial summer heatwave period**, when most tropical nights and many summer days occurred.

---

## Visualization Features

1. **Interactive Map**:
   - Displays the total number of **summer days** or **tropical nights** at each station.
   - Stations are color-coded based on their exceedance counts.

2. **Histogram**:
   - Shows the distribution of exceedance counts across all stations.
   - Highlights the variability in the number of days exceeding the chosen threshold.

3. **Adjustable Thresholds**:
   - Thresholds can be adjusted dynamically using a slider to explore different definitions of **summer days** and **tropical nights**.

---


