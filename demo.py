import os

import dotenv
from algosdk.v2client.algod import AlgodClient
from algosdk.future import transaction
from algosdk import account
from algosdk.logic import teal_sign_from_program
from pyteal import compileTeal, Mode, Bytes
from account import Account

from contracts import escrow
from sandbox import get_genesis_accounts
from utils import fully_compile_contract, get_algod_client, wait_for_transaction


def get_escrow_program(client: AlgodClient, data: str):
    return fully_compile_contract(
        client,
        compileTeal(
            escrow(Bytes(data)),
            mode=Mode.Signature,
            assembleConstants=True,
            version=5
        )
    )


if __name__ == '__main__':
    dotenv.load_dotenv('.env')

    algod_url = os.environ.get('ALGOD_URL')
    algod_api_key = os.environ.get('ALGOD_API_KEY')
    client = get_algod_client(algod_url, algod_api_key)
    
    funder = get_genesis_accounts()[0]
    
    hp = Account.from_mnemonic("manage erode connect disagree scene auction close oil assume yard ride rapid brush assume gossip match find south deposit snake access endless stove absent ski")
    data = "test"
    program = get_escrow_program(client, data)
    signature = teal_sign_from_program(hp.get_private_key(), data.encode('utf-8'), program)
    lsig = transaction.LogicSigAccount(
        program,
        args=[signature]
    )
    
    txn0 = transaction.PaymentTxn(
        sender=funder.get_address(),
        sp=client.suggested_params(),
        receiver=lsig.address(),
        amt=10_000_000,
    )
    signed_txn0 = txn0.sign(funder.get_private_key())
    tx_id = client.send_transaction(signed_txn0)
    wait_for_transaction(client, tx_id)
    
    txn = transaction.PaymentTxn(
        sender=lsig.address(),
        sp=client.suggested_params(),
        receiver=hp.get_address(),
        amt=100_000
    )
    signed_txn = transaction.LogicSigTransaction(txn, lsig)
    tx_id = client.send_transaction(signed_txn)
    wait_for_transaction(client, tx_id)
