

#import "PlaceDataParser.h"


@implementation PlaceDataParser

NSCharacterSet *quotes;

- (PlaceDataParser *) init {
	self = [super init];
	quotes = [NSCharacterSet characterSetWithCharactersInString:@"\""];
	return self;
}

	- (NSMutableArray *) loadPlacesFromFileSystem {
	//NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];

	NSMutableArray *places;
	int nodes = 0;
	//int COLUMNS = 22;

	//NSString *csvFile = @"Resources/glasgow-veggie.csv";
	NSString *csvFile = [[NSBundle mainBundle]
							pathForResource:@"glasgow-veggie"
							ofType:@"csv"];



	NSString *fileContent = [NSString stringWithContentsOfFile:csvFile encoding:NSUTF8StringEncoding error:NULL];
	NSArray *lines = [fileContent componentsSeparatedByCharactersInSet:[NSCharacterSet newlineCharacterSet]];
	NSLog(@"Read %i lines from %@",[lines count],csvFile);
	places = [NSMutableArray arrayWithCapacity: [lines count] - 1];
	for (int i = 1; i < [lines count]; i++) {
		// TODO: doesn't handle empty cells - thinks multiple commas are a single delimiter
		NSArray *cells = [[lines objectAtIndex:i] componentsSeparatedByString:@","];
		// In case you have quotes on the outside, do
		NSString *name = [[cells objectAtIndex:0] stringByTrimmingCharactersInSet:quotes];
		NSString *food = [[cells objectAtIndex:1] stringByTrimmingCharactersInSet:quotes];
		NSString *type = [[cells objectAtIndex:2] stringByTrimmingCharactersInSet:quotes];
		Place *place = [[Place alloc] initWithName: name type: type food: food];
		place.description = [self getTrimmedColumn: cells column: 3];
		place.address = [self getTrimmedColumn: cells column: 4];
		place.area = [self getTrimmedColumn: cells column: 5];
		place.town = [self getTrimmedColumn: cells column: 6];
		place.phone = [self getTrimmedColumn: cells column: 7];
		place.email = [self getTrimmedColumn: cells column: 8];
		place.website = [NSURL URLWithString: [self getTrimmedColumn: cells column: 9] ];
		place.image = [NSURL URLWithString: [self getTrimmedColumn: cells column: 10]];
		NSString *placeStatus = [self getTrimmedColumn: cells column: 11];
		if ( placeStatus == nil || [placeStatus length] == 0) {
			place.status = unknown;
		}
		else {
			placeStatus = [placeStatus uppercaseString];
			if ( [placeStatus isEqualToString: @"OPEN"] ) {
				place.status = open;
			}
			else {
				if ( [placeStatus isEqualToString: @"CLOSED"] ) {
					place.status = closed;
				}
				else {
					if ( [placeStatus isEqualToString: @"NO LONGER RECOMMENDED"] ) {
						place.status = unrecommended;
					}
					else {
						place.status = unknown;
						NSLog(@"Unknown status %@ for %@",placeStatus,place.name);
					}
				}
			}
		}
		NSString *latitude = [self getTrimmedColumn: cells column: 12];
		NSString *longtitude = [self getTrimmedColumn: cells column: 13];
		place.postcode = [self getTrimmedColumn: cells column: 14];
		place.theListReview = [NSURL URLWithString: [self getTrimmedColumn: cells column: 15]];
		place.theHeraldReview = [NSURL URLWithString: [self getTrimmedColumn: cells column: 16]];
		place.otherReviews = [NSURL URLWithString: [self getTrimmedColumn: cells column: 17]];

		[places addObject: place];
		nodes++;
	}


	//[pool drain];
	return places;
}

- (NSString *) getTrimmedColumn: (NSArray *) sheet column: (int) i {
	return [[sheet objectAtIndex:i] stringByTrimmingCharactersInSet:quotes];
}


@end
