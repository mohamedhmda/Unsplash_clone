from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),
    path('image/<int:pk>', views.ImageDetailView.as_view(), name = 'image'),
    path('upload/', views.UploadImage, name = 'uploadimage'),
    path('editimage/<int:pk>', views.EditImage.as_view(), name = 'editimage'),

    path('deleteimagee/<int:pk>', views.DeleteImagee.as_view(), name = 'deleteimagee'), # the class
    path('deleteimage/<int:image_id>', views.DeleteImage, name = 'deleteimage'), # the view ( so we can add a script to delete from imgbb.com)
    path('delete/<path:image_name>', views.DeleteImageFromLocal, name = 'deleteimagelocal'),

    path('download/<int:image_id>', views.DownloadImage, name = 'downloadimage'),
    path('like/<int:image_id>', views.like_image, name = 'likeimage'),
    path('unlike/<int:image_id>', views.unlike_image, name = 'unlikeimage'),

    path('search/', views.SearchView.as_view(), name = 'searchimage'),

    path('colection/<int:pk>', views.CollectionDetailView.as_view(), name = 'collectiondetail'),
    path('createcolection/', views.CreateCollection.as_view(), name = 'createcollection'),
    path('editcollection/<int:pk>', views.EditCollection.as_view(), name = 'editcollection'),
    path('deletecollection/<int:pk>', views.DeleteCollection.as_view(), name = 'deletecollection'),

    path('addimagetocollection/<int:collection_id>/<int:image_id>', views.AddImageToCollection, name = 'addimagetocollection'),
    path('removeimagefromcollection/<int:collection_id>/<int:image_id>', views.RemoveImageFromCollection, name = 'removeimagefromcollection'),

    path('signup/', views.signup, name = 'signup'),
    path('profile/<int:pk>', views.ProfileDetailView.as_view(), name = 'profile'),
    path('editprofile/<int:pk>', views.EditProfileView.as_view(), name = 'editprofile'),
    path('follow/<int:user_id>', views.FollowUser, name = 'follow'),
    path('unfollow/<int:user_id>', views.UnfollowUser, name = 'unfollow'),
]
