//
//  PlacesModel.h
//  iphone1
//
//  Created by Jeffrey Burrows on 04/01/2010.
//  Copyright 2010 Rhizomatics. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "PlaceDataParser.h"
#import "Place.h";

@interface PlacesModel : NSObject {
	NSMutableArray *places;
}

@property (nonatomic, retain) NSMutableArray *places;

+ (PlacesModel *) sharedPlacesModel;


@end
