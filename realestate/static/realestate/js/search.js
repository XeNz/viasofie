$( document ).ready(
    $(function() {
    $('#select_province').change(function() {
        console.log($('#select_province option:selected').val())
    	});
	})
);