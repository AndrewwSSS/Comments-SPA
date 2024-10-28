from rest_framework import routers

from comments.views import CommentViewSet

router = routers.DefaultRouter()
router.register("comments", CommentViewSet, basename="comments")

urlpatterns = router.urls
