$ = require("jquery")
Fraction = require("fractional").Fraction

module.exports = {
	directions: {
		increment: "increment"
		decrement: "decrement"
	}

	init: ->
		return if !$(".page-recipe").length

		@steps = $(".step")
		@listen()
		@updateRecipeQuantities(1)
		@steps.closest("ul").removeClass("uninitialized")

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
		value = parseInt(field.val(), 10)

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

			num = amount.data("original-amount-num")
			den = amount.data("original-amount-den")

			newAmountFraction = new Fraction(num, den).multiply(quantity)
			newAmountFloat = newAmountFraction.numerator / newAmountFraction.denominator

			amount.text(@_formatAmount(newAmountFraction))

			if newAmountFraction > 1
				unit = unit.text(unit.data("unit-plural"))
			else
				unit = unit.text(unit.data("unit-singular"))

	_fractionLookup: {
		1: {
			2: "½"
			3: "⅓"
			4: "¼"
			5: "⅕"
			6: "⅙"
			7: "⅐"
			8: "⅛"
			9: "⅑"
			10: "⅒"
		}
		2: {
			3: "⅔"
			5: "⅖"
		}
		3: {
			4: "¾"
			5: "⅗"
			8: "⅜"
		}
		4: {
			5: "⅘"
		}
		5: {
			6: "⅚"
			8: "⅝"
		}
		7: {
			8: "⅞"
		}
	}

	# split the fraction into the integer and a fraction
	_formatAmount: (fraction) ->
		numerator = fraction.numerator % fraction.denominator
		int = Math.floor(fraction.numerator / fraction.denominator)
		fractionCharacter = this._fractionLookup[numerator]?[fraction.denominator]

		if fractionCharacter
			if int
				return "#{int} #{fractionCharacter}"
			else
				return fractionCharacter
		else
			return fraction.toString()
}
