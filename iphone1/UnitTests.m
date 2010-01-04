//
//  UnitTests.m
//  iphone1
//
//  Created by Jeffrey Burrows on 04/01/2010.
//  Copyright 2010 Rhizomatics. All rights reserved.
//

#import "UnitTests.h"


@implementation UnitTests


- (void) testMath {

    STAssertTrue((1+1)==2, @"Compiler isn't feeling well today :-(" );
}
/*
- (void) testParseData {
	NSAutoreleasePool *pool = [[NSAutoreleasePool alloc] init];
	NSFileHandle *jsonFile;
	NSData *data;
	int nodes = 0;
	int COLUMNS = 22;

	jsonFile = [NSFileHandle fileHandleForReadingAtPath:@"glasgow-veggie.json"];
	STAssertNotNil(jsonFile,@"JSON source file not found");

	data = [jsonFile readDataToEndOfFile];
	[jsonFile closeFile];
	NSLog(@"Read JSON file");
	// Store incoming data into a string
	NSString *jsonString = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];

	// Create a dictionary from the JSON string
	NSDictionary *results = [jsonString JSONValue];

	// Build an array from the dictionary for easy access to each entry
	NSArray *places = [[results objectForKey:@"feed"] objectForKey:@"entry"];
	for (NSDictionary *place in places) {
		NSLog(@"Found a place %i",[place count]);
		NSDictionary *content = [place objectForKey:@"content"];
		for (NSString *leaf in content) {
			NSLog(@"Found a leaf: %@ %@",leaf,[content objectForKey:leaf]);
			nodes++;
		}
	}

	STAssertTrue(nodes>10000,@"No nodes found: %i",nodes);
	[jsonString release];
	[pool drain];
}*/

- (void) testParseCsvData {
	NSArray	*places = [PlaceDataParser loadPlacesFromFileSystem];

	STAssertTrue([places count]>100,@"No nodes found");
	[places autorelease];

}




@end
