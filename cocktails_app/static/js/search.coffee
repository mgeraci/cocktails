$ = require("npm-zepto")

module.exports = {
	init: ->
		@hasSearch = false
		@header = $(".page-header")
		@input = $(".page-header-search input")
		@showSearchClass = "hasSearch"
		@focusIfMobile()

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

	focusIfMobile: ->
		input = $(".page-content #id_query")

		return if !input.length

		if input.val() == ""
			input.focus()

	_showForm: ->
		@header.addClass(@showSearchClass)
		@input.focus()
		@hasSearch = true

	_hideForm: ->
		@header.removeClass(@showSearchClass)
		@hasSearch = false
}
