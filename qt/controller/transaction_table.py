# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-10-31
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QPixmap

from moneyguru.gui.transaction_table import TransactionTable as TransactionTableModel
from .column import Column, DATE_EDIT, DESCRIPTION_EDIT, PAYEE_EDIT, ACCOUNT_EDIT
from .table_with_transactions import TableWithTransactions

class TransactionTable(TableWithTransactions):
    COLUMNS = [
        Column('status', '', 28),
        Column('date', 'Date', 120, editor=DATE_EDIT),
        Column('description', 'Description', 150, editor=DESCRIPTION_EDIT),
        Column('payee', 'Payee', 150, editor=PAYEE_EDIT),
        Column('checkno', 'Check #', 100),
        Column('from_', 'From', 120, editor=ACCOUNT_EDIT),
        Column('to', 'To', 120, editor=ACCOUNT_EDIT),
        Column('amount', 'Amount', 120),
    ]
    
    def __init__(self, doc, view):
        model = TransactionTableModel(view=self, document=doc.model)
        TableWithTransactions.__init__(self, model, view)
    
    #--- Data methods override
    def _getData(self, row, rowattr, role):
        if rowattr == 'status':
            if role == Qt.DecorationRole:
                if row.reconciled:
                    return QPixmap(':/check_16')
                elif row.is_budget:
                    return QPixmap(':/budget_16')
                elif row.recurrent:
                    return QPixmap(':/recurrent_16')
                else:
                    return None
            else:
                return None
        else:
            return TableWithTransactions._getData(self, row, rowattr, role)
    
