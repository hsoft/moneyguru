# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-11-27
# $Id$
# Copyright 2010 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

from core.document import (FILTER_UNASSIGNED, FILTER_INCOME, FILTER_EXPENSE, FILTER_TRANSFER,
    FILTER_RECONCILED, FILTER_NOTRECONCILED)
from core.gui.filter_bar import EntryFilterBar as EntryFilterBarModel

from ..filter_bar import FilterBar

class EntryFilterBar(FilterBar):
    BUTTONS = [
        ("All", None),
        ("Increase", FILTER_INCOME),
        ("Decrease", FILTER_EXPENSE),
        ("Transfers", FILTER_TRANSFER),
        ("Unassigned", FILTER_UNASSIGNED),
        ("Reconciled", FILTER_RECONCILED),
        ("Not Reconciled", FILTER_NOTRECONCILED),
    ]
    
    def __init__(self, doc, view):
        model = EntryFilterBarModel(document=doc.model, view=self)
        FilterBar.__init__(self, model, view)
    
    #--- model --> view
    def disable_transfers(self):
        self.view.setTabEnabled(3, False)
    
    def enable_transfers(self):
        self.view.setTabEnabled(3, True)
    
