$ = require("npm-zepto")
debounce = require("just-debounce")

module.exports = {
	upClass: "mobile-menu--up"
	downClass: "mobile-menu--down"

	init: ->
		@menu = $(".mobile-menu")
		@maxScroll = $("body").height() - $(window).height()
		@lastScroll = $(window).scrollTop()

		atStart = true
		@scrollWatcher()
		@dbScrollStart = debounce(@onScroll, 100, atStart)
		atStart = false
		@dbScrollEnd = debounce(@onScroll, 100, atStart)

	scrollWatcher: ->
		@document = $(document)
		@body = $("body")

		@document.on("scroll", (e) =>
			@dbScrollStart()
			@dbScrollEnd()
		)

		@document.on("touchmove", (e) =>
			@onTouchMove(e)
		)

	onScroll: ->
		scroll = $(window).scrollTop()

		# keep scroll in bounds to counteract measuring the "rubber band" effect
		# on iOS
		if scroll > @maxScroll
			scroll = @maxScroll

		return if scroll == @lastScroll

		if scroll > @lastScroll
			@menu.removeClass(@upClass).addClass(@downClass)
		else
			@menu.removeClass(@downClass).addClass(@upClass)

		@lastScroll = scroll

	onTouchMove: (e) ->
		@onScroll()
}
