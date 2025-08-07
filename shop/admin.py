from shop.models import Product, Category, Galery
from django.contrib import admin
from django.utils.safestring import mark_safe

class GaleryInline(admin.TabularInline):
    fk = "product"
    model = Galery
    extra = 1
    max_num = 8


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "parent", "get_product_count")
    prepopulated_fields = {"slug": ("title",)}

    def get_product_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return "0"
    get_product_count.short_description = "Кількість товару"



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','price','category','quantity','slug','size','color', "create_at", "get_photo")
    list_editable = ("price","size","color", "quantity",)
    list_filter = ("title","price",)
    list_display_links = ("title",)
    prepopulated_fields = {"slug": ("title",)}

    fields = ('title','category','price','quantity', 'slug','size','color', "create_at")

    inlines = (GaleryInline,)

    def get_photo(self, obj):
        if obj.images.all():
            return mark_safe(f"<img src='{obj.images.first().img.url}' width='75'>")
        else:
            return "-"

    get_photo.short_description = "Фото"




admin.site.register(Galery)




