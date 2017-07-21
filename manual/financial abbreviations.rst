Root 
====

Available python modules to program financial modelling 
-------------------------------------------------------
- https://github.com/wilsonfreitas/awesome-quant


Libs
----
- http://www.statsmodels.org/stable/index.html
- https://github.com/bashtage/arch
- https://github.com/quantopian/pyfolio


Documents
---------
- http://uhs.es/Financial%20Modelling%20in%20Python.pdf
- http://www.oracle.com/us/industries/financial-services/multi-state-markov-model-wp-3432818.pdf
- https://lectures.quantecon.org/py/index.html
- https://www.datacamp.com/community/tutorials/finance-python-trading


- https://github.com/pydata/pandas-datareader        												 \use pandas datareader to access world bank
	- https://lectures.quantecon.org/py/pandas.html  												 \pandas basics 
	- https://blog.plon.io/pandas/worldbank-gdp-analysis-using-pandas-and-seaborn-python-libraries/  \use case
	- https://apsportal.ibm.com/exchange/public/entry/view/47ed96c50374ccd15f93ef262c1af63b
	
Data sources
------------
- World Bank - http://data.worldbank.org/indicator/NY.GDP.MKTP.CD?locations=FI

(msm) multi-state Markov
------------------

The msm package for R (R Development Core Team 2010), available from http://CRAN.R-project.org/package=msm. msm can be used to a Markov model with any number of states and any pattern of transitions to panel data, and includes several extensions such as hidden Markov models and models whose transition intensities vary  with individual-specific or time-varying covariates. msm was motivated by studies of chronic diseases in medicine, and is frequently used in this area (Jackson et al. 2003; Sharples et al.

Basel2 (second Basel accord)
----------------------------

	Basel II is the second of the Basel Accords, (now extended and partially superseded[clarification needed] by Basel III), which are recommendations on banking laws and regulations issued by the Basel Committee on Banking Supervision.

	Basel II, initially published in June 2004, was intended to amend international standards that controlled how much capital banks need to hold to guard against the financial and operational risks banks face. These rules sought to ensure that the greater the risk to which a bank is exposed, the greater the amount of capital the bank needs to hold to safeguard its solvency and economic stability. Basel II attempted to accomplish this by establishing risk and capital management requirements to ensure that a bank has adequate capital for the risk the bank exposes itself to through its lending, investment and trading activities. One focus was to maintain sufficient consistency of regulations so to limit competitive inequality amongst internationally active banks.

	Basel II was implemented in the years prior to 2008, and was only to be implemented in early 2008 in most major economies;[1][2][3] that year's Financial crisis intervened before Basel II could become fully effective. As Basel III was negotiated, the crisis was top of mind and accordingly more stringent standards were contemplated and quickly adopted in some key countries including in Europe and the USA.

	
Relations 
---------
- http://www.oracle.com/us/industries/financial-services/multi-state-markov-model-wp-3432818.pdf

	In this section we briefly outline the main requirements for the estimation of default probabilities from the IFRS9 Standard point of view.

	* PD estimates should be unbiased ("best estimate PD"), i.e. PD (Probability of default) should accurately predict number of defaults and does not include optimism or conservatism. Where regulatory capital models are used as a starting point to calculate ECL, appropriate adjustments need to be made to remove inherent conservatism.
	* Estimated PDs should be point time, i.e., adjusted, where necessary, to reflect the effects of the current economic conditions.
	* The PD (Probability of default) estimates should be recalibrated on a regular basis, or monitoring should be provided to show why recalibration was not necessary. The (re)calibration sample should representative of the current population.
	* PD (Probability of default) should be calculated using sufficient sample size, i.e. estimates should be based on a sufficiently large sample size to allow for a meaningful quantification and validation of the loss characteristics. Historical loss data should cover at least one full credit cycle.
	* The PDs (Probability of default) should be calculated with appropriate segmentation the bank should consider risk drivers in respect of borrower risk, transaction risk and delinquency status in assigning exposures to PD model segments.
	* The data used for calibration should be consistent with the IFRS9 (Financial Instruments issued on 24 July 2014) default definition, i.e. all components of the PD calculation (including 12m PDs and default curves for extrapolation to lifetime) should use the same definition of default.
	* Lifetime PDs (Probability of default) should be calculated using appropriate extrapolation methodologies. Where extrapolation techniques are used to determine lifetime PD measures, these should not introduce bias into the calculation of ECL (Express Credit Line).
	* The  estimated  PDs (Probability of default) should  be  inclusive  of  forward  looking  information,  including  macroeconomic  factors in the computation of lifetime PD's, to ensure that loss recognition is not delayed. MULTI-STATE MARKOV MODELING OF IFRS9 DEFAULT PROBABILITY TERM STRUCTURE IN OFSAA
	* For instruments that have comparable credit risk, the risk of a default must be higher the longer the expected life of the instrument (this requires that cumulative life time PD (Probability of default) curves are monotonically increasing)
	* Internal data should be used in building the PD models, where possible, and data should be representative of the portfolio going forward.
	* Where external data or vendor models are used, the external calibration sample should be representative of the internal risk profile of the current population.	

