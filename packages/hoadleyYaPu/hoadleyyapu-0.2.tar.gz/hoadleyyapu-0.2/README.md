# **Calculation Of Option Greeks and Implied Volatility in Python**

The aim of this package is to calculate Option Greeks and Implied Volatility for European options. The function takes input in a similar form to the popular Hoadley add-in used in Excel.

## **Functions:**
```blackScholes(calculation_type, Option_type, K, S, T, sigma, r = 0)```: Calculates option price, delta, gamma, vega, theta, or rho.
```implied_volatility(Option_type, K, S, T, Option_price, r = 0, tol = 0.0001, max_iterations = 100)```: Estimates implied volatility using Newton-Ralphson method.

## **Calculations**: 
1.  Performs price, delta, gamma, vega, theta, and rho calculations for both call and put options.
2.  Implied Volatility: Estimates implied volatility using numerical methods.
Input Validation: Includes checks for invalid inputs (e.g., NaN values, zero strike price).
Error Handling: Handles potential errors (e.g., incorrect option type, wrong Datatype entry when number is expected, etc.).

## **Input Parameters**:
```calculation_type```: Specifies the type of calculation to perform (price, delta, gamma, vega, theta, rho).<br>
&nbsp;&nbsp;&nbsp;i. Use 'p' for price.<br>
&nbsp;&nbsp;&nbsp;ii. Use 'd' for delta.<br>
&nbsp;&nbsp;&nbsp;iii. Use 'g' for gamma.<br>
&nbsp;&nbsp;&nbsp;iv. Use 'v' for vega.<br>
&nbsp;&nbsp;&nbsp;v. Use 't' for theta.<br>
&nbsp;&nbsp;&nbsp;vi. Use 'r' for rho.<br>
```Option_type```: Specifies the option type (call or put).<br>
```K```: Strike price.<br>
```S```: Underlying asset price.<br>
```T```: Time to expiration (in Days).<br>
```sigma```: Volatility.<br>
```r```: Risk-free interest rate.<br>
```Option_price```: Market price of the option (used for implied volatility calculation).<br>
```tol```: Tolerance level for implied volatility calculation.<br>
```max_iterations```: Maximum number of iterations for implied volatility calculation.<br>

## Example Usage

Here is an example of how to use the `blackScholes` and `implied_volatility` functions:

```python
from hoadleyYaPu import hoadleyYaPu

# Calculate call and put prices using the Black-Scholes model
callprice = hoadleyYaPu.blackScholes("p", "c", 100, 100, 15, 0.1855, 0)
putprice = hoadleyYaPu.blackScholes("p", "p", 1350, 1400, 15, 0.25, 0)

# Calculate the Greeks for a call option using the Black-Scholes model
callDelta = hoadleyYaPu.blackScholes("d", "c", 1350, 1400, 15, 0.25, 0)
callgamma = hoadleyYaPu.blackScholes("g", "c", 1350, 1400, 15, 0.25, 0)
callvega = hoadleyYaPu.blackScholes("v", "c", 1350, 1400, 15, 0.25, 0)
calltheta = hoadleyYaPu.blackScholes("t", "c", 1350, 1400, 15, 0.25, 0)
callrho = hoadleyYaPu.blackScholes("r", "c", 1350, 1400, 15, 0.25, 0)

# Calculate implied volatility for call and put options
callIV = hoadleyYaPu.implied_volatility("c", 42200, 41653.55, 1, 14.05, 0)
putIV = hoadleyYaPu.implied_volatility("p", 42200, 41653.55, 15, 550, 0)

