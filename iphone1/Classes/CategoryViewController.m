
#import "CategoryViewController.h"


@implementation CategoryViewController

@synthesize categories;


- (void)viewDidLoad {
		cells = [[NSMutableArray alloc]initWithCapacity: 12];
		for (int i=0; i< 12; i++) {
			UITableViewCell *cell = [[UITableViewCell alloc] init];
			cell.accessoryType = UITableViewCellAccessoryCheckmark;
			cell.textLabel.text = [[NSString alloc] initWithFormat: @"Category %u ",i+1];
			[cells insertObject: cell atIndex: i];
			NSLog(@"Initialized cell %u",i);
		}
}


- (NSInteger)tableView:(UITableView *)table numberOfRowsInSection:(NSInteger)section {
	return cells.count;
}

- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath *)indexPath {
	UITableViewCell *cell = [cells objectAtIndex:indexPath.row];
	if (cell.accessoryType == UITableViewCellAccessoryCheckmark) {
		cell.accessoryType = UITableViewCellAccessoryNone;
		NSLog(@"Deselected category %@",cell.textLabel.text);
	}
	else {
		cell.accessoryType = UITableViewCellAccessoryCheckmark;
		NSLog(@"Selected category %@",cell.textLabel.text);
	}
	
}


// Row display. Implementers should *always* try to reuse cells by setting each cell's reuseIdentifier and querying for available reusable cells with dequeueReusableCellWithIdentifier:
// Cell gets various attributes set automatically based on table (separators) and data source (accessory views, editing controls)

- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath {
	return  [cells objectAtIndex: indexPath.row];
}

- (void)didReceiveMemoryWarning {
	// Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
	
	// Release any cached data, images, etc that aren't in use.
}

- (void)viewDidUnload {
	[cells release];
}


- (void)dealloc {
    [super dealloc];
}


@end
