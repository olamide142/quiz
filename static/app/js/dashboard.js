
function fileData(){
    // Get file name and extension 
    var extension = document.getElementById('file').value;
    console.log(extension);
    var extension = extension.split('.');
    EXTENSION = extension[extension.length-1];
    document.getElementById('file_extension').value = EXTENSION;
    li = ['png', 'jpg', 'jpeg', 'gif'];
    valid = False;

    for(i = 0; i < li.length; i++){
        if(li[i] == EXTENSION){
            valid = True;
            break;
        }
    }
    if (valid == False){
        alert("This is not a allowed format.");
        document.getElementById('file').value = '';
    }
}
