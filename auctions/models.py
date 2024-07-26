from django.utils import timezone # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore
from django.db import models # type: ignore


class User(AbstractUser):
    pass

class AuctionListing(models.Model):

    CATEGORY_CHOICES = [
    ('fashion', 'Fashion'),
    ('toys', 'Toys'),
    ('electronics', 'Electronics'),
    ('home', 'Home'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auction_listings')
    active = models.BooleanField(default=True)
    image_url = models.URLField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, blank=True)

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='bids')

    def __str__(self):
        return f"{self.amount} by {self.user.username}"

class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    auction_listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.auction_listing.title}"        

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey('AuctionListing', on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.user.username}'s Watchlist"

    class Meta:
        unique_together = ('user', 'listing')

class Bid(models.Model):
    auction_listing = models.ForeignKey('AuctionListing', related_name='bids', on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Bid by {self.bidder.username} on {self.auction_listing.title} for {self.amount}"

class Comment(models.Model):
    auction_listing = models.ForeignKey('AuctionListing', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.auction_listing.title}"            
