$ = require("npm-zepto")
debounce = require("just-debounce")

module.exports = {
	upClass: "mobile-menu--up"
	downClass: "mobile-menu--down"

	init: ->
		@menu = $(".mobile-menu")
		atStart = true
		@lastScroll = $(window).scrollTop()

		@scrollWatcher()
		@dbScrollStart = debounce(@onScroll, 100, atStart)
		atStart = false
		@dbScrollEnd = debounce(@onScroll, 100, atStart)

	scrollWatcher: ->
		$(document).on("scroll", (e) =>
			@dbScrollStart()
			@dbScrollEnd()
		)

	onScroll: ->
		scroll = $(window).scrollTop()

		if scroll > @lastScroll
			@menu.removeClass(@upClass).addClass(@downClass)
		else
			@menu.removeClass(@downClass).addClass(@upClass)

		@lastScroll = scroll
}
