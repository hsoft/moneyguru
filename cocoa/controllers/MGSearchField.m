/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "MGSearchField.h"
#import "Utils.h"
#import "ObjP.h"

@implementation MGSearchField
- (id)initWithPy:(id)aPy
{
    PyObject *pRef = getHackedPyRef(aPy);
    PySearchField *m = [[PySearchField alloc] initWithModel:pRef];
    OBJP_LOCKGIL;
    Py_DECREF(pRef);
    OBJP_UNLOCKGIL;
    self = [super initWithModel:m];
    [m bindCallback:createCallback(@"GUIObjectView", self)];
    [NSBundle loadNibNamed:@"SearchField" owner:self];
    [self setView:linkedView];
    return self;
}

- (PySearchField *)model
{
    return (PySearchField *)model;
}

/* Action */

- (IBAction)changeQuery:(id)sender
{
    NSString *query = [linkedView stringValue];
    [[self model] setQuery:query];
}

/* Python callbacks */

- (void)refresh
{
    [linkedView setStringValue:[[self model] query]];
}

@end