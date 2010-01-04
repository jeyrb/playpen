//
//  Place.m
//  iphone1
//
//  Created by Jeffrey Burrows on 26/12/2009.
//  Copyright 2009 JPMorgan. All rights reserved.
//

#import "Place.h"


@implementation Place

@synthesize name;
@synthesize type;
@synthesize food;
@synthesize description;
@synthesize address;
@synthesize area;
@synthesize town;
@synthesize phone;
@synthesize email;
@synthesize website;
@synthesize image;
@synthesize status;
@synthesize location;
@synthesize postcode;
@synthesize theListReview;
@synthesize theHeraldReview;
@synthesize otherReviews;
- (id) initWithName: (NSString *) newName type: (NSString *) newType food: (NSString *) newFood {
	self = [super init];
	self.name = newName;
	self.type = newType;
	self.food = newFood;
	NSLog(@"Create a new place of name %@, type %@ and food %@",self.name,self.type,self.food);
	return self;
}
@end
