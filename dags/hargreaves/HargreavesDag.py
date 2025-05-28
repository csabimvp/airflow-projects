import os
import pathlib
import sys
from dataclasses import dataclass

import requests

# from ...lib.Processors import DataProcessor, ItemProcessor

lib = os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), "lib")
sys.path.append(lib)
from Processors import DataProcessor, ItemProcessor, LogItem


@dataclass
class LogData(DataProcessor):
    dag_logs: list


# Dataclass to store HL Fund Item data.
@dataclass
class HLFundItem(ItemProcessor):
    sedol: str
    aims: str
    annual_charge: float
    annual_saving: float
    bid_price: float
    citicode: str
    closed_fund: int
    company_id: int
    company_name: str
    cost_segment: int
    full_description: str
    fund_name: str
    fund_size: float
    historic_yield: float
    holding_fee: float
    icvc: int
    initial_charge: float
    initial_commission: float
    initial_saving: float
    is_oeic: int
    isaable: int
    kiid: int
    launch_currency: str
    launchdate: str  # 2008-03-28 00:00:00
    lsmininv: float
    lump_sum_min_inv: float
    net_annual_charge: float
    num_holdings: float
    offer_price: float
    other_expenses: float
    payment_frequency: str
    payment_type: str
    percent_change: float
    perf0t12m: float
    perf120m: float
    perf12m: float
    perf12t24m: float
    perf24t36m: float
    perf36m: float
    perf36t48m: float
    perf3m: float
    perf48t60m: float
    perf60m: float
    perf6m: float
    reg_saver: int
    reg_saver_min_inv: float
    sector_id: int
    sector_name: str
    sicav: int
    sippable: int
    total_expenses: float
    tracker: int
    unit_type: str
    update_time: str  # 2024-11-12 06:01:50
    updated: str  # 2024-11-12
    valuation_frequency: str
    fund_yield: float
    Wealth150: int


# Dataclass to store Master Data.
@dataclass
class HLMasterData(DataProcessor):
    master_data: list


