from django.contrib import admin
from .models import Category, Product, Size, Color, Variants, Images, Slide, Categoryproduct
import admin_thumbnails


@admin_thumbnails.thumbnail('image')
class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('id',)
    extra = 1
    show_change_link = True


@admin_thumbnails.thumbnail('image')
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['image', 'name', 'image_thumbnail']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category', 'slug', 'available', 'image_tag']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['available']
    inlines = [ ProductImageInline, ProductVariantsInline ]
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'color_tag']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']

@admin.register(Variants)
class VariantsAdmin(admin.ModelAdmin):
    list_display = ['name', 'product', 'size', 'color', 'quantity', 'price', 'image_tag']


@admin.register(Categoryproduct)
class CategoryproductAdmin(admin.ModelAdmin):
    list_display = ['image', 'image_tag']

@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['image','image_tag']