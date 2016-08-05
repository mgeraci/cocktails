$ = require("npm-zepto")

module.exports = {
	init: ->
		@hasSearch = false
		@header = $(".page-header")
		@input = $(".page-header-search input")
		@showSearchClass = "hasSearch"

		# toggle form on icon click
		$("body").on("click", ".page-header-search-icon", (e) =>
			if @hasSearch
				@_hideForm()
			else
				@_showForm()
		)

		# hide form on blur, if blank
		@input.on("blur", (e)=>
			@_hideForm() if @input.val() == ""
		)

	_showForm: ->
		@header.addClass(@showSearchClass)
		@input.focus()
		@hasSearch = true

	_hideForm: ->
		@header.removeClass(@showSearchClass)
		@hasSearch = false
}
