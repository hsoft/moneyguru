# Copyright 2019 Virgil Dupras
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

from ..testutil import eq_

from ...const import AccountType
from ..base import TestApp

# ---
def app_two_txns():
    app = TestApp()
    app.add_account('one')
    app.add_account('two', account_type=AccountType.Liability)
    app.add_txn(description='first', from_='one', to='two', amount='42')
    app.add_txn(description='second', from_='two', to='one', amount='12')
    app.show_glview()
    return app

def test_totals_one_selected():
    # the totals line shows totals for selected entries
    app = app_two_txns()
    app.gltable.select([1])
    expected = "1 out of 4 selected. Debit: 0.00 Credit: 42.00"
    eq_(app.mw.status_line, expected)

def test_totals_four_selected():
    # the totals line shows totals for selected entries
    app = app_two_txns()
    app.gltable.select([1, 2, 5, 6])
    expected = "4 out of 4 selected. Debit: 54.00 Credit: 54.00"
    eq_(app.mw.status_line, expected)
