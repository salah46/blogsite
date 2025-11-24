from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from blog.models import Post


class LatestPostsFeed(Feed):
    title = "My Blog"
    link = reverse_lazy("blog:post_list")
    description = "New posts of my blog."

    def items(self):
        return Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-publish')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.publish

    def item_author_name(self, item):
        return item.author.username

    def item_author_email(self, item):
        return item.author.email

    def item_author_link(self, item):
        return reverse_lazy("blog:post_list") + f"?author={item.author.username}"

    def item_categories(self, item):
        return [tag.name for tag in item.tag.all()]

    def item_comments(self, item):
        return reverse_lazy("blog:post_detail", args=[
            item.publish.year,
            item.publish.month,
            item.publish.day,
            item.slug
        ]) + "#comments"
