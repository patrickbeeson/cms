// Function for printing stories and other content

$(document).ready(function() {
 $('ul.content_tools').prepend('<li class="print">Print: <a href="#"><img src="/images/icons/printer.png" alt="Print this content"></a></li>');
 $('ul.content_tools li.print a').click(function() {
  window.print();
  return false;
 });
}); 