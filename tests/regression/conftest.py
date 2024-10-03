import pytest
import os

from utils.config import contracts
from utils.import_current_votes import is_there_any_vote_scripts, is_there_any_upgrade_scripts, start_and_execute_votes
from utils.test.extra_data import ExtraDataService

from utils.test.helpers import ETH
from utils.test.oracle_report_helpers import oracle_report
from utils.test.simple_dvt_helpers import fill_simple_dvt_ops_vetted_keys

ENV_REPORT_AFTER_VOTE = "REPORT_AFTER_VOTE"
ENV_FILL_SIMPLE_DVT = "FILL_SIMPLE_DVT"


@pytest.fixture(scope="function", autouse=is_there_any_vote_scripts() or is_there_any_upgrade_scripts())
def autoexecute_vote(request, helpers, vote_ids_from_env, accounts, stranger):
    if "autoexecute_vote_ms" in request.node.fixturenames:
        return
    autoexecute_vote_impl(helpers, vote_ids_from_env, accounts, stranger)

@pytest.fixture(scope="module")
def autoexecute_vote_ms(helpers, vote_ids_from_env, accounts, stranger):
    autoexecute_vote_impl(helpers, vote_ids_from_env, accounts, stranger)

def autoexecute_vote_impl(helpers, vote_ids_from_env, accounts, stranger):
    if vote_ids_from_env:
        helpers.execute_votes(accounts, vote_ids_from_env, contracts.voting, topup="0.5 ether")
    else:
        start_and_execute_votes(contracts.voting, helpers)

    if os.getenv(ENV_FILL_SIMPLE_DVT):
        print(f"Prefilling SimpleDVT...")
        fill_simple_dvt_ops_vetted_keys(stranger)

    if os.getenv(ENV_REPORT_AFTER_VOTE):
        oracle_report(cl_diff=ETH(523), exclude_vaults_balances=False)

@pytest.fixture()
def extra_data_service() -> ExtraDataService:
    return ExtraDataService()
