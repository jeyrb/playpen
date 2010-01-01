//
//  CategoryViewController.h
//  iphone1
//
//  Created by Jeffrey Burrows on 26/12/2009.
//  Copyright 2009 JPMorgan. All rights reserved.
//


@interface CategoryViewController : UIViewController <UITableViewDelegate, UITableViewDataSource> {
	UITableView *categories;
	NSMutableArray *cells;
}

@property (nonatomic, retain) IBOutlet UITableView *categories;

- (void)loadView;

- (NSInteger)tableView:(UITableView *)table numberOfRowsInSection:(NSInteger)section;

// Row display. Implementers should *always* try to reuse cells by setting each cell's reuseIdentifier and querying for available reusable cells with dequeueReusableCellWithIdentifier:
// Cell gets various attributes set automatically based on table (separators) and data source (accessory views, editing controls)

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath;
- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath;

@end
