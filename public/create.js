$(document).ready(function() {

$(".submit").click(function(e) {
  $.post("/submit", {"text": $("input[name='input']").val()});
  e.preventDefault();
});

});