Key metrics to compare
* GDP			
* Employment	
* Consumption	
* FTSE 100 | S&P500	(main regional index)

	
Branches
========
IRBA (Internal ratings-based approach)
--------------------------------------
	Under the Basel II guidelines, banks are allowed to use their own estimated risk parameters for the purpose of calculating regulatory capital. This is known as the internal ratings-based (IRB) approach to capital requirements for credit risk. Only banks meeting certain minimum conditions, disclosure requirements and approval from their national supervisor are allowed to use this approach in estimating capital for various exposures.[1][2]


IFRS9 
-----
	IFRS 9 Financial Instruments issued on 24 July 2014 is the IASB's replacement of IAS 39 Financial Instruments: Recognition and Measurement. The Standard includes requirements for recognition and measurement, impairment, derecognition and general hedge accounting. The IASB completed its project to replace IAS 39 in phases, adding to the standard as it completed each phase.

	The version of IFRS 9 issued in 2014 supersedes all previous versions and is mandatorily effective for periods beginning on or after 1 January 2018 with early adoption permitted (subject to local endorsement requirements). For a limited period, previous versions of IFRS 9 may be adopted early if not already done so provided the relevant date of initial application is before 1 February 2015.

	IFRS 9 does not replace the requirements for portfolio fair value hedge accounting for interest rate risk (often referred to as the ‘macro hedge accounting’ requirements) since this phase of the project was separated from the IFRS 9 project due to the longer term nature of the macro hedging project which is currently at the discussion paper phase of the due process. In April 2014, the IASB published a Discussion Paper Accounting for Dynamic Risk management: a Portfolio Revaluation Approach to Macro Hedging. Consequently, the exception in IAS 39 for a fair value hedge of an interest rate exposure of a portfolio of financial assets or financial liabilities continues to apply.

	- https://www.iasplus.com/en/standards/ifrs/ifrs9


	Matlab
	- https://se.mathworks.com/campaigns/products/ppc/google/financial-risk-improve-model-governance-white-paper.html?s_eid=psn_44440937449&q=ifrs%209

	
PD (Probability of default)
---------------------------
	Probability of default (PD) is a financial term describing the likelihood of a default over a particular time horizon. It provides an estimate of the likelihood that a borrower will be unable to meet its debt obligations.[1][2]

	PD is used in a variety of credit analyses and risk management frameworks. Under Basel II, it is a key parameter used in the calculation of economic capital or regulatory capital for a banking institution.

	PD is closely linked to the Expected Loss, which is defined as the product of the PD, the Loss Given Default (LGD) and the Exposure at Default (EAD).[3][4]

	- https://en.wikipedia.org/wiki/Probability_of_default

	
LGD (Loss given default)
------------------------
	Loss given default or LGD is the share of an asset that is lost if a borrower defaults.

	It is a common parameter in Risk Models and also a parameter used in the calculation of Economic Capital, Expected loss or Regulatory Capital under Basel II for a banking institution. This is an attribute of any exposure on bank's client. Exposure is the amount that one may lose in an investment.

	The LGD is closely linked to the Expected Loss, which is defined as the product of the LGD, the Probability of Default (PD) and the Exposure at Default (EAD).

	- https://en.wikipedia.org/wiki/Loss_given_default
		

EAD (Exposure at default)
-------------------------
	Exposure at default or (EAD) is a parameter used in the calculation of economic capital or regulatory capital under Basel II for a banking institution. It can be defined as the gross exposure under a facility upon default of an obligor.[1]

	Outside of Basel II, the concept is sometimes known as Credit Exposure (CE). It represents the immediate loss that the lender would suffer if the borrower (counterparty) fully defaults on his debt.

	The EAD is closely linked to the expected loss, which is defined as the product of the EAD, the probability of default (PD) and the loss given default (LGD).

	- https://www.eota.eu/en-GB/content/what-is-an-ead/30/

	
ECL (Express Credit Line)
-------------------------
	Loans Secured by Eligible Restricted & Control Stock

	Express Credit Line (ECL) Loans
	A flexible line of credit using eligible securities in your brokerage account as collateral. Offered by Morgan Stanley Smith Barney LLC.

	Margin Loans
	A traditional brokerage loan enabling the purchase of additional securities to diversify your investment portfolio — an effective strategy to potentially expedite ownership requirements. Offered by Morgan Stanley Smith Barney LLC.

	Portfolio Loan Account (PLA)
	A securities based loan offered by Morgan Stanley Bank, N.A. A PLA loan/line of credit may be a cost-effective financing alternative for qualified applicants.

	Tailored Lending
	Uses different assets and asset classes as collateral based on your unique needs. Offered by Morgan Stanley Private Bank, National Association.

	- https://www.morganstanley.com/spc/knowledge/managing-equity/executive-services/products-services-for-executives/liquidity-strategies.html

