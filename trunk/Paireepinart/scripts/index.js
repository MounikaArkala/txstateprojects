
$(document).ready(function(){

   $("a").click(function(event){
   event.preventDefault();
   $(this).hide("slow");
 });

    $("a").addClass("test");

});
