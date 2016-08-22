# vendor
Fastclick = require("fastclick")
modernizr = require("./vendor/modernizr.js")

# pages
Index = require("./index.coffee")
Search = require("./search.coffee")
Recipe = require("./recipe.coffee")
Navigation = require("./navigation.coffee")
MobileMenu = require("./mobile-menu.coffee")

# execute
Fastclick.attach(document.body)
Index.init()
Search.init()
Recipe.init()
Navigation.init()
MobileMenu.init()
