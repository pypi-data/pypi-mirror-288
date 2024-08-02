# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["MetricListParams"]


class MetricListParams(TypedDict, total=False):
    category: Literal[
        "INCOME_STATEMENT",
        "BALANCE_SHEET",
        "CASH_FLOW",
        "RATIOS",
        "FINANCIAL_SERVICES",
        "INDUSTRY_METRICS",
        "PENSION_AND_POSTRETIREMENT",
        "MARKET_DATA",
        "MISCELLANEOUS",
        "DATES",
    ]
    """Filters the list of FF\\__\\** metrics by major category -

    - **INCOME_STATEMENT** = Income Statement line items, such as Sales, Gross
      Profit, Net Income.
    - **BALANCE_SHEET** = Balance Sheet line items, such as Assets, Liabilities, and
      Shareholders Equity.
    - **CASH_FLOW** = Cash Flow Statement line items, such as Financing activities,
      Operation, and Per Share.
    - **RATIOS** = Pre-calculated Ratios, including Financial, Growth Rates,
      Profitability, Liquidity, Size, and Valuation.
    - **FINANCIAL_SERVICES** = Financial Statement Items modified for Financial
      Services companies.
    - **INDUSTRY_METRICS** = Industry Specific Line Items or Modifications. View
      subcategory for list of Industries.
    - **PENSION_AND_POSTRETIREMENT** = Accumulated Pension Benefit Obligations and
      related data.
    - **MARKET_DATA** = General Market Data, such as Shares Outstanding. _Note -
      /factset-prices/prices/ endpoints may be better suited for pricing-related
      market data._
    - **MISCELLANEOUS** = Corporation Data, Financial Records details, Indicators.
    - **DATES** = Relevant Dates
    """

    metric_data_type: Annotated[str, PropertyInfo(alias="metricDataType")]
    """
    Returns general data type of the metrics like integer, float or strings, when
    left blankmetrics with all data types would be returned
    """

    subcategory: Literal[
        "ASSETS",
        "BALANCE_SHEET",
        "HEALTHCARE",
        "LIABILITIES",
        "PER_SHARE",
        "SHAREHOLDERS_EQUITY",
        "SUPPLEMENTAL",
        "CASH_FLOW",
        "CHANGE_IN_CASH",
        "FINANCING",
        "INVESTING",
        "OPERATING",
        "DATES",
        "INCOME_STATEMENT",
        "NON-OPERATING",
        "RETAIL",
        "AIRLINES",
        "BANK",
        "BANKING",
        "HOTELS_AND_GAMING",
        "METALS_AND_MINING",
        "OIL_AND_GAS",
        "PHARMACEUTICAL",
        "REIT",
        "MARKET_DATA",
        "CLASSIFICATION",
        "CORPORATE_DATA",
        "FINANCIAL_RECORDS",
        "INDICATOR",
        "EMPLOYEES_AND_MANAGEMENT",
        "PENSION_AND_POSTRETIREMENT",
        "FINANCIAL",
        "GROWTH_RATE",
        "LIQUIDITY",
        "PROFITABILITY",
        "SIZE",
        "VALUATION",
        "OTHER",
        "HOMEBUILDING",
        "NET_INCOME",
        "TELECOM",
        "UTILITY",
        "INSURANCE",
    ]
    """Sub-Category Filter for the Primary Category Requested.

    Choose a related sub-category for the Category requested-

    - **INCOME_STATEMENT** - INCOME_STATEMENT, NON-OPERATING, PER_SHARE,
      SUPPLEMENTAL, OTHER
    - **BALANCE_SHEET** - ASSETS, BALANCE_SHEET, HEALTHCARE, LIABILITIES, PER_SHARE,
      SHAREHOLDERS_EQUITY, SUPPLEMENTAL
    - **CASH_FLOW** - CASH_FLOW, CHANGE_IN_CASH, FINANCING, INVESTING, OPERATING,
      PER_SHARE, SUPPLEMENTAL
    - **RATIOS** - FINANCIAL, GROWTH_RATE, LIQUIDITY, PROFITABILITY, SIZE, VALUATION
    - **FINANCIAL_SERVICES** - BALANCE_SHEET, INCOME_STATEMENT, SUPPLEMENTAL
    - **INDUSTRY_METRICS** - AIRLINES, BANKING, HOTELS_AND_GAMING,
      METALS_AND_MINING, OIL_AND_GAS, PHARMACEUTICAL, REIT, RETAIL, BANK, INSURANCE,
      UTILITY
    - **PENSION_AND_POSTRETIREMENT** - PENSION_AND_POSTRETIREMENT
    - **MARKET_DATA** - MARKET_DATA
    - **MISCELLANEOUS** - CLASSIFICATION, CORPORATE_DATA, FINANCIAL_RECORDS,
      INDICATOR, EMPLOYEES_AND_MANAGEMENT
    - **DATES** - DATES
    """
