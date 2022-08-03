var sub = $("#submitkeyword");
    function submitkeey(){
        console.log(allKeywords[0]);
          $("#hidden").val(allKeywords.join(","));
        
       
        $("#key-form").submit();
        //ky.submit();



    }
    //The entered keywords
var allKeywords = []

//Delete a keyword
function deleteWord(element){
  var index = allKeywords.indexOf($(element).parent('.keyword').text());
  if(index !== -1){                                  
    allKeywords.splice(index, 1);
  }
  $(element).parent('.keyword').remove();
}

//Add a keyword
function addWord(word){

if(allKeywords.length === 3){
    alert('You can only enter 3 keywords');
    $(txtInput).val('');
    return;
    
}

  if(word === undefined || word === ''){
    return;
  }

  
  
  allKeywords.push(word);
  
  $('#divKeywords > #txtInput').before($('<p class="keyword">' + word + '<a class="delete" onclick="deleteWord(this)"><img src="/static/icons/cut.png" /></a></p>'));
  $('#txtInput').val('');
  $('#txtInput').focus();
}

//On focus out, add word
function addWordFromTextBox(){
  var val = $('#txtInput').val();
  if(val !== undefined && val !== ''){
    addWord(val);
  }
}

//On key press, check for , or ;
function checkLetter(){
  var val = $('#txtInput').val()
  if(val.length > 0){
    var letter = val.slice(-1);
    if(letter === ',' || letter === ';'){
      var word = val.slice(0,-1);
      if(word.length > 0){
        addWord(word);
      }
    }
  }
}

$('#txtInput').blur(addWordFromTextBox);
$('#txtInput').keyup(checkLetter);
$('#divKeywords').click(function(){ $('#txtInput').focus(); });