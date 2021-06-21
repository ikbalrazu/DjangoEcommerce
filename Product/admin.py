from django.contrib import admin
from Product.models import Category, Product, Images, CommentModel, Color
from mptt.admin import DraggableMPTTAdmin
# Register your models here.
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Product,
            'category',
            'products_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Product,
                                                'category',
                                                'products_count',
                                                cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'


admin.site.register(Category, CategoryAdmin)

admin.site.register(Images)


class productImageInline(admin.TabularInline):
    model = Images
    extra = 5

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','status','created_at','updated_at','image_tag']
    list_filter = ['title','created_at']
    list_per_page = 10
    search_fields = ['title','new_price','detail']
    inlines = [productImageInline]
    prepopulated_fields = {'slug':('title',)}



admin.site.register(Product,ProductAdmin)

@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','product','subject','comment','rate','status','created_at','updated_at']
    list_filter = ['status','created_at']
    list_per_page = 10 

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name','code','colortag']




