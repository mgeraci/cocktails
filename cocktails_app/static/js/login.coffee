$ = require("npm-zepto")

module.exports = {
	passwordGoalLength: 4

	init: ->
		return if !$(".page-login").length

		@form = $(".login-form")
		@input = $(".page-login-fieldset-input")
		@listen()

	listen: ->
		$(".login-button").on("click tap", (e) =>
			value = $(e.currentTarget).val()
			currentPassword = @input.val()
			newPassword = "#{currentPassword}#{value}"

			@input.val(newPassword)
			@setIndicatorsTo(newPassword.length)

			if newPassword.length == @passwordGoalLength
				@form.submit()
		)

	setIndicatorsTo: (count) ->
		$(".login-buttons-indicators-indicator").each((i) ->
			if i < count
				$(this).addClass("filled")
			else
				$(this).removeClass("filled")
		)
}
