$(document).ready(function(){
    $("#reference_search").hide();
    $("#advancedsearch-button").click(function(){
        $("#reference_search").fadeOut( "slow", function(){
            $("#advanced_search").fadeIn( "slow", "");
        });
        
    });
    $("#referencesearch-button").click(function(){
        $("#advanced_search").fadeOut( "slow", function(){
            $("#reference_search").fadeIn( "slow", "");
        });
    });
});
