$ = require("npm-zepto")

module.exports = {
	init: ->
		return if !$(".page-index").length

		@sectionClass = ".page-index-section"
		@collapseClass = "isCollapsed"
		@sections = $(@sectionClass)
		@listen()

	listen: ->
		$("body").on("click", ".page-index-section-label", (e)=>
			@sections.addClass(@collapseClass)
			$(e.currentTarget).closest(@sectionClass).removeClass(@collapseClass)
		)
}
