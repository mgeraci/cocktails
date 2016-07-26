$ = require("jquery")

module.exports = {
	directions: {
		increment: "increment"
		decrement: "decrement"
	}

	init: ->
		return if !$(".page-recipe").length

		@steps = $(".step")
		@listen()

	listen: ->
		$(".quantity-button").on("click tap", (e) =>
			button = $(e.currentTarget)
			field = button.closest(".quantity").find("input")

			if button.hasClass("quantity-button--increment")
				direction = "increment"
			else
				direction = "decrement"

			@changeValue(field, direction)
		)

	changeValue: (field, direction) ->
		value = field.val()

		if direction == @directions.increment
			value++
		else if direction == @directions.decrement
			value--

		if value < 1
			value = 1
		else if value > 30
			value = 30

		field.val(value)
		@updateRecipeQuantities(value)

	updateRecipeQuantities: (quantity) ->
		for step in @steps
			step = $(step)
			amount = step.find(".step-amount")
			unit = step.find(".step-unit")

			continue if !amount.length

			originalAmount = parseFloat($(amount).data("original-amount"))
			newAmount = originalAmount * quantity

			amount.text(@_formatAmount(newAmount))

			if newAmount > 1
				unit = unit.text(unit.data("unit-plural"))
			else
				unit = unit.text(unit.data("unit-singular"))

	# duplicate of templatetags/recipe_extras.py:format_value
	_formatAmount: (amount) ->
		step = String(amount)
		matches = step.match(/\d+\.\d+/)

		return step if !matches?.length

		for num in step.match(/\d+\.\d+/)
			[whole, fraction] = num.split('.')

			if whole == '0'
				step = step.replace('0', '')

			if fraction == '0'
				step = step.replace(num, whole)
			else if fraction == '25'
				step = step.replace('.25', '¼')
			else if fraction == '33'
				step = step.replace('.33', '⅓')
			else if fraction == '5'
				step = step.replace('.5', '½')
			else if fraction == '66'
				step = step.replace('.66', '⅔')
			else if fraction == '75'
				step = step.replace('.75', '¾')

			if whole == '0' and fraction == '0'
				step = step.replace(/^\. /, '', step)

		return step
}
