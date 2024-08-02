# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["CompanyFundamentalsResponse", "Data", "DataDividend", "DataError"]


class DataDividend(BaseModel):
    annual_dividend_per_share: Optional[float] = FieldInfo(alias="annualDividendPerShare", default=None)
    """
    Dividend is the distribution of reward from a portion of company's earnings, and
    is paid to a class of its shareholders each year for every share they own.
    """

    distribution_frequency: Optional[str] = FieldInfo(alias="distributionFrequency", default=None)
    """
    Distribution frequency is how often a dividend is paid by an individual stock,
    distribution frequency can vary from monthly to annually.
    """

    dividend_per_share: Optional[float] = FieldInfo(alias="dividendPerShare", default=None)
    """
    Dividend is the distribution of reward from a portion of company's earnings, and
    is paid to a class of its shareholders for every share they own each time the
    company distributes dividends, which could be quarterly, semi-annually, or
    annually depending on the company's dividend policy.
    """

    ex_dividend_date: Optional[date] = FieldInfo(alias="exDividendDate", default=None)
    """
    The date on which the dividend eligibility expires is called the ex-dividend
    date
    """

    indicative_dividend_rate: Optional[str] = FieldInfo(alias="indicativeDividendRate", default=None)
    """
    Indicated dividend Rate projects the annual dividend return of a stock based on
    its most recent dividend, the number of dividends issued each year, and the
    current share price
    """

    payable_date: Optional[date] = FieldInfo(alias="payableDate", default=None)
    """
    The company issues the payment of the dividend on the payment date, which is
    when the money gets credited to investor's account
    """

    record_date: Optional[date] = FieldInfo(alias="recordDate", default=None)
    """
    The record date is the cut-off date in order to determine which shareholders are
    eligible to receive a dividend or distribution
    """

    yield_: Optional[float] = FieldInfo(alias="yield", default=None)
    """
    Dividend yield is the financial ratio that shows how much a company pays out in
    dividends each year relative to its stock price
    """


class DataError(BaseModel):
    code: Optional[str] = None
    """status"""

    detail: Optional[str] = None
    """Error details explanation"""

    title: Optional[str] = None
    """The plain text error message"""


