//comments_pr
$('#comments_pr').click(function(){
if(!$('#opportunity').is(':hidden'))
{
    $('#opportunity').hide('slow');
    return
}
$('#opportunity').show("slow");
});