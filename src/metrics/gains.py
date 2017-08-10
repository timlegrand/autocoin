# coding: utf-8
from connectors import request
from metrics import capitalization as cap
from data import ledgers
from data import ticker


def compute_gains():
    # Get what we could expect from current account balances
    cap_table, cap_headers, total_cap_table = cap.get_balance_capitalization()
    # Get history of all deposits
    ledger, ledger_headers = ledgers.get_private_ledger(['deposit'])

    eur_earned = total_cap_table[0][3]
    eur_spent = sum([float(x[4]) for x in ledger])

    return eur_earned, eur_spent


if __name__ == '__main__':
    eur_earned, eur_spent = compute_gains()
    benefit = eur_earned - eur_spent
    print("Spent: {:.2f} €, earned: {:.2f} €, balance: {:.2f} €".format(eur_spent, eur_earned, benefit))
