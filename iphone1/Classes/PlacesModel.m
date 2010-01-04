//
//  PlacesModel.m
//  iphone1
//
//  Created by Jeffrey Burrows on 04/01/2010.
//  Copyright 2010 Rhizomatics. All rights reserved.
//

#import "PlacesModel.h"


@implementation PlacesModel

@synthesize places;

static PlacesModel *sharedPlacesModel = nil;

+ (PlacesModel *) sharedPlacesModel {
	@synchronized(self) {
		if ( sharedPlacesModel == nil) {
			sharedPlacesModel = [[PlacesModel alloc] init];
		}
	}
	return sharedPlacesModel;
}

- (PlacesModel *) init {
	self = [super init];
	NSMutableArray *newPlaces = [[[PlaceDataParser alloc] init] loadPlacesFromFileSystem];
	self.places = newPlaces;
	NSLog(@"Loaded %i places",[newPlaces count]);
	return self;
}

@end
