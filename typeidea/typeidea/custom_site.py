from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_title = 'Typeidea管理后台'

    # Text to put in each page's <h1>.
    site_header = 'Typeidea'

    # Text to put at the top of the admin index page.
    index_title = '首页'


custom_site = CustomSite(name='cus_admin')
