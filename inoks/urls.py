from django.conf.urls import url

from inoks.Views import ProductViews, UserViews, OrderViews, ReportViews, EarningsViews, DashboardViews, SettingViews, \
    TreeViews, RefundViews

app_name = 'inoks'

urlpatterns = [

    # Dashboard
    url(r'dashboard/admin-dashboard/$', DashboardViews.return_admin_dashboard, name='admin-dashboard'),
    url(r'dashboard/user-dashboard/$', DashboardViews.return_user_dashboard, name='user-dashboard'),
    url(r'dashboard/admin-dashboard/sil/(?P<pk>\d+)$', DashboardViews.pending_profile_delete,
        name='bekleyen-kullanicilar-sil'),
    url(r'dashboard/admin-dashboard/(?P<pk>\d+)$', DashboardViews.getPendingProfile, name='getPendingProfile'),
    url(r'kullanici-onayla/$', DashboardViews.profile_active_passive, name="kullanici-onayla"),
    url(r'dashboard/admin-dashboard/sil/(?P<pk>\d+)$', DashboardViews.pending_order_delete,
        name='bekleyen-siparisler-sil'),
    url(r'dashboard/admin-dashboard/(?P<pk>\d+)$', DashboardViews.getPendingOrder, name='getPendingOrder'),
    url(r'siparis-onayla/$', DashboardViews.pendingOrderActive, name="siparis-onayla"),

    # Kullanıcılar
    url(r'kullanici/kullanici-ekle/$', UserViews.return_add_users, name='kullanici-ekle'),
    url(r'kullanici/kullanicilar/$', UserViews.return_users, name='kullanicilar'),
    url(r'kullanici/uyelerim/$', UserViews.return_my_users, name='uyelerim'),
    url(r'kullanici/bekleyen-kullanicilar/$', UserViews.return_pending_users, name='bekleyen-kullanicilar'),
    url(r'kullanici/iptal-edilen-kullanicilar/$', UserViews.return_deactive_users, name='iptal-edilen-kullanicilar'),
    url(r'kullanici/bekleyen-kullanicilar/sil/(?P<pk>\d+)$', UserViews.pending_profile_delete,
        name='bekleyen-kullanicilar-sil'),
    url(r'kullanici-onayla/$', UserViews.profile_active_passive, name="kullanici-onayla"),
    url(r'kullanici-iptal-et/$', UserViews.profile_passive, name="kullanici-iptal-et"),
    url(r'kullanici/bekleyen-kullanicilar/(?P<pk>\d+)$', UserViews.getPendingProfile, name='getPendingProfile'),
    url(r'kullanici/kullanicilar/(?P<pk>\d+)$', UserViews.getAllProfile, name='getAllProfile'),
    url(r'kullanici/iptal-edilen-kullanicilar/(?P<pk>\d+)$', UserViews.getDeactiveProfile, name='getDeactiveProfile'),
    url(r'kullanici-aktif-et/$', UserViews.profile_reactive, name="kullanici-aktif-et"),
    url(r'kullanici/kullanici-ekle/duzenle/(?P<pk>\d+)$', UserViews.users_update, name='kullanici-duzenle'),

    # Urunler
    url(r'urunler/urun-ekle/$', ProductViews.return_add_products, name='urun-ekle'),
    url(r'urunler/organik-temizlik-urunleri/$', ProductViews.return_health_products, name='organik-temizlik-urunleri'),
    url(r'urunler/genel-temizlik-urunleri/$', ProductViews.return_cleaning_products, name='genel-temizlik-urunleri'),
    url(r'urunler/arac-temizlik-urunleri/$', ProductViews.return_automotive_products, name='arac-temizlik-urunleri'),
    url(r'urunler/urunler/$', ProductViews.return_products, name='urunler'),
    url(r'urunler/urun-kategori-ekle/$', ProductViews.return_add_product_category, name='urun-kategori-ekle'),
    url(r'urunler/urun-listesi/$', ProductViews.return_product_list, name='urun-listesi'),
    url(r'urunler/urun-listesi/sil/(?P<pk>\d+)$', ProductViews.product_delete, name='product-sil'),
    url(r'urunler/urun-ekle/duzenle/(?P<pk>\d+)$', ProductViews.product_update, name='urun-duzenle'),
    url(r'urunler/urun-kategori-ekle/sil/(?P<pk>\d+)$', ProductViews.productCategory_delete,
        name='productCategory-sil'),
    url(r'urunler/urun-kategori-ekle/duzenle/(?P<pk>\d+)$', ProductViews.productCategory_update,
        name='urun-kategori-ekle-duzenle'),
    url(r'urunler/urun-listesi/(?P<pk>\d+)$', ProductViews.getProduct, name='getProduct'),

    # Siparisler
    url(r'siparisler/siparis-ekle/$', OrderViews.return_add_orders, name='siparis-ekle'),
    url(r'siparisler/bekleyen-siparisler/$', OrderViews.return_pending_orders, name='bekleyen-siparisler'),
    url(r'siparisler/siparislerim/$', OrderViews.return_my_orders, name='siparislerim'),
    url(r'siparisler/siparislerim/(?P<pk>\d+)$', OrderViews.getMyOrder, name='getMyOrder'),
    url(r'siparisler/siparisler/$', OrderViews.return_orders, name='siparisler'),
    url(r'siparisler/siparis-durumlari/$', OrderViews.return_order_situations, name='siparis-durumlari'),
    url(r'siparisler/bekleyen-siparisler/sil/(?P<pk>\d+)$', OrderViews.pending_order_delete,
        name='bekleyen-siparisler-sil'),
    url(r'siparisler/bekleyen-siparisler/(?P<pk>\d+)$', OrderViews.getPendingOrder, name='getPendingOrder'),
    url(r'siparis-onayla/$', OrderViews.pendingOrderActive, name="siparis-onayla"),

    # İadeler
    url(r'iadeler/iade-olustur/$', RefundViews.return_add_refund, name='iade-olustur'),
    url(r'iadeler/iadeler/$', RefundViews.return_refunds, name='iadeler'),
    url(r'iadeler/iade-durumlari/$', RefundViews.return_refund_situations, name='iade-durumlari'),
    url(r'iadeler/iade-durumlari/sil/(?P<pk>\d+)$', RefundViews.refund_situations_delete, name='iade-durum-sil'),
    url(r'iadeler/iade-durumlari/duzenle/(?P<pk>\d+)$', RefundViews.refund_situations_update,
        name='iade-durum-duzenle'),

    # Raporlar
    url(r'raporlar/rapor-olustur/$', ReportViews.return_create_report, name='rapor-olustur'),

    # Kazançlar
    url(r'kazanclar/kazanclar/$', EarningsViews.return_all_earnings_report, name='kazanclar'),
    url(r'kazanclar/kazanclarim/$', EarningsViews.return_my_earnings_report, name='kazanclarim'),

    # Ayarlar
    url(r'ayarlar/profil-ayarlari/$', SettingViews.return_profil_settings, name='profil-ayarlari'),
    url(r'ayarlar/sistem-ayarlari/$', SettingViews.return_system_settings, name='sistem-ayarlari'),

    # SoyAgacı
    url(r'soyagaci/soy-agacim/$', TreeViews.return_my_tree, name='soy-agacim'),
    url(r'soyagaci/soy-agaclari/$', TreeViews.return_all_tree, name='soy-agaclari'),

]