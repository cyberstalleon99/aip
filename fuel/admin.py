from django.contrib import admin
from .models import (Transaction, Tank, Reading)

# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('trans_date','unit','trans_type','fwf','processed_by','tank_site','project_site','amount','price','smr','kmr')
    list_filter = ('trans_date','unit','trans_type','processed_by','tank_site','project_site')
    exclude = ('create_date',)
    save_as = True

@admin.register(Tank)
class TankAdmin(admin.ModelAdmin):
    list_display = ('name','location','max_capacity',)
    list_filter = ('name','location',)

@admin.register(Reading)
class ReadingAdmin(admin.ModelAdmin):
    list_display = ('tank','read_date','conducted_by','reading')
    list_filter = ('tank','read_date','conducted_by','reading')
