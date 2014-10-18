//
//  LocalPhotosViewController.m
//  TroglodytePhotoDrop
//
//  Created by dio on 10/18/14.
//  Copyright (c) 2014 dio. All rights reserved.
//

#import "LocalPhotosViewController.h"
#import <AssetsLibrary/AssetsLibrary.h>
#import "FlickrPhoto.h"
#import "PhotoCell.h"
#import "Flickr.h"

@interface LocalPhotosViewController () <UICollectionViewDelegate, UICollectionViewDataSource>
@property (weak, nonatomic) IBOutlet UICollectionView *collectionViewLocalPhotos;
@property (nonatomic, strong) Flickr *flickr;
@end

NSMutableArray *photoArray;
NSArray *flickrPhotosArray;

@implementation LocalPhotosViewController

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}


- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view.
    if([ALAssetsLibrary authorizationStatus])
    {
        //Library Access code goes here
        ALAssetsLibrary *assetLibrary = [[ALAssetsLibrary alloc] init];
        [assetLibrary enumerateGroupsWithTypes:ALAssetsGroupAll usingBlock:^(ALAssetsGroup *group, BOOL *stop) {
            if(group)
            {
                //Filter photos
                photoArray = [self getContentFrom:group withAssetFilter:[ALAssetsFilter allPhotos]];
                //Enumerate through the group to get access to the photos.

                //[contentDictionary setObject:photoArray forKey:@"Photos"];

                [[NSNotificationCenter defaultCenter] postNotificationName:@"assetread" object:nil];

            }
        } failureBlock:^(NSError *error) {
            NSLog(@"Error Description %@",[error description]);
        }];
    }
    else
    {
        UIAlertView *alertView = [[UIAlertView alloc] initWithTitle:@"Permission Denied" message:@"Please allow the application to access your photo and videos in settings panel of your device" delegate:self cancelButtonTitle:@"Ok" otherButtonTitles: nil];
        [alertView show];
    }

    self.flickr = [[Flickr alloc] init];
    [self.flickr searchFlickrForTerm:@"cats" completionBlock:^(NSString *searchTerm, NSArray *results, NSError *error) {
        if(results && [results count] > 0) {
            // 2
            flickrPhotosArray = results;
            // 3
            dispatch_async(dispatch_get_main_queue(), ^{
                // Placeholder: reload collectionview data
            });
        } else { // 1
            NSLog(@"Error searching Flickr: %@", error.localizedDescription);
        } }];
}

- (void)didReceiveMemoryWarning
{
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

-(NSMutableArray *) getContentFrom:(ALAssetsGroup *) group withAssetFilter:(ALAssetsFilter *)filter
{
    NSMutableArray *contentArray = [NSMutableArray array];
    [group setAssetsFilter:filter];

    [group enumerateAssetsUsingBlock:^(ALAsset *result, NSUInteger index, BOOL *stop) {

        //ALAssetRepresentation holds all the information about the asset being accessed.
        if(result)
        {

            ALAssetRepresentation *representation = [result defaultRepresentation];

            //Stores releavant information required from the library
            NSMutableDictionary *tempDictionary = [[NSMutableDictionary alloc] init];
            //Get the url and timestamp of the images in the ASSET LIBRARY.
            NSString *imageUrl = [representation UTI];
            NSDictionary *metaDataDictonary = [representation metadata];
            NSString *dateString = [result valueForProperty:ALAssetPropertyDate];

                        NSLog(@"imageUrl %@",imageUrl);
                        NSLog(@"metadictionary: %@",metaDataDictonary);

            //Check for the date that is applied to the image
            // In case its earlier than the last sync date then skip it. ##TODO##

            NSString *imageKey = @"ImageUrl";
            NSString *metaKey = @"MetaData";
            NSString *dateKey = @"CreatedDate";

            [tempDictionary setObject:imageUrl forKey:imageKey];
            [tempDictionary setObject:metaDataDictonary forKey:metaKey];
            [tempDictionary setObject:dateString forKey:dateKey];
            [tempDictionary setObject:[result valueForProperty:ALAssetPropertyType] forKey:@"UIImagePickerControllerMediaType"];
            [tempDictionary setObject:[UIImage imageWithCGImage:[[result defaultRepresentation] fullScreenImage]] forKey:@"UIImagePickerControllerOriginalImage"];
            [tempDictionary setObject:[[result valueForProperty:ALAssetPropertyURLs] valueForKey:[[[result valueForProperty:ALAssetPropertyURLs] allKeys] objectAtIndex:0]] forKey:@"UIImagePickerControllerReferenceURL"];

            //Add the values to photos array.
            [contentArray addObject:tempDictionary];
        }
    }];
    return contentArray;
}

#pragma mark - UICollectionView methods

- (UICollectionViewCell *)collectionView:(UICollectionView *)collectionView cellForItemAtIndexPath:(NSIndexPath *)indexPath
{
    PhotoCell *cell = [collectionView dequeueReusableCellWithReuseIdentifier:@"LocalPhotoCell" forIndexPath:indexPath];
    cell.backgroundColor = [UIColor whiteColor];
    //get image into cell
    NSDictionary *dict = [photoArray objectAtIndex:indexPath.row];
    UIImageView *imageview = [[UIImageView alloc] initWithImage:[dict objectForKey:UIImagePickerControllerOriginalImage]];
    [imageview setContentMode:UIViewContentModeScaleAspectFit];
    //FlickrPhoto *flickrPhoto = [FlickrPhoto init];
    //flickrPhoto.largeImage = imageview.image;
    cell.imageView.image = imageview.image;

    return cell;
}

- (NSInteger)collectionView:(UICollectionView *)collectionView numberOfItemsInSection:(NSInteger)section
{
    return [photoArray count];
    //return [flickrPhotosArray count];
}

- (NSInteger)numberOfSectionsInCollectionView:(UICollectionView *)collectionView
{
    return 1;
}

- (void)collectionView:(UICollectionView *)collectionView didSelectItemAtIndexPath:(NSIndexPath *)indexPath
{
    // TODO: Select Item
}



@end
