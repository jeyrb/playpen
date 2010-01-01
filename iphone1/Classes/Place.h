//
//  Place.h
//  iphone1
//
//  Created by Jeffrey Burrows on 26/12/2009.
//

#import <Foundation/Foundation.h>
#import <CoreLocation/CoreLocation.h>

@interface Place : NSObject {
	NSString *name;
	NSString *type;
	NSString *food;
	NSString *description;
	NSString *address;
	NSString *area;
	NSString *town;
	NSString *phone;
	NSString *email;
	NSURL *website;
	NSURL *image;
	NSString *status;
	CLLocation *location;
	NSString *postcode;
	NSURL *theListReview;
	NSURL *theHeraldReview;
	NSMutableArray *otherReviews;		
}

@property (nonatomic, copy) NSString *name;
@property (nonatomic, copy) NSString *type;
@property (nonatomic, copy) NSString *food;
@property (nonatomic, copy) NSString *description;
@property (nonatomic, copy) NSString *address;
@property (nonatomic, copy) NSString *area;
@property (nonatomic, copy) NSString *town;
@property (nonatomic, copy) NSString *phone;
@property (nonatomic, copy) NSString *email;
@property (nonatomic, copy) NSURL *website;
@property (nonatomic, copy) NSURL *image;
@property (nonatomic, copy) NSString *status;
@property (nonatomic, copy) CLLocation *location;
@property (nonatomic, copy) NSString *postcode;
@property (nonatomic, copy) NSURL *theListReview;
@property (nonatomic, copy) NSURL *theHeraldReview;
@property (nonatomic, copy) NSMutableArray *otherReviews;	

- (id) initWithName: (NSString *) name type: (NSString *) type food: (NSString *) food;

@end