class Data(BaseModel):
    as_of_date: Optional[date] = FieldInfo(alias="asOfDate", default=None)
    """
    Date on which the specified fundamentals data or information is accurate or
    relevant.
    """

    asset_turnover_ratio: Optional[float] = FieldInfo(alias="assetTurnoverRatio", default=None)
    """
    The asset turnover ratio measures the value of a company's sales or revenues
    relative to the value of its assets
    """

    book_value_per_share: Optional[float] = FieldInfo(alias="bookValuePerShare", default=None)
    """
    Book value per common share is a formula used to calculate the per share value
    of a company based on common shareholders' equity in the company
    """

    cash_flow_per_share: Optional[float] = FieldInfo(alias="cashFlowPerShare", default=None)
    """
    Cash flow per share is calculated as a ratio, indicating the amount of cash a
    business generates based on a company's net income with the costs of
    depreciation and amortization added back
    """

    cash_per_share: Optional[float] = FieldInfo(alias="cashPerShare", default=None)
    """Cash Per Share of Security"""

    currency: Optional[str] = None
    """Currency code for the data.

    For a list of currency ISO codes, visit
    [Online Assistant Page #1470](https://oa.apps.factset.com/pages/1470).
    """

    current_ratio: Optional[float] = FieldInfo(alias="currentRatio", default=None)
    """
    The current ratio is a liquidity ratio that measures a company's ability to pay
    short-term and long-term obligations. The ratio is calculated by comparing
    current assets to current liabilities
    """

    dividend: Optional[DataDividend] = None

    earnings_per_share: Optional[float] = FieldInfo(alias="earningsPerShare", default=None)
    """
    Earnings per share (EPS) is the portion of a company's profit allocated to each
    share of common stock
    """

    ebitda_margin: Optional[float] = FieldInfo(alias="ebitdaMargin", default=None)
    """
    EBITDA margin is an assessment of a firm's operating profitability as a
    percentage of its total revenue. It is equal to earnings before interest, tax,
    depreciation and amortization (EBITDA) divided by total revenue
    """

    ebit_margin: Optional[float] = FieldInfo(alias="ebitMargin", default=None)
    """
    EBIT margin is an assessment of a firm's operating profitability as a percentage
    of its total revenue. It is equal to earnings before interest and tax (EBIT)
    divided by total revenue
    """

    enterprise_value: Optional[float] = FieldInfo(alias="enterpriseValue", default=None)
    """
    Enterprise Value (EV) is the measure of a company's total value for the period
    and date(s) requested in local currency by default
    """

    error: Optional[DataError] = None

    five_year_average_yield: Optional[float] = FieldInfo(alias="fiveYearAverageYield", default=None)
    """
    Average of the dividend yield with yield calculated for each of the past five
    years
    """

    five_year_dividend_growth_rate: Optional[float] = FieldInfo(alias="fiveYearDividendGrowthRate", default=None)
    """
    The dividend growth rate is the annualized percentage rate of growth that a
    particular stock's dividend undergoes over five years of time
    """

    floating_shares_outstanding: Optional[float] = FieldInfo(alias="floatingSharesOutstanding", default=None)
    """
    Represents the number of shares outstanding less closely held shares for the
    period and date(s) requested
    """

    fsym_id: Optional[str] = FieldInfo(alias="fsymId", default=None)
    """FactSet Regional Security Identifier.

    Six alpha-numeric characters, excluding vowels, with an -R suffix (XXXXXX-R).
    Identifies the security's best regional security data series per currency. For
    equities, all primary listings per region and currency are allocated a
    regional-level permanent identifier. The regional-level permanent identifier
    will be available once a SEDOL representing the region/currency has been
    allocated and the identifiers are on FactSet.
    """

    gross_margin: Optional[float] = FieldInfo(alias="grossMargin", default=None)
    """
    Gross profit margin is the proportion of money left over from revenues after
    accounting for the cost of goods sold, calculated by dividing gross profit by
    revenues.
    """

    inventory_turnover: Optional[float] = FieldInfo(alias="inventoryTurnover", default=None)
    """
    Inventory turnover is a ratio showing how many times a company has sold and
    replaced inventory during a given period
    """

    long_term_debt_to_equity: Optional[float] = FieldInfo(alias="longTermDebtToEquity", default=None)
    """Long-term debt consists of loans and financial obligations lasting over one
    year.

    The Debt/Equity (D/E) Ratio is calculated by dividing a company's total
    liabilities lasting over one year by its shareholder equity
    """

    net_income: Optional[float] = FieldInfo(alias="netIncome", default=None)
    """
    This equals to net earnings (profit) calculated as sales less cost of goods
    sold, selling, general and administrative expenses, operating expenses,
    depreciation, interest, taxes and other expenses
    """

    number_of_employees: Optional[int] = FieldInfo(alias="numberOfEmployees", default=None)
    """
    Represents the number of employees under the company's payroll as reported by
    the management to the shareholders within 90 days of the fiscal year-end.
    """

    payout_ratio: Optional[float] = FieldInfo(alias="payoutRatio", default=None)
    """
    The dividend payout ratio is the ratio of the total amount of dividends paid out
    to shareholders relative to the net income of the company
    """

    pretax_margin: Optional[float] = FieldInfo(alias="pretaxMargin", default=None)
    """
    The pretax margin is the ratio of a company's pre-tax earnings to its total
    sales
    """

    price_to_book_ratio: Optional[float] = FieldInfo(alias="priceToBookRatio", default=None)
    """
    Companies use the price-to-book ratio to compare a firm's market to book value
    by dividing price per share by book value per share (BVPS) .
    """

    price_to_cash_flow_ratio: Optional[float] = FieldInfo(alias="priceToCashFlowRatio", default=None)
    """
    The price-to-cash flow ratio is a stock valuation indicator or multiple that
    measures the value of a stock's price relative to its operating cash flow per
    share.
    """

    price_to_earnings_ratio: Optional[float] = FieldInfo(alias="priceToEarningsRatio", default=None)
    """
    The price-to-earnings ratio (P/E ratio) is the ratio for valuing a company that
    measures its current share price relative to its per-share earnings
    """

    price_to_sales_ratio: Optional[float] = FieldInfo(alias="priceToSalesRatio", default=None)
    """
    The price-to-sales ratio (P/S ratio) is a valuation ratio that compares a
    company's stock price to its revenues
    """

    quick_ratio: Optional[float] = FieldInfo(alias="quickRatio", default=None)
    """
    The quick ratio measures the dollar amount of liquid assets available with the
    company against the dollar amount of its current liabilities
    """

    request_id: Optional[str] = FieldInfo(alias="requestId", default=None)
    """Identifier that was used for the request."""

    return_on_assets: Optional[float] = FieldInfo(alias="returnOnAssets", default=None)
    """
    Return on net assets (RONA) is a measure of financial performance calculated as
    net income divided by the sum of fixed assets and net working capital
    """

    return_on_equity: Optional[float] = FieldInfo(alias="returnOnEquity", default=None)
    """
    Return on equity (ROE) is a measure of financial performance calculated as net
    income divided by shareholders' equity
    """

    return_on_invested_capital: Optional[float] = FieldInfo(alias="returnOnInvestedCapital", default=None)
    """Return on Investment (ROI) measures how well an investment is performing"""

    revenue_per_share: Optional[float] = FieldInfo(alias="revenuePerShare", default=None)
    """
    The portion of a company's revenue that is allocated to each share of common
    stock.
    """

    sales_per_employee: Optional[float] = FieldInfo(alias="salesPerEmployee", default=None)
    """
    Revenue per employee is a ratio that is calculated as a company's total revenue
    divided by its current number of employees
    """

    sales_per_share: Optional[float] = FieldInfo(alias="salesPerShare", default=None)
    """
    Sales per share is a ratio that computes the total revenue earned per share over
    a designated period
    """

    share_holder_equity: Optional[float] = FieldInfo(alias="shareHolderEquity", default=None)
    """
    Shareholder equity represents the amount of financing the company experiences
    through common and preferred shares
    """

    three_year_average_yield: Optional[float] = FieldInfo(alias="threeYearAverageYield", default=None)
    """
    Average of the dividend yield with yield calculated for each of the past three
    years
    """

    three_year_dividend_growth_rate: Optional[float] = FieldInfo(alias="threeYearDividendGrowthRate", default=None)
    """
    The dividend growth rate is the annualized percentage rate of growth that a
    particular stock's dividend undergoes over three years of time
    """

    total_assets: Optional[float] = FieldInfo(alias="totalAssets", default=None)
    """Total amount of assets owned by entity."""

    total_debt_to_equity: Optional[float] = FieldInfo(alias="totalDebtToEquity", default=None)
    """
    The Debt/Equity (D/E) Ratio is calculated by dividing a company's total
    liabilities by its shareholder equity
    """

    total_revenue: Optional[float] = FieldInfo(alias="totalRevenue", default=None)
    """
    Revenue is the amount of money (in Million) that a company actually receives
    during a specific period, including discounts and deductions for returned
    merchandise.
    """

    trailing_twelve_month_earnings_per_share: Optional[float] = FieldInfo(
        alias="trailingTwelveMonthEarningsPerShare", default=None
    )
    """Earnings per share over the last 12 months."""


class CompanyFundamentalsResponse(BaseModel):
    data: Optional[List[Data]] = None