# Fetching data from the HL API.
def FetchHargreavesData(page_size):
    log_item = LogItem(
        project_name="hargreaves", task_name=FetchHargreavesData.__name__
    )
    hl = list()
    start = 0
    keep_going = True
    while keep_going:
        url = f"https://www.hl.co.uk/ajax/funds/fund-search/search?investment=&companyid=&sectorid=&wealth=&unitTypePref=&tracker=&payment_frequency=&payment_type=&yield=&standard_ocf=&perf12m=&perf36m=&perf60m=&fund_size=&num_holdings=&start={start}&rpp={page_size}&lo=0&sort=fd.full_description&sort_dir=asc&"
        r = requests.get(url=url)

        if r.status_code == 200:
            res = r.json()
            result = res["Results"]

            # Cleaning up the data
            for item in result:
                item["aims"] = item["aims"].strip().replace("'", "").replace('""', "")
                launchdate = item["launchdate"].split(" ")[0]
                update_time = item["update_time"].split(" ")[0]
                updated = item["updated"]

                # Dictionary for numbers may be an empty string in the response data.
                numbers = {
                    "bid_price": 0,
                    "offer_price": 0,
                    "perf0t12m": 0,
                    "perf120m": 0,
                    "perf12m": 0,
                    "perf12t24m": 0,
                    "perf24t36m": 0,
                    "perf36m": 0,
                    "perf36t48m": 0,
                    "perf3m": 0,
                    "perf48t60m": 0,
                    "perf60m": 0,
                    "perf6m": 0,
                }

                for key in numbers.keys():
                    try:
                        numbers[key] = float(item[key])
                    except ValueError as e:
                        pass

                try:
                    fund_item = HLFundItem(
                        sedol=item["sedol"],
                        aims=item["aims"],
                        annual_charge=float(item["annual_charge"]),
                        annual_saving=float(item["annual_saving"]),
                        bid_price=float(numbers["bid_price"]),
                        citicode=item["citicode"],
                        closed_fund=int(item["closed_fund"]),
                        company_id=int(item["company_id"]),
                        company_name=item["company_name"],
                        cost_segment=int(item["cost_segment"]),
                        full_description=item["full_description"],
                        fund_name=item["fund_name"],
                        fund_size=float(item["fund_size"]),
                        historic_yield=float(item["historic_yield"]),
                        holding_fee=float(item["holding_fee"]),
                        icvc=int(item["icvc"]),
                        initial_charge=float(item["initial_charge"]),
                        initial_commission=float(item["initial_commission"]),
                        initial_saving=float(item["initial_saving"]),
                        is_oeic=int(item["is_oeic"]),
                        isaable=int(item["isaable"]),
                        kiid=int(item["kiid"]),
                        launch_currency=item["launch_currency"],
                        launchdate=launchdate,
                        lsmininv=float(item["lsmininv"]),
                        lump_sum_min_inv=float(item["lump_sum_min_inv"]),
                        net_annual_charge=float(item["net_annual_charge"]),
                        num_holdings=float(item["num_holdings"]),
                        offer_price=float(numbers["offer_price"]),
                        other_expenses=float(item["other_expenses"]),
                        payment_frequency=item["payment_frequency"],
                        payment_type=item["payment_type"],
                        percent_change=float(item["percent_change"]),
                        perf0t12m=float(numbers["perf0t12m"]),
                        perf120m=float(numbers["perf120m"]),
                        perf12m=float(numbers["perf12m"]),
                        perf12t24m=float(numbers["perf12t24m"]),
                        perf24t36m=float(numbers["perf24t36m"]),
                        perf36m=float(numbers["perf36m"]),
                        perf36t48m=float(numbers["perf36t48m"]),
                        perf3m=float(numbers["perf3m"]),
                        perf48t60m=float(numbers["perf48t60m"]),
                        perf60m=float(numbers["perf60m"]),
                        perf6m=float(numbers["perf6m"]),
                        reg_saver=int(item["reg_saver"]),
                        reg_saver_min_inv=float(item["reg_saver_min_inv"]),
                        sector_id=int(item["sector_id"]),
                        sector_name=item["sector_name"],
                        sicav=int(item["sicav"]),
                        sippable=int(item["sippable"]),
                        total_expenses=float(item["total_expenses"]),
                        tracker=int(item["tracker"]),
                        unit_type=item["unit_type"],
                        update_time=update_time,
                        updated=updated,
                        valuation_frequency=item["valuation_frequency"],
                        fund_yield=float(item["yield"]),
                        Wealth150=int(item["Wealth150"]),
                    )
                except ValueError as e:
                    log_item.log_actions(
                        data_items=len(hl), description=e, status_code=r.status_code
                    )
                except KeyError as e:
                    log_item.log_actions(
                        data_items=len(hl), description=e, status_code=r.status_code
                    )

                hl.append(fund_item)
        else:
            log_item.log_actions(
                data_items=len(hl), description=r.reason, status_code=r.status_code
            )

        start += page_size
        print(f"Number of Hargreaves Lansdown Funds downloaded: {len(hl)}")
        if len(result) < page_size:
            keep_going = False

    log_item.log_actions(
        data_items=len(hl), description=r.reason, status_code=r.status_code
    )
    return hl, log_item


def main():
    # Admin
    dir_path = pathlib.Path(__file__).parent.resolve()
    csv_folder_path = os.path.join(dir_path, "data")
    sql_folder_path = os.path.join(dir_path, "sql")

    # Main Function
    page_size = 40
    master_data, log_item = FetchHargreavesData(page_size=page_size)
    hlData = HLMasterData(master_data=master_data)
    hlData.save_data_to_csv(csv_folder_path=csv_folder_path)
    hlData.save_data_to_sql(schema="hl", sql_folder_path=sql_folder_path)

    # Log process
    L = LogData(dag_logs=[log_item])
    L.save_data_to_sql(schema="log", sql_folder_path=sql_folder_path)


if __name__ == "__main__":
    main()
