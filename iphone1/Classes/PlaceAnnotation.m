//
//  PlaceAnnotation.m
//  iphone1
//
//  Created by Jeffrey Burrows on 26/12/2009.
//  Copyright 2009 JPMorgan. All rights reserved.
//

#import "PlaceAnnotation.h"
#import "Place.h"

@implementation PlaceAnnotation

@synthesize place;

- (CLLocationCoordinate2D) coordinate {
	return self.place.location.coordinate;
}

- (id) initWithPlace:(Place *) newPlace {
	self = [super init];
	place = newPlace;
	return self;
}

@end
