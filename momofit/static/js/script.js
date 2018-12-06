$(document).ready(function(){
  $('.modal').modal();
  $('select').formSelect();
  $('.modal').modal();
  $('.sidenav').sidenav();
  var options = {format:'yyyy-mm-dd', setDefaultDate:true};
  $('.datepicker').datepicker(options);
});