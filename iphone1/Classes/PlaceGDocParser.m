//
//  PlaceXmlParserDelegate.m
//  iphone1
//
//  Created by Jeffrey Burrows on 27/12/2009.
//  Copyright 2009 JPMorgan. All rights reserved.
//

#import "PlaceGDocParser.h"


@implementation PlaceGDocParser


// get a spreadsheet service object with the current username/password
//
// A "service" object handles networking tasks.  Service objects
// contain user authentication information as well as networking
// state information (such as cookies and the "last modified" date for
// fetched data.)

- (GDataServiceGoogleSpreadsheet *)spreadsheetService {

	static GDataServiceGoogleSpreadsheet* service = nil;

	if (!service) {
		service = [[GDataServiceGoogleSpreadsheet alloc] init];

		[service setShouldCacheDatedData:YES];
		[service setServiceShouldFollowNextLinks:YES];

		// iPhone apps will typically disable caching dated data or will call
		// clearLastModifiedDates after done fetching to avoid wasting
		// memory.
	}
}

@end
