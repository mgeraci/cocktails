$ = require("npm-zepto")

module.exports = {
	animationCount: 1

	init: ->
		return if !window.navigator.standalone

		$("body").on("click", "a", =>
			@startAnimation()
		)

		# search form
		$("body").on("submit", "form", =>
			@startAnimation()
		)

	startAnimation: ->
		animation = Math.floor(Math.random() * @animationCount)

		$(".page-navigation").addClass("page-navigation--is-navigating n#{animation}")
}
