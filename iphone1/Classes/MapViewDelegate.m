//
//  MapViewController.m
//  iphone1
//
//  Created by Jeffrey Burrows on 25/12/2009.
//  Copyright 2009 JPMorgan. All rights reserved.
//

#import "MapViewDelegate.h"

@implementation MapViewDelegate

- (void)mapViewDidFailLoadingMap:(MKMapView *)mapView withError:(NSError *)error {
		NSLog(@"Unable to load the map");
}





- (void)dealloc {
    [super dealloc];
}


@end
