
from flask_assets import Bundle, Environment

css_all = Bundle("css/bootstrap.min.css",
                 "css/main.css",
                 "css/bootstrap-responsive.min.css",
                 filters="cssmin",
                 output="css/all.css")

js_vendor = Bundle("js/vendor/jquery-1.8.3.min.js",
                   "js/vendor/bootstrap.min.js",
                   "js/vendor/socket.io.min.js",
                   output="js/vendor.js")

assets = Environment()
assets.register('css', css_all)
assets.register('js_vendor', js_vendor)
