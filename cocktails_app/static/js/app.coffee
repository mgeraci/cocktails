# vendor
Fastclick = require("fastclick")
modernizr = require("./vendor/modernizr.js")

# pages
Index = require("./index.coffee")
Search = require("./search.coffee")
Recipe = require("./recipe.coffee")

# execute
Fastclick.attach(document.body)
Index.init()
Search.init()
Recipe.init()
