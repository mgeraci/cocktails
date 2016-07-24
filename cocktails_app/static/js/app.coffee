# vendor
Fastclick = require("fastclick")
modernizr = require("./vendor/modernizr.js")

# pages
Search = require("./search.coffee")

# execute
Fastclick.attach(document.body)
Search.init()
