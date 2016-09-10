$(function() {
	$(".form-row:not(.empty-form) .field-ingredient select").chosen();

	$(".add-row a").on("click", function() {
		$(".form-row:not(.empty-form) .field-ingredient select").chosen();
	});
});
