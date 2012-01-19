/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import <Cocoa/Cocoa.h>
#import "PyPanel.h"
#import "PySplitTable.h"
#import "PyCompletableEdit.h"

@interface PyPanelWithTransaction : PyPanel {}
- (PyCompletableEdit *)completableEdit;
- (PySplitTable *)splitTable;
- (NSString *)description;
- (void)setDescription:(NSString *)description;
- (NSString *)payee;
- (void)setPayee:(NSString *)payee;
- (NSString *)checkno;
- (void)setCheckno:(NSString *)checkno;
- (NSString *)notes;
- (void)setNotes:(NSString *)checkno;
- (BOOL)isMultiCurrency;
@end