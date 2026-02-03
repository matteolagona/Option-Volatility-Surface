\# Equity Index Volatility Surface Calibration  

\## A Comparative Study of Surface-Consistent SVI and SABR Models



---



\## 1. Introduction



Implied volatility surfaces play a central role in the pricing, hedging, and risk management of equity index derivatives. Market option prices exhibit pronounced volatility smiles and skews that vary across strikes and maturities, making constant-volatility models inadequate in practice.



This project focuses on the construction and calibration of implied volatility surfaces for equity index options using two widely adopted models in quantitative finance:



\- \*\*Surface-Consistent SVI (Stochastic Volatility Inspired)\*\*, a static but arbitrage-aware parameterization of implied variance surfaces.

\- \*\*SABR (Stochastic Alpha Beta Rho)\*\*, a stochastic volatility model commonly used for smile modeling at fixed maturities.



The goal is to compare these approaches from both a quantitative and structural perspective, emphasizing calibration stability, surface consistency, and practical limitations.



---



\## 2. Market Setup and Data



The underlying asset is an equity index observed under the risk-neutral measure. The market environment explicitly incorporates:



\- A deterministic risk-free rate term structure  

\- A continuous dividend yield curve  

\- Forward-based normalization of strikes  



Option data consist of a \*\*mixed dataset\*\*, combining real market observations with controlled preprocessing assumptions. Medium-dated maturities are considered, reflecting the most liquid segment of index option markets.



Strikes are expressed in terms of log-moneyness relative to the forward price:

\\\[

k = \\log\\left(\\frac{K}{F(T)}\\right)

\\]

This choice ensures consistency across maturities and removes distortions induced by carry effects.



---



\## 3. Implied Volatility Construction



Implied volatilities are recovered from observed option prices using the Black–Scholes framework with continuous dividends. A robust numerical inversion scheme is employed to ensure stability across strikes and maturities.



Data preprocessing includes:

\- Filtering of illiquid or unreliable quotes  

\- Vega-based weighting to emphasize informative regions of the smile  

\- Basic arbitrage sanity checks  



---



\## 4. Model Descriptions



\### 4.1 Surface-Consistent SVI



The SVI model parameterizes total implied variance as a function of log-moneyness. Unlike naïve smile-by-smile fitting, this project adopts a \*\*surface-consistent calibration approach\*\*, enforcing smoothness and stability across maturities while respecting static no-arbitrage constraints.



Key features:

\- Parsimonious parameterization

\- Explicit control of skew and wing behavior

\- Compatibility with arbitrage-free surface conditions



SVI is treated as a \*\*static representation\*\* of the volatility surface, designed for robustness rather than dynamic realism.



---



\### 4.2 SABR Model



The SABR model describes the joint dynamics of the forward price and its stochastic volatility. Implied volatilities are obtained via the Hagan et al. asymptotic approximation.



Key characteristics:

\- Intuitive stochastic interpretation

\- Flexible smile shapes at fixed maturities

\- Calibration performed independently for each maturity



While SABR provides valuable insight into smile dynamics, it lacks intrinsic surface consistency and may exhibit instability across maturities.



---



\## 5. Calibration Methodology



Model parameters are estimated via constrained nonlinear optimization, minimizing weighted discrepancies between market and model-implied volatilities.



The calibration framework includes:

\- Vega-weighted least squares objectives  

\- Explicit parameter constraints to promote arbitrage-free behavior  

\- Multiple initializations to mitigate local minima  



Numerical robustness and parameter stability are treated as primary objectives, not merely goodness of fit.



---



\## 6. Results and Visualization



The calibrated models are evaluated through:

\- Two-dimensional volatility smiles across maturities  

\- Three-dimensional implied volatility surfaces  

\- Residual and difference surface visualizations  



Comparative analysis highlights the trade-offs between surface smoothness, local fit accuracy, and parameter interpretability.



---



\## 7. Model Comparison and Discussion



From a structural perspective:

\- \*\*SVI\*\* excels in producing smooth, arbitrage-aware surfaces suitable for pricing and risk aggregation.

\- \*\*SABR\*\* offers strong intuition and local smile flexibility but struggles with surface-level coherence.



The comparison underscores the distinction between static surface representations and dynamically motivated smile models.



---



\## 8. Limitations and Extensions



Several limitations are acknowledged:

\- The static nature of SVI precludes dynamic hedging interpretation

\- SABR asymptotics may lose accuracy for long maturities or extreme strikes

\- Extrapolation beyond quoted strikes remains model-dependent



Potential extensions include:

\- SSVI formulations

\- Local volatility recovery

\- Joint modeling with stochastic interest rates or dividends



---



\## 9. Repository Structure



\- `src/`: reusable pricing, calibration, and diagnostic modules  

\- `notebooks/`: research workflow and result analysis  

\- `figures/`: generated plots and surfaces  



This separation mirrors professional quantitative research and development practices.



---



\## 10. Key Takeaways



\- Volatility surface modeling requires balancing fit quality, stability, and arbitrage considerations  

\- Surface-consistent SVI provides a robust framework for equity index options  

\- SABR remains valuable for local smile intuition but must be used with caution at the surface level  



---

