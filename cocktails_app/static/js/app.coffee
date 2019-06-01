# vendor
Fastclick = require("fastclick")
modernizr = require("./vendor/modernizr.js")

# pages
Login = require("./login.coffee")
Index = require("./index.coffee")
Search = require("./search.coffee")
Recipe = require("./recipe.coffee")
Navigation = require("./navigation.coffee")
MobileMenu = require("./mobile-menu.coffee")

# execute
Fastclick.attach(document.body)
Login.init()
Index.init()
Search.init()
Recipe.init()
Navigation.init()
MobileMenu.init()
