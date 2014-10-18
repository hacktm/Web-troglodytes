//
//  PhotoCell.h
//  TroglodytePhotoDrop
//
//  Created by dio on 10/18/14.
//  Copyright (c) 2014 dio. All rights reserved.
//

#import <UIKit/UIKit.h>
@class FlickrPhoto;

@interface PhotoCell : UICollectionViewCell
@property (nonatomic, strong) IBOutlet UIImageView *imageView;
@property (nonatomic, strong) FlickrPhoto *photo;
@end
