# vendor
Fastclick = require("fastclick")
modernizr = require("./vendor/modernizr.js")

# pages
Search = require("./search.coffee")
Recipe = require("./recipe.coffee")

# execute
Fastclick.attach(document.body)
Search.init()
Recipe.init()
