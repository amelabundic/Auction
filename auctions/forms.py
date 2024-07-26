from tokenize import Comment
from django.utils import timezone # type: ignore
from django import forms # type: ignore
from .models import AuctionListing, Bid, User
from commerce.auctions import models # type: ignore

class AuctionListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'starting_bid', 'category', 'image_url']

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.bidder.username} - ${self.bid_amount}"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']        
         