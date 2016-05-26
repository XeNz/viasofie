// $( document ).ready(
//     $(function() {
//     $('#select_province').change(function() {
//         console.log($('#select_province option:selected').val())
//         selectievar = $('#select_province option:selected').val();
//         $.ajax({
//           type: 'POST',
//           url: '/nl/sell',
//           data: {'selectie': selectievar, 'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()},
//           dataType: 'jsonp',
//           success: function(data) {
//       	  console.log("gelukt"); },
//    		  error: function(data) {
//    		  console.log(data);
//    		  console.log("niet gelukt"); }
//         });
//     	});
// 	})
// );