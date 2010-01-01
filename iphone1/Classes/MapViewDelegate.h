//
//  MapViewController.h
//  iphone1
//
//  Created by Jeffrey Burrows on 25/12/2009.
//  Copyright 2009 JPMorgan. All rights reserved.
//

#import <MapKit/MKMapView.h>
#import <CoreLocation/CoreLocation.h>


@interface MapViewDelegate : NSObject <MKMapViewDelegate> {
	
}

- (void)mapViewDidFailLoadingMap:(MKMapView *)mapView withError:(NSError *)error;	



@end
