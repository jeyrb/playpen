

#import <Foundation/Foundation.h>
#import "Place.h"


@interface PlaceDataParser : NSObject {
}

- (NSMutableArray *) loadPlacesFromFileSystem;
- (NSString *) getTrimmedColumn: (NSArray *) sheet column: (int) i;

@end

