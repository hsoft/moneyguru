/* 
Copyright 2010 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "HS" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/hs_license
*/

#import "NSCellAdditions.h"

@implementation NSCell(NSCellAdditions)
- (void)drawTransparentBezelWithFrame:(NSRect)frame inView:(NSView *)controlView withLeftSide:(BOOL)withLeftSide {
    // Figure out the geometry. Note: NSButton uses flipped coordinates
    NSRect leftSide = NSMakeRect(NSMinX(frame), NSMinY(frame), 1, NSHeight(frame));
    NSRect rightSide = NSMakeRect(NSMaxX(frame) - 1, NSMinY(frame), 1, NSHeight(frame));
    
    // Define colors
    NSColor *borderColor = [NSColor colorWithDeviceWhite:0.62 alpha:1.0];
    NSColor *highlightColor = [NSColor colorWithDeviceWhite:0.0 alpha:0.35];
    
    // Draw the sides of the button
    [borderColor setFill];
    if (withLeftSide)
        [NSBezierPath fillRect:leftSide];
    [NSBezierPath fillRect:rightSide];
    
    // Draw the highlight
    if ([self isHighlighted])
    {
        [highlightColor setFill];
        [NSBezierPath fillRect:frame];
    }
}
@end