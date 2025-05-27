-- sudo su postgres
-- psql
CREATE DATABASE hargreaves_lansdown OWNER csabimvp;

-- \q
-- psql -U csabimvp -d hargreaves_lansdown
CREATE SCHEMA hl AUTHORIZATION csabimvp;

CREATE TABLE
    IF NOT EXISTS hl.master_data (
        sedol varchar PRIMARY KEY,
        aims varchar,
        annual_charge float,
        annual_saving float,
        bid_price float,
        citicode varchar,
        closed_fund int,
        company_id int,
        company_name varchar,
        cost_segment int,
        full_description varchar,
        fund_name varchar,
        fund_size float,
        historic_yield float,
        holding_fee float,
        icvc int,
        initial_charge float,
        initial_commission float,
        initial_saving float,
        is_oeic int,
        isaable int,
        kiid int,
        launch_currency varchar,
        launchdate varchar,
        lsmininv float,
        lump_sum_min_inv float,
        net_annual_charge float,
        num_holdings float,
        offer_price float,
        other_expenses float,
        payment_frequency varchar,
        payment_type varchar,
        percent_change float,
        perf0t12m float,
        perf120m float,
        perf12m float,
        perf12t24m float,
        perf24t36m float,
        perf36m float,
        perf36t48m float,
        perf3m float,
        perf48t60m float,
        perf60m float,
        perf6m float,
        reg_saver int,
        reg_saver_min_inv float,
        sector_id int,
        sector_name varchar,
        sicav int,
        sippable int,
        total_expenses float,
        tracker int,
        unit_type varchar,
        update_time varchar,
        updated varchar,
        valuation_frequency varchar,
        fund_yield float,
        Wealth150 int
    );

-- \q
-- exit