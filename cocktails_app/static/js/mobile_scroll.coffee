$ = require("npm-zepto")
debounce = require("just-debounce")

module.exports = {
	upClass: "mobile-menu--up"
	downClass: "mobile-menu--down"
	stateDelay: 100
	states: {
		up: "up"
		down: "down"
	}

	init: ->
		@menu = $(".mobile-menu")
		atStart = true
		@lastScroll = $(window).scrollTop()

		@scrollWatcher()
		@dbScrollStart = debounce(@onScroll, 100, atStart)
		atStart = false
		@dbScrollEnd = debounce(@onScroll, 100, atStart)

	scrollWatcher: ->
		$(document).on("touchmove, scroll", (e) =>
			@dbScrollStart()
			@dbScrollEnd()
		)

	onScroll: ->
		scroll = $(window).scrollTop()

		return if scroll == @lastScroll

		if scroll > @lastScroll
			@changeState(@states.down)
		else
			@changeState(@states.up)

		@lastScroll = scroll

	changeState: (state) ->
		clearTimeout(@stateTimeout) if @stateTimeout?

		@stateTimeout = setTimeout(=>
			if state == @states.up
				@menu.removeClass(@downClass).addClass(@upClass)
			else if state == @states.down
				@menu.removeClass(@upClass).addClass(@downClass)
		, @stateDelay)
}
