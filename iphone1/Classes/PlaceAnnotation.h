//
//  PlaceAnnotation.h
//  iphone1
//
//  Created by Jeffrey Burrows on 26/12/2009.
//  Copyright 2009 JPMorgan. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <MapKit/MapKit.h>
#import <CoreLocation/CoreLocation.h>

@class Place;


@interface PlaceAnnotation : NSObject <MKAnnotation>	{
	Place *place;
}

@property (nonatomic,readonly) Place *place;

- (CLLocationCoordinate2D) coordinate;
- (id) initWithPlace:(Place *) newPlace;

@end